"""KittenTTS text-to-speech provider."""
import io
import logging
import voluptuous as vol
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_VOICE = "voice"
CONF_MODEL = "model"

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
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): cv.string,
        vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(VOICES),
        vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): cv.string,
    }
)

async def async_get_engine(hass: HomeAssistant, config: ConfigType, discovery_info=None):
    """Set up KittenTTS speech component."""
    # If set up via config entry, use those options
    if discovery_info is not None:
        config = discovery_info
    
    lang = config.get(CONF_LANG, DEFAULT_LANG)
    voice = config.get(CONF_VOICE, DEFAULT_VOICE)
    model = config.get(CONF_MODEL, DEFAULT_MODEL)
    
    return KittenTTSProvider(lang, voice, model)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up KittenTTS from a config entry."""
    lang = config_entry.options.get(CONF_LANG, config_entry.data.get(CONF_LANG, DEFAULT_LANG))
    voice = config_entry.options.get(CONF_VOICE, config_entry.data.get(CONF_VOICE, DEFAULT_VOICE))
    model = config_entry.options.get(CONF_MODEL, config_entry.data.get(CONF_MODEL, DEFAULT_MODEL))
    
    async_add_entities([KittenTTSProvider(lang, voice, model)])


class KittenTTSProvider(Provider):
    """The KittenTTS API provider."""

    def __init__(self, lang: str, voice: str, model: str) -> None:
        """Initialize the provider."""
        self._lang = lang
        self._voice = voice
        self._model = model
        self.name = "KittenTTS"
        
        # Import KittenTTS here to avoid issues if the component is not used
        try:
            from kittentts import KittenTTS
            self._kittentts = KittenTTS(model)
        except ImportError as e:
            _LOGGER.warning("KittenTTS is not installed or not compatible with your system. "
                          "Please check the KittenTTS documentation for Python 3.13 compatibility. "
                          "Error: %s", e)
            self._kittentts = None
        except Exception as e:
            _LOGGER.error("Error initializing KittenTTS: %s", e)
            self._kittentts = None

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return [self._lang]

    @property
    def supported_options(self):
        """Return list of supported options."""
        return [CONF_VOICE]

    @property
    def default_options(self):
        """Return a dict including default options."""
        return {CONF_VOICE: self._voice}

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS audio."""
        if self._kittentts is None:
            _LOGGER.error("KittenTTS is not available. Please ensure it is properly installed "
                         "and compatible with your system.")
            return (None, None)
            
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
            
            return ("audio/wav", buf.read())
        except Exception as e:
            _LOGGER.error("Error generating speech with KittenTTS: %s", e)
            return (None, None)