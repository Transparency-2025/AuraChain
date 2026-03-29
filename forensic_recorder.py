import os
import time
import queue
import hashlib
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime

# --- CONFIGURATION ---
CASE_ID = "CASE_2024_001"
BASE_DIR = "./forensic_recordings"
SEGMENT_DURATION = 60  # seconds per file
OVERLAP_DURATION = 5   # seconds of overlap
SAMPLE_RATE = 48000    # UMIK-1 is 48kHz
CHANNELS = 1           # UMIK-1 is mono. 
SUBTYPE = 'PCM_24'     # 24-bit uncompressed
DEVICE_SUBSTRING = "UMIK-1" # Set to "Built-in" or None for default

# --- FOLDER STRUCTURE ---
current_date = datetime.now().strftime("%Y-%m-%d")
# We'll finalize the output_path after we confirm the device name

audio_queue = queue.Queue()

def get_device_info(name_substring):
    """Finds device ID and name. Returns (ID, Name)."""
    devices = sd.query_devices()
    
    # Try to find specific device
    if name_substring:
        for i, dev in enumerate(devices):
            if name_substring.lower() in dev['name'].lower():
                return i, dev['name']
    
    # Fallback to system default input
    default_input_id = sd.default.device[0]
    # Handle case where default might be -1
    if default_input_id == -1:
        raise RuntimeError("No input device found.")
    
    default_dev_info = sd.query_devices(default_input_id)
    return default_input_id, default_dev_info['name']

def calculate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def recording_worker(stop_event, output_path):
    """Consumes audio from queue and writes overlapping segments."""
    segment_samples = int(SEGMENT_DURATION * SAMPLE_RATE)
    overlap_samples = int(OVERLAP_DURATION * SAMPLE_RATE)
    
    buffer = np.zeros((0, CHANNELS), dtype='float32')
    file_count = 1

    print(f"[*] Worker active. Saving to: {output_path}")
    
    while not stop_event.is_set() or not audio_queue.empty():
        try:
            # Short timeout to allow checking stop_event
            data = audio_queue.get(timeout=1)
            if data is None: break
            buffer = np.append(buffer, data, axis=0)

            if len(buffer) >= segment_samples:
                to_save = buffer[:segment_samples]
                # Keep overlap for next segment
                buffer = buffer[segment_samples - overlap_samples:]
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{CASE_ID}_{timestamp}_PART{file_count:03d}.wav"
                full_file_path = os.path.join(output_path, filename)
                
                sf.write(full_file_path, to_save, SAMPLE_RATE, subtype=SUBTYPE)
                
                file_hash = calculate_md5(full_file_path)
                with open(os.path.join(output_path, "manifest.txt"), "a") as f:
                    f.write(f"{filename} | MD5: {file_hash} | UTC: {datetime.utcnow()}\n")
                
                print(f"[+] Saved: {filename} (MD5: {file_hash[:8]}...)")
                file_count += 1
        except queue.Empty:
            continue

def audio_callback(indata, frames, time, status):
    if status:
        print(f"[!] Audio Status: {status}", flush=True)
    audio_queue.put(indata.copy())

# --- MAIN EXECUTION ---
try:
    # 1. Identify Device
    device_id, device_name = get_device_info(DEVICE_SUBSTRING)
    clean_device_name = "".join([c if c.isalnum() else "_" for c in device_name])
    
    # 2. Setup Folder Structure
    output_path = os.path.join(BASE_DIR, CASE_ID, current_date, clean_device_name)
    os.makedirs(output_path, exist_ok=True)
    
    print(f"[*] Using Device: [{device_id}] {device_name}")
    print(f"[*] Format: {SUBTYPE} @ {SAMPLE_RATE}Hz")
    
    # 3. Start Background Worker
    stop_event = threading.Event()
    worker_thread = threading.Thread(target=recording_worker, args=(stop_event, output_path))
    worker_thread.start()

    # 4. Start Recording Stream
    with sd.InputStream(device=device_id, channels=CHANNELS, 
                        samplerate=SAMPLE_RATE, callback=audio_callback):
        print("\n>>> RECORDING... Press Ctrl+C to stop. <<<\n")
        while True:
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[*] Stopping recording (finishing current buffer)...")
    stop_event.set()
    audio_queue.put(None)
    worker_thread.join()
    print("[*] All files saved and hashed. Session closed.")
except Exception as e:
    print(f"\n[!] Critical Error: {e}")
