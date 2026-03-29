# AuraChain Forensic Recorder 🎧🛡️

**AuraChain** is a high-fidelity, forensic-grade audio acquisition tool specifically optimized for macOS (Apple Silicon M3) and the MiniDSP UMIK-1. It is designed for long-term acoustic monitoring where data integrity, continuity, and "gold standard" audio quality are non-negotiable.

## ✨ Key Forensic Features
- **Lossless Quality:** Records in uncompressed 24-bit Linear PCM (WAV).
- **UMIK-1 Optimized:** Native support for 48kHz sampling (hardware-locked standard).
- **Data Integrity:** Real-time MD5 hashing for every audio segment, saved to a verifiable `manifest.txt`.
- **Gapless Continuity:** Configurable overlapping segments (e.g., 5 seconds) to ensure no data loss during file transitions.
- **Forensic Hierarchy:** Automatic organization by Case ID, Date, and Device ID.
- **Apple Silicon Native:** Performance-optimized for M-series architecture.

## 📋 Requirements
- **Hardware:** MacBook M3 (or M1/M2) or Intel Mac.
- **Microphone:** UMIK-1 (Recommended) or Built-in Microphone.
- **Software:** 
  - Python 3.10+
  - `portaudio` (System library)

## ⚙️ Installation

1. **Install PortAudio (via Homebrew):**
   ```bash
   brew install portaudio
   ```

2. **Clone and Setup Environment:**
   ```bash
   git clone https://github.com/yourusername/aurachain.git
   cd aurachain
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Dependencies:**
   ```bash
   pip install sounddevice soundfile numpy
   ```

## 🚀 Usage

1. **Configure:** Edit `forensic_recorder.py` to set your `CASE_ID` and `DEVICE_SUBSTRING`.
2. **Run:**
   ```bash
   python forensic_recorder.py
   ```
3. **Permissions:** macOS will prompt for Microphone access. Grant permissions in *System Settings > Privacy & Security*.

## 📂 Data Structure
The tool generates a standardized forensic directory:
```text
forensic_recordings/
└── CASE_2024_001/
    └── 2024-05-20/
        └── UMIK_1_Omni_Mic/
            ├── manifest.txt              # Contains MD5 hashes & timestamps
            ├── CASE_2024_001_PART001.wav
            └── CASE_2024_001_PART002.wav
```

## ⚖️ Disclaimer
This software is intended for professional forensic and acoustic analysis. Ensure your use of this tool complies with local laws regarding audio recording and privacy.
```

