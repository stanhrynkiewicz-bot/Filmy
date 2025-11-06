"""
Transcription Module
Handles speech-to-text using Whisper with CUDA support
"""

import os
import torch
import whisper
import numpy as np
from typing import List, Dict, Tuple, Optional


class TranscriptionEngine:
    """Handles video transcription using Whisper"""
    
    def __init__(self, model_size: str = "medium", device: str = "cuda", language: str = "en"):
        """Initialize transcription engine
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Device to use (cuda or cpu)
            language: Source language code
        """
        self.model_size = model_size
        self.device = device if torch.cuda.is_available() else "cpu"
        self.language = language
        self.model = None
        
        print(f"Transcription engine initialized with device: {self.device}")
    
    def load_model(self) -> bool:
        """Load Whisper model
        
        Returns:
            True if successful
        """
        try:
            print(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size, device=self.device)
            print("Whisper model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Optional[Dict]:
        """Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcription result with segments
        """
        if not self.model:
            if not self.load_model():
                return None
        
        try:
            print(f"Transcribing: {audio_path}")
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                task="transcribe",
                verbose=False,
                word_timestamps=True
            )
            print(f"Transcription complete: {len(result.get('segments', []))} segments")
            return result
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def get_segments(self, transcription_result: Dict) -> List[Dict]:
        """Extract segments from transcription result
        
        Args:
            transcription_result: Whisper transcription result
            
        Returns:
            List of segment dictionaries with start, end, and text
        """
        segments = []
        if transcription_result and 'segments' in transcription_result:
            for seg in transcription_result['segments']:
                segments.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': seg['text'].strip(),
                    'id': seg['id']
                })
        return segments
    
    def merge_short_segments(self, segments: List[Dict], min_duration: float = 1.0) -> List[Dict]:
        """Merge segments that are too short
        
        Args:
            segments: List of segment dictionaries
            min_duration: Minimum segment duration
            
        Returns:
            List of merged segments
        """
        if not segments:
            return []
        
        merged = []
        current_segment = segments[0].copy()
        
        for seg in segments[1:]:
            duration = current_segment['end'] - current_segment['start']
            
            if duration < min_duration:
                # Merge with next segment
                current_segment['end'] = seg['end']
                current_segment['text'] = current_segment['text'] + " " + seg['text']
            else:
                merged.append(current_segment)
                current_segment = seg.copy()
        
        # Add last segment
        merged.append(current_segment)
        
        return merged
    
    def split_long_segments(self, segments: List[Dict], max_duration: float = 30.0) -> List[Dict]:
        """Split segments that are too long at sentence boundaries
        
        Args:
            segments: List of segment dictionaries
            max_duration: Maximum segment duration
            
        Returns:
            List of split segments
        """
        result = []
        
        for seg in segments:
            duration = seg['end'] - seg['start']
            
            if duration <= max_duration:
                result.append(seg)
            else:
                # Split at sentence boundaries
                text = seg['text']
                sentences = self._split_into_sentences(text)
                
                if len(sentences) <= 1:
                    # Cannot split further
                    result.append(seg)
                else:
                    # Estimate time per sentence
                    time_per_char = duration / len(text) if len(text) > 0 else 0
                    current_time = seg['start']
                    
                    for sentence in sentences:
                        sentence_duration = len(sentence) * time_per_char
                        result.append({
                            'start': current_time,
                            'end': current_time + sentence_duration,
                            'text': sentence.strip(),
                            'id': seg['id']
                        })
                        current_time += sentence_duration
        
        return result
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        import re
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
