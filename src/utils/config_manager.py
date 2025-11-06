"""
Configuration Manager
Handles loading and saving application configuration
"""

import os
import yaml
import json
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG_PATH = "config.yaml"
    DEFAULT_TEMPLATE_PATH = "config.yaml.template"
    
    def __init__(self, config_path: str = None):
        """Initialize configuration manager
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        # If config doesn't exist, create from template
        if not os.path.exists(self.config_path):
            if os.path.exists(self.DEFAULT_TEMPLATE_PATH):
                with open(self.DEFAULT_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                    template = f.read()
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    f.write(template)
        
        # Load config
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config or {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def save_config(self) -> bool:
        """Save current configuration to file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'whisper.model_size')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            'whisper': {
                'model_size': 'medium',
                'device': 'cuda',
                'language': 'en'
            },
            'translation': {
                'source_lang': 'en',
                'target_lang': 'pl',
                'service': 'google'
            },
            'tts': {
                'model_name': 'tts_models/pl/mai_female/vits',
                'speaker': None,
                'language': 'pl'
            },
            'video': {
                'silence_threshold': 0.4,
                'min_segment_duration': 1.0,
                'max_segment_duration': 30.0,
                'tempo_adjustment_enabled': True,
                'add_keyframes': True
            },
            'audio': {
                'sample_rate': 16000,
                'silence_threshold_db': -40
            },
            'output': {
                'format': 'mp4',
                'codec': 'libx264',
                'audio_codec': 'aac',
                'bitrate': '5000k'
            },
            'paths': {
                'temp_dir': 'temp_segments',
                'output_dir': 'output',
                'cache_dir': 'cache',
                'models_dir': 'models',
                'dictionary_file': 'custom_dictionary.json'
            }
        }
    
    def load_custom_dictionary(self) -> Dict[str, str]:
        """Load custom translation dictionary
        
        Returns:
            Dictionary mapping terms
        """
        dict_path = self.get('paths.dictionary_file', 'custom_dictionary.json')
        if os.path.exists(dict_path):
            try:
                with open(dict_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Flatten nested structure
                result = {}
                for category in data.values():
                    if isinstance(category, dict):
                        result.update(category)
                return result
            except Exception as e:
                print(f"Error loading dictionary: {e}")
        return {}
    
    def save_custom_dictionary(self, dictionary: Dict[str, str]) -> bool:
        """Save custom translation dictionary
        
        Args:
            dictionary: Dictionary to save
            
        Returns:
            True if successful
        """
        dict_path = self.get('paths.dictionary_file', 'custom_dictionary.json')
        try:
            # Structure dictionary by category
            structured = {'trading_terms': dictionary}
            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(structured, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving dictionary: {e}")
            return False
