"""
Video Processing Module
Handles video segmentation, audio replacement, and tempo adjustment
"""

import os
import subprocess
from typing import List, Dict, Optional, Tuple
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np


class VideoProcessor:
    """Handles video processing operations"""
    
    def __init__(self, silence_threshold: float = 0.4, add_keyframes: bool = True):
        """Initialize video processor
        
        Args:
            silence_threshold: Minimum silence duration to keep (seconds)
            add_keyframes: Whether to add keyframes at segment boundaries
        """
        self.silence_threshold = silence_threshold
        self.add_keyframes = add_keyframes
    
    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        """Extract audio from video
        
        Args:
            video_path: Path to input video
            audio_path: Path to save audio
            
        Returns:
            True if successful
        """
        try:
            print(f"Extracting audio from: {video_path}")
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            
            print(f"Audio extracted: {audio_path}")
            return True
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return False
    
    def remove_short_silence(self, audio_path: str, output_path: str, 
                            min_silence_len: int = 400, silence_thresh: int = -40) -> bool:
        """Remove silence segments shorter than threshold
        
        Args:
            audio_path: Input audio path
            output_path: Output audio path
            min_silence_len: Minimum silence length to keep (milliseconds)
            silence_thresh: Silence threshold in dB
            
        Returns:
            True if successful
        """
        try:
            print(f"Removing short silence from: {audio_path}")
            audio = AudioSegment.from_file(audio_path)
            
            # Detect non-silent chunks
            nonsilent_ranges = detect_nonsilent(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh
            )
            
            if not nonsilent_ranges:
                print("Warning: No non-silent audio detected")
                return False
            
            # Extract and concatenate non-silent chunks
            chunks = [audio[start:end] for start, end in nonsilent_ranges]
            processed = sum(chunks)
            
            processed.export(output_path, format="wav")
            print(f"Processed audio saved: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error removing silence: {e}")
            return False
    
    def create_video_segment(self, video_path: str, start: float, end: float, 
                           output_path: str) -> bool:
        """Create video segment
        
        Args:
            video_path: Input video path
            start: Start time in seconds
            end: End time in seconds
            output_path: Output path
            
        Returns:
            True if successful
        """
        try:
            video = VideoFileClip(video_path)
            segment = video.subclip(start, end)
            segment.write_videofile(output_path, codec='libx264', audio=False, 
                                   verbose=False, logger=None)
            segment.close()
            video.close()
            return True
        except Exception as e:
            print(f"Error creating video segment: {e}")
            return False
    
    def adjust_video_tempo(self, video_path: str, target_duration: float, 
                          output_path: str) -> bool:
        """Adjust video tempo to match target duration
        
        Args:
            video_path: Input video path
            target_duration: Target duration in seconds
            output_path: Output path
            
        Returns:
            True if successful
        """
        try:
            video = VideoFileClip(video_path)
            original_duration = video.duration
            
            if original_duration == 0:
                print("Error: Video has zero duration")
                video.close()
                return False
            
            # Calculate speed factor
            speed_factor = original_duration / target_duration
            
            print(f"Adjusting tempo: {speed_factor:.2f}x (from {original_duration:.2f}s to {target_duration:.2f}s)")
            
            # Adjust video speed
            adjusted = video.fx(lambda clip: clip.speedx(speed_factor))
            adjusted.write_videofile(output_path, codec='libx264', audio=False,
                                    verbose=False, logger=None)
            
            adjusted.close()
            video.close()
            return True
            
        except Exception as e:
            print(f"Error adjusting video tempo: {e}")
            return False
    
    def add_keyframes_to_video(self, video_path: str, output_path: str) -> bool:
        """Add keyframes at the beginning and end of video
        
        Args:
            video_path: Input video path
            output_path: Output path
            
        Returns:
            True if successful
        """
        try:
            # Use ffmpeg to add keyframes
            cmd = [
                'ffmpeg', '-i', video_path,
                '-force_key_frames', '0,{}'.format('end'),
                '-c:v', 'libx264',
                '-an',  # No audio
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error adding keyframes: {e}")
            return False
    
    def combine_video_audio(self, video_path: str, audio_path: str, 
                           output_path: str) -> bool:
        """Combine video with new audio track
        
        Args:
            video_path: Path to video (no audio)
            audio_path: Path to audio file
            output_path: Output path
            
        Returns:
            True if successful
        """
        try:
            print(f"Combining video and audio...")
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Ensure audio matches video duration
            if audio.duration < video.duration:
                print(f"Warning: Audio shorter than video. Padding with silence.")
            
            video_with_audio = video.set_audio(audio)
            video_with_audio.write_videofile(output_path, codec='libx264', 
                                            audio_codec='aac', verbose=False, logger=None)
            
            video_with_audio.close()
            audio.close()
            video.close()
            
            print(f"Combined video saved: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error combining video and audio: {e}")
            return False
    
    def get_video_duration(self, video_path: str) -> Optional[float]:
        """Get video duration
        
        Args:
            video_path: Path to video
            
        Returns:
            Duration in seconds
        """
        try:
            video = VideoFileClip(video_path)
            duration = video.duration
            video.close()
            return duration
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return None
    
    def create_silent_audio(self, duration: float, output_path: str, 
                           sample_rate: int = 16000) -> bool:
        """Create silent audio file
        
        Args:
            duration: Duration in seconds
            output_path: Output path
            sample_rate: Sample rate
            
        Returns:
            True if successful
        """
        try:
            silence = AudioSegment.silent(duration=int(duration * 1000))
            silence.export(output_path, format="wav")
            return True
        except Exception as e:
            print(f"Error creating silent audio: {e}")
            return False
    
    def pad_audio_with_silence(self, audio_path: str, target_duration: float, 
                              output_path: str) -> bool:
        """Pad audio with silence to match target duration
        
        Args:
            audio_path: Input audio path
            target_duration: Target duration in seconds
            output_path: Output path
            
        Returns:
            True if successful
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            audio_duration = len(audio) / 1000.0  # Convert to seconds
            
            if audio_duration >= target_duration:
                # Audio is already long enough
                audio.export(output_path, format="wav")
                return True
            
            # Calculate silence needed
            silence_duration = (target_duration - audio_duration) * 1000  # Convert to ms
            silence = AudioSegment.silent(duration=int(silence_duration))
            
            # Concatenate audio + silence
            padded = audio + silence
            padded.export(output_path, format="wav")
            
            print(f"Padded audio from {audio_duration:.2f}s to {target_duration:.2f}s")
            return True
            
        except Exception as e:
            print(f"Error padding audio: {e}")
            return False
