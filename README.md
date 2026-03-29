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
