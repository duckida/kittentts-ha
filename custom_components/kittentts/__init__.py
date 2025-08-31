"""KittenTTS integration for Home Assistant."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "kittentts"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the KittenTTS component."""
    return True