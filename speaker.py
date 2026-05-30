"""
Text-to-Speech Module: Convert Response Text to Audio
Uses Piper TTS for fast, offline speech synthesis.

Why Piper?
- Ultra-fast: 1-2 seconds to generate speech for a full response
- Runs entirely offline (no API keys, no network latency)
- Good quality voices (multiple accents available)
- Lightweight: 100-200MB for all voices
- Open source (can customize further if needed)

Why NOT other options?
- ElevenLabs: Better quality but cloud-based, costs money
- Google TTS: Cloud-based, need API key
- Amazon Polly: Cloud-based, need AWS account
- Festival/eSpeak: Older, robot-like quality

For a local assistant that needs to feel instant, Piper is the sweet spot.
"""

import logging
import numpy as np
import subprocess
from pathlib import Path
from typing import Optional
from friday.config import (
    TTS_VOICE,
    TTS_SPEED,
    TTS_DEVICE,
    MODELS_DIR,
    DEBUG_MODE
)

logger = logging.getLogger(__name__)


class PiperTTSEngine:
    """
    Text-to-speech using Piper.
    
    Piper is installed as a standalone binary that we communicate with
    via command line. This is simpler and more reliable than trying to
    load it as a Python library.
    
    Workflow:
    1. User text: "Hello, how can I help?"
    2. We call: piper --model en_US-lessac-medium --output speech.wav
    3. We read the generated WAV file
    4. We play it back
    
    Simple, modular, and reliable.
    """
    
    def __init__(self):
        """Initialize the TTS engine."""
        self.voice_model = TTS_VOICE
        self.speed = TTS_SPEED
        self.piper_binary = self._find_piper_binary()
        self.is_ready = self.piper_binary is not None
        
        if self.is_ready:
            logger.info(f"Piper TTS initialized with voice: {self.voice_model}")
        else:
            logger.warning(
                "Piper binary not found. Install with:\n"
                "  pip install piper-tts\n"
                "  piper-download-voice en_US-lessac-medium"
            )
    
    def _find_piper_binary(self) -> Optional[Path]:
        """
        Find the piper executable.
        
        Piper can be installed in multiple ways:
        1. As a Python package (pip install piper-tts)
        2. As a standalone binary
        3. Built from source
        
        We check common locations.
        """
        import shutil
        
        # First, try finding it in PATH (most common case)
        piper_path = shutil.which("piper")
        if piper_path:
            return Path(piper_path)
        
        # Check if pip installed it
        try:
            import piper_tts
            piper_dir = Path(piper_tts.__file__).parent
            piper_path = piper_dir / "bin" / "piper"
            if piper_path.exists():
                return piper_path
        except ImportError:
            pass
        
        logger.warning("Could not find piper executable")
        return None
    
    def generate_speech(self, text: str) -> Optional[np.ndarray]:
        """
        Generate speech audio from text.
        
        Args:
            text: text to convert to speech
            
        Returns:
            numpy array of audio samples, or None if generation failed
            
        Example:
            >>> engine = PiperTTSEngine()
            >>> audio = engine.generate_speech("Hello world")
            >>> # audio is now a numpy array ready to play
        """
        
        if not self.is_ready:
            logger.warning("Piper TTS not ready")
            return None
        
        try:
            # Create temporary file for output
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                output_path = tmp.name
            
            # Call piper to generate speech
            # The --input and --output flags are standard for piper
            cmd = [
                str(self.piper_binary),
                "--model", self.voice_model,
                "--output-file", output_path,
                "--speed", str(self.speed)
            ]
            
            # Send text via stdin
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text, timeout=30)
            
            if process.returncode != 0:
                logger.error(f"Piper error: {stderr}")
                return None
            
            # Read the generated WAV file
            import scipy.io.wavfile as wavfile
            sample_rate, audio_data = wavfile.read(output_path)
            
            # Convert to float32 in range [-1, 1]
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Clean up temporary file
            Path(output_path).unlink()
            
            if DEBUG_MODE:
                logger.debug(f"Generated {len(audio_data)/sample_rate:.1f}s of speech")
            
            return audio_data
        
        except subprocess.TimeoutExpired:
            logger.error("Piper generation timed out")
            return None
        
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None


class MockTTSEngine:
    """
    Mock TTS for testing without Piper installed.
    Returns simulated audio data.
    """
    
    def __init__(self):
        logger.warning("Using MOCK TTS engine (testing mode)")
    
    def generate_speech(self, text: str) -> np.ndarray:
        """Return fake audio data."""
        # Generate silence proportional to text length
        # Rough estimate: 150 words per minute = 4 chars per 0.016 seconds
        estimated_duration = len(text) / 150.0  # in seconds
        sample_count = int(estimated_duration * 16000)  # 16kHz sample rate
        
        # Simulate a spoken word by generating quiet noise
        return np.random.randn(sample_count).astype(np.float32) * 0.01


class SpeakerOutput:
    """
    High-level interface for speech output.
    
    This handles:
    - Converting text to speech (if needed)
    - Playing audio
    - Managing audio playback (volume, device selection, etc.)
    """
    
    def __init__(self):
        """Initialize the speaker output."""
        self.tts_engine = self._get_tts_engine()
        self.audio_device = None
        logger.info("Speaker output initialized")
    
    def _get_tts_engine(self):
        """Get TTS engine (real or mock)."""
        engine = PiperTTSEngine()
        
        if not engine.is_ready:
            logger.warning("Falling back to mock TTS")
            return MockTTSEngine()
        
        return engine
    
    def play_text(self, text: str) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: text to speak
            
        Returns:
            True if successful, False otherwise
        """
        
        if not text:
            return False
        
        try:
            # Generate audio
            audio_data = self.tts_engine.generate_speech(text)
            
            if audio_data is None:
                logger.error("Failed to generate audio")
                return False
            
            # Play it
            self.play_audio(audio_data)
            return True
        
        except Exception as e:
            logger.error(f"Error playing text: {e}")
            return False
    
    def play_audio(self, audio_data: np.ndarray, sample_rate: int = 16000):
        """
        Play audio data.
        
        Args:
            audio_data: numpy array of audio samples
            sample_rate: sample rate in Hz
        """
        
        try:
            import sounddevice as sd
            
            # Normalize audio if needed
            if audio_data.max() > 1.0:
                audio_data = audio_data / 32768.0
            
            # Play the audio
            sd.play(audio_data, samplerate=sample_rate, blocking=True)
            
            if DEBUG_MODE:
                logger.debug(f"Played {len(audio_data)/sample_rate:.1f}s of audio")
        
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        # Nothing to clean up for Piper, but included for consistency
        logger.info("Speaker output cleaned up")
