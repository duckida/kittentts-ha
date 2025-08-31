"""TTS platform for KittenTTS."""
import asyncio
import io
import logging
import voluptuous as vol
from typing import Any

from homeassistant.components.tts import (
    PLATFORM_SCHEMA,
    Provider,
    TtsAudioType,
    Voice,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_VOICE, CONF_MODEL

_LOGGER = logging.getLogger(__name__)

DEFAULT_LANG = "en"
DEFAULT_VOICE = "expr-voice-2-f"
DEFAULT_MODEL = "KittenML/kitten-tts-nano-0.2"

# Available voices in KittenTTS
VOICES = [
    'expr-voice-2-m', 'expr-voice-2-f', 
    'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f',
    'expr-voice-5-m', 'expr-voice-5-f'
]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(VOICES),
        vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): cv.string,
    }
)

async def async_get_engine(
    hass: HomeAssistant, config: ConfigType, discovery_info=None
) -> Provider:
    """Set up KittenTTS TTS component."""
    # For config flow based integrations, we get config from hass.data
    if DOMAIN in hass.data:
        conf = hass.data[DOMAIN]
    else:
        # Fallback for YAML configuration
        conf = config
    
    voice = conf.get(CONF_VOICE, DEFAULT_VOICE)
    model = conf.get(CONF_MODEL, DEFAULT_MODEL)
    
    return KittenTTSProvider(hass, voice, model)


class KittenTTSProvider(Provider):
    """KittenTTS TTS provider."""

    def __init__(self, hass: HomeAssistant, voice: str, model: str) -> None:
        """Initialize the provider."""
        self.hass = hass
        self._voice = voice
        self._model = model
        self.name = "KittenTTS"
        
        # Import KittenTTS here to avoid issues if the component is not used
        self._kittentts = None
        self._check_kittentts_availability()

    def _check_kittentts_availability(self):
        """Check if KittenTTS is available and import it."""
        try:
            import kittentts
            self._kittentts = kittentts.KittenTTS(self._model)
            _LOGGER.info("KittenTTS successfully initialized with model: %s", self._model)
        except ImportError as e:
            _LOGGER.warning("KittenTTS is not available or not compatible with your system. "
                          "Please check the KittenTTS documentation for Python 3.13 compatibility. "
                          "You may need to manually install KittenTTS in your Home Assistant environment. "
                          "Error: %s", e)
        except Exception as e:
            _LOGGER.error("Error initializing KittenTTS: %s", e)
            self._kittentts = None

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return DEFAULT_LANG

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return [DEFAULT_LANG]

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return [CONF_VOICE]

    @property
    def default_options(self) -> dict[str, Any]:
        """Return a dict including default options."""
        return {CONF_VOICE: self._voice}

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS audio."""
        # Try to import KittenTTS if not already imported
        if self._kittentts is None:
            self._check_kittentts_availability()
            
        if self._kittentts is None:
            _LOGGER.error("KittenTTS is not available. Please ensure it is properly installed "
                         "and compatible with your Home Assistant environment.")
            return None
            
        try:
            # Get the voice from options or use default
            voice = options.get(CONF_VOICE, self._voice) if options else self._voice
            
            # Generate audio using KittenTTS
            audio_data = self._kittentts.generate(message, voice=voice)
            
            # Convert to WAV format using soundfile
            import soundfile as sf
            buf = io.BytesIO()
            sf.write(buf, audio_data, 24000, format='WAV')
            buf.seek(0)
            
            return ("wav", buf.read())
        except Exception as e:
            _LOGGER.error("Error generating speech with KittenTTS: %s", e)
            return None