"""
Translation Module
Handles text translation with custom dictionary support
"""

from typing import Dict, List
from deep_translator import GoogleTranslator
import re


class TranslationEngine:
    """Handles text translation with custom dictionary"""
    
    def __init__(self, source_lang: str = "en", target_lang: str = "pl", service: str = "google"):
        """Initialize translation engine
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            service: Translation service to use
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.service = service
        self.custom_dictionary = {}
        
        # Initialize translator
        if service == "google":
            self.translator = GoogleTranslator(source=source_lang, target=target_lang)
        else:
            raise ValueError(f"Unsupported translation service: {service}")
    
    def set_custom_dictionary(self, dictionary: Dict[str, str]):
        """Set custom translation dictionary
        
        Args:
            dictionary: Dictionary mapping source terms to target terms
        """
        self.custom_dictionary = dictionary
    
    def translate_text(self, text: str) -> str:
        """Translate text with custom dictionary support
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text.strip():
            return text
        
        # Apply custom dictionary
        text_with_dict = self._apply_dictionary(text)
        
        try:
            # Translate
            translated = self.translator.translate(text_with_dict)
            return translated
        except Exception as e:
            print(f"Error translating text: {e}")
            return text
    
    def translate_segments(self, segments: List[Dict]) -> List[Dict]:
        """Translate multiple segments
        
        Args:
            segments: List of segment dictionaries with 'text' field
            
        Returns:
            List of segments with added 'translated_text' field
        """
        translated_segments = []
        
        for seg in segments:
            translated_seg = seg.copy()
            translated_seg['translated_text'] = self.translate_text(seg['text'])
            translated_segments.append(translated_seg)
        
        return translated_segments
    
    def _apply_dictionary(self, text: str) -> str:
        """Apply custom dictionary to text
        
        Args:
            text: Original text
            
        Returns:
            Text with dictionary terms applied
        """
        if not self.custom_dictionary:
            return text
        
        # Create a pattern that matches whole words
        result = text
        for source_term, target_term in self.custom_dictionary.items():
            # Case-insensitive replacement of whole words
            pattern = r'\b' + re.escape(source_term) + r'\b'
            result = re.sub(pattern, target_term, result, flags=re.IGNORECASE)
        
        return result
    
    def batch_translate(self, texts: List[str]) -> List[str]:
        """Translate multiple texts
        
        Args:
            texts: List of texts to translate
            
        Returns:
            List of translated texts
        """
        return [self.translate_text(text) for text in texts]
