"""
Text-to-Speech Module
Handles generation of Polish voiceover audio
"""

import os
import torch
from TTS.api import TTS
from typing import Optional


class TTSEngine:
    """Handles text-to-speech generation"""
    
    def __init__(self, model_name: str = "tts_models/pl/mai_female/vits", device: str = "cuda"):
        """Initialize TTS engine
        
        Args:
            model_name: TTS model name
            device: Device to use (cuda or cpu)
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        self.tts = None
        
        print(f"TTS engine initialized with device: {self.device}")
    
    def load_model(self) -> bool:
        """Load TTS model
        
        Returns:
            True if successful
        """
        try:
            print(f"Loading TTS model: {self.model_name}")
            self.tts = TTS(model_name=self.model_name, progress_bar=False).to(self.device)
            print("TTS model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading TTS model: {e}")
            # Fallback to a basic model if specified model fails
            try:
                print("Attempting to load fallback TTS model...")
                self.tts = TTS(model_name="tts_models/pl/mai_female/vits", progress_bar=False).to(self.device)
                print("Fallback TTS model loaded successfully")
                return True
            except Exception as e2:
                print(f"Error loading fallback TTS model: {e2}")
                return False
    
    def generate_speech(self, text: str, output_path: str) -> Optional[str]:
        """Generate speech from text
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file, or None if failed
        """
        if not self.tts:
            if not self.load_model():
                return None
        
        if not text.strip():
            print("Warning: Empty text provided for TTS")
            return None
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            print(f"Generating speech: {text[:50]}...")
            self.tts.tts_to_file(text=text, file_path=output_path)
            
            if os.path.exists(output_path):
                print(f"Speech generated: {output_path}")
                return output_path
            else:
                print("Error: Audio file was not created")
                return None
                
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None
    
    def generate_speech_batch(self, segments: list, output_dir: str) -> list:
        """Generate speech for multiple segments
        
        Args:
            segments: List of segment dictionaries with 'translated_text' field
            output_dir: Directory to save audio files
            
        Returns:
            List of segments with added 'audio_path' field
        """
        os.makedirs(output_dir, exist_ok=True)
        
        result_segments = []
        for i, seg in enumerate(segments):
            text = seg.get('translated_text', '')
            if not text:
                print(f"Warning: Segment {i} has no translated text")
                result_seg = seg.copy()
                result_seg['audio_path'] = None
                result_segments.append(result_seg)
                continue
            
            audio_path = os.path.join(output_dir, f"segment_{i:04d}.wav")
            generated_path = self.generate_speech(text, audio_path)
            
            result_seg = seg.copy()
            result_seg['audio_path'] = generated_path
            result_segments.append(result_seg)
        
        return result_segments
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Get duration of audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds, or None if failed
        """
        try:
            import soundfile as sf
            data, samplerate = sf.read(audio_path)
            duration = len(data) / samplerate
            return duration
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            return None
