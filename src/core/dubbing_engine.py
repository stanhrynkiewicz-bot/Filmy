"""
Główny silnik dubbingu
Koordynuje proces transkrypcji, tłumaczenia, TTS i przetwarzania wideo
"""

import os
import shutil
from typing import List, Dict, Optional, Callable
from src.core.transcription import TranscriptionEngine
from src.core.translation import TranslationEngine
from src.core.tts import TTSEngine
from src.core.video_processor import VideoProcessor


class DubbingEngine:
    """Główny silnik koordynujący proces dubbingu"""
    
    def __init__(self, config: dict, progress_callback: Optional[Callable] = None):
        """Inicjalizacja silnika dubbingu
        
        Args:
            config: Konfiguracja aplikacji
            progress_callback: Funkcja callback do raportowania postępu
        """
        self.config = config
        self.progress_callback = progress_callback
        
        # Inicjalizacja komponentów
        self.transcription = TranscriptionEngine(
            model_size=config.get('whisper', {}).get('model_size', 'medium'),
            device=config.get('whisper', {}).get('device', 'cuda'),
            language=config.get('whisper', {}).get('language', 'en')
        )
        
        self.translation = TranslationEngine(
            source_lang=config.get('translation', {}).get('source_lang', 'en'),
            target_lang=config.get('translation', {}).get('target_lang', 'pl'),
            service=config.get('translation', {}).get('service', 'google')
        )
        
        self.tts = TTSEngine(
            model_name=config.get('tts', {}).get('model_name', 'tts_models/pl/mai_female/vits'),
            device=config.get('whisper', {}).get('device', 'cuda')
        )
        
        self.video_processor = VideoProcessor(
            silence_threshold=config.get('video', {}).get('silence_threshold', 0.4),
            add_keyframes=config.get('video', {}).get('add_keyframes', True)
        )
        
        # Katalogi robocze
        self.temp_dir = config.get('paths', {}).get('temp_dir', 'temp_segments')
        self.output_dir = config.get('paths', {}).get('output_dir', 'output')
        
    def report_progress(self, message: str, progress: float):
        """Raportuj postęp
        
        Args:
            message: Wiadomość o postępie
            progress: Procent ukończenia (0-100)
        """
        print(f"[{progress:.1f}%] {message}")
        if self.progress_callback:
            self.progress_callback(message, progress)
    
    def process_video(self, video_path: str, output_path: str, 
                     custom_dictionary: Dict[str, str] = None,
                     edited_translations: Dict[int, str] = None) -> bool:
        """Przetwórz wideo i dodaj dubbing
        
        Args:
            video_path: Ścieżka do wideo źródłowego
            output_path: Ścieżka do wideo wyjściowego
            custom_dictionary: Niestandardowy słownik tłumaczeń
            edited_translations: Edytowane tłumaczenia (indeks segmentu -> tekst)
            
        Returns:
            True jeśli sukces
        """
        try:
            # Przygotuj katalogi
            os.makedirs(self.temp_dir, exist_ok=True)
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Krok 1: Ekstrakcja audio (5%)
            self.report_progress("Ekstrakcja ścieżki audio...", 5)
            audio_path = os.path.join(self.temp_dir, "original_audio.wav")
            if not self.video_processor.extract_audio(video_path, audio_path):
                return False
            
            # Krok 2: Transkrypcja (20%)
            self.report_progress("Transkrypcja audio przy użyciu Whisper...", 10)
            transcription_result = self.transcription.transcribe_audio(audio_path)
            if not transcription_result:
                return False
            
            segments = self.transcription.get_segments(transcription_result)
            self.report_progress(f"Wykryto {len(segments)} segmentów", 20)
            
            # Krok 3: Optymalizacja segmentów
            self.report_progress("Optymalizacja segmentów...", 25)
            min_duration = self.config.get('video', {}).get('min_segment_duration', 1.0)
            max_duration = self.config.get('video', {}).get('max_segment_duration', 30.0)
            
            segments = self.transcription.merge_short_segments(segments, min_duration)
            segments = self.transcription.split_long_segments(segments, max_duration)
            
            # Krok 4: Tłumaczenie (40%)
            self.report_progress("Tłumaczenie tekstu...", 30)
            if custom_dictionary:
                self.translation.set_custom_dictionary(custom_dictionary)
            
            segments = self.translation.translate_segments(segments)
            
            # Zastosuj edytowane tłumaczenia
            if edited_translations:
                for idx, text in edited_translations.items():
                    if 0 <= idx < len(segments):
                        segments[idx]['translated_text'] = text
            
            self.report_progress("Tłumaczenie zakończone", 40)
            
            # Krok 5: Generowanie lektora TTS (60%)
            self.report_progress("Generowanie polskiego lektora...", 45)
            tts_dir = os.path.join(self.temp_dir, "tts_audio")
            segments = self.tts.generate_speech_batch(segments, tts_dir)
            self.report_progress("Generowanie lektora zakończone", 60)
            
            # Krok 6: Dodanie długości audio do segmentów
            for seg in segments:
                if seg.get('audio_path'):
                    seg['audio_duration'] = self.tts.get_audio_duration(seg['audio_path'])
            
            # Krok 7: Przetwarzanie segmentów wideo (80%)
            self.report_progress("Przetwarzanie segmentów wideo...", 65)
            processed_segments = self._process_video_segments(video_path, segments)
            
            if not processed_segments:
                return False
            
            self.report_progress("Segmenty wideo przetworzone", 80)
            
            # Krok 8: Łączenie segmentów (95%)
            self.report_progress("Łączenie finalnego wideo...", 85)
            if not self._combine_segments(processed_segments, output_path):
                return False
            
            # Krok 9: Czyszczenie
            self.report_progress("Finalizacja...", 95)
            self._cleanup_temp_files()
            
            self.report_progress("Dubbing zakończony!", 100)
            return True
            
        except Exception as e:
            print(f"Błąd podczas przetwarzania wideo: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _process_video_segments(self, video_path: str, segments: List[Dict]) -> List[Dict]:
        """Przetwórz segmenty wideo
        
        Args:
            video_path: Ścieżka do oryginalnego wideo
            segments: Lista segmentów z audio lektora
            
        Returns:
            Lista przetworzonych segmentów
        """
        processed = []
        segments_dir = os.path.join(self.temp_dir, "video_segments")
        os.makedirs(segments_dir, exist_ok=True)
        
        total_segments = len(segments)
        
        for i, seg in enumerate(segments):
            try:
                # Raportuj postęp
                progress = 65 + (i / total_segments) * 15
                self.report_progress(f"Przetwarzanie segmentu {i+1}/{total_segments}", progress)
                
                video_start = seg['start']
                video_end = seg['end']
                video_duration = video_end - video_start
                audio_path = seg.get('audio_path')
                audio_duration = seg.get('audio_duration', 0)
                
                if not audio_path or not audio_duration:
                    print(f"Segment {i} nie ma audio, pomijanie")
                    continue
                
                # Wytnij segment wideo
                segment_video_path = os.path.join(segments_dir, f"segment_{i:04d}_video.mp4")
                if not self.video_processor.create_video_segment(
                    video_path, video_start, video_end, segment_video_path
                ):
                    print(f"Błąd podczas tworzenia segmentu {i}")
                    continue
                
                # Dodaj klatki kluczowe jeśli włączone
                if self.config.get('video', {}).get('add_keyframes', True):
                    keyframe_path = os.path.join(segments_dir, f"segment_{i:04d}_keyframes.mp4")
                    if self.video_processor.add_keyframes_to_video(segment_video_path, keyframe_path):
                        segment_video_path = keyframe_path
                
                # Decyzja: dostosować tempo czy dodać ciszę
                if video_duration < audio_duration:
                    # Wideo krótsze - dostosuj tempo wideo
                    if self.config.get('video', {}).get('tempo_adjustment_enabled', True):
                        adjusted_path = os.path.join(segments_dir, f"segment_{i:04d}_adjusted.mp4")
                        if self.video_processor.adjust_video_tempo(
                            segment_video_path, audio_duration, adjusted_path
                        ):
                            segment_video_path = adjusted_path
                        
                        # Audio bez zmian
                        final_audio_path = audio_path
                    else:
                        # Bez dostosowania tempo - użyj oryginalnego
                        final_audio_path = audio_path
                else:
                    # Wideo dłuższe lub równe - dodaj ciszę do audio
                    padded_audio_path = os.path.join(segments_dir, f"segment_{i:04d}_padded_audio.wav")
                    if self.video_processor.pad_audio_with_silence(
                        audio_path, video_duration, padded_audio_path
                    ):
                        final_audio_path = padded_audio_path
                    else:
                        final_audio_path = audio_path
                
                # Połącz wideo z audio
                final_segment_path = os.path.join(segments_dir, f"segment_{i:04d}_final.mp4")
                if self.video_processor.combine_video_audio(
                    segment_video_path, final_audio_path, final_segment_path
                ):
                    processed.append({
                        'path': final_segment_path,
                        'index': i
                    })
                
            except Exception as e:
                print(f"Błąd podczas przetwarzania segmentu {i}: {e}")
                continue
        
        return processed
    
    def _combine_segments(self, segments: List[Dict], output_path: str) -> bool:
        """Połącz przetworzone segmenty w jeden film
        
        Args:
            segments: Lista przetworzonych segmentów
            output_path: Ścieżka wyjściowa
            
        Returns:
            True jeśli sukces
        """
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
            
            # Wczytaj wszystkie segmenty
            clips = []
            for seg in sorted(segments, key=lambda x: x['index']):
                clip = VideoFileClip(seg['path'])
                clips.append(clip)
            
            if not clips:
                print("Brak segmentów do połączenia")
                return False
            
            # Połącz segmenty
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Zapisz finalne wideo
            final_video.write_videofile(
                output_path,
                codec=self.config.get('output', {}).get('codec', 'libx264'),
                audio_codec=self.config.get('output', {}).get('audio_codec', 'aac'),
                bitrate=self.config.get('output', {}).get('bitrate', '5000k'),
                verbose=False,
                logger=None
            )
            
            # Zamknij wszystkie klipy
            final_video.close()
            for clip in clips:
                clip.close()
            
            print(f"Finalne wideo zapisane: {output_path}")
            return True
            
        except Exception as e:
            print(f"Błąd podczas łączenia segmentów: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _cleanup_temp_files(self):
        """Wyczyść pliki tymczasowe"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir, exist_ok=True)
        except Exception as e:
            print(f"Błąd podczas czyszczenia plików tymczasowych: {e}")
    
    def get_transcription_preview(self, video_path: str) -> Optional[List[Dict]]:
        """Pobierz podgląd transkrypcji bez pełnego przetwarzania
        
        Args:
            video_path: Ścieżka do wideo
            
        Returns:
            Lista segmentów z transkrypcją
        """
        try:
            # Ekstrakcja audio
            audio_path = os.path.join(self.temp_dir, "preview_audio.wav")
            if not self.video_processor.extract_audio(video_path, audio_path):
                return None
            
            # Transkrypcja
            transcription_result = self.transcription.transcribe_audio(audio_path)
            if not transcription_result:
                return None
            
            segments = self.transcription.get_segments(transcription_result)
            
            # Optymalizacja
            min_duration = self.config.get('video', {}).get('min_segment_duration', 1.0)
            max_duration = self.config.get('video', {}).get('max_segment_duration', 30.0)
            segments = self.transcription.merge_short_segments(segments, min_duration)
            segments = self.transcription.split_long_segments(segments, max_duration)
            
            return segments
            
        except Exception as e:
            print(f"Błąd podczas podglądu transkrypcji: {e}")
            return None
