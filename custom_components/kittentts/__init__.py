"""KittenTTS integration for Home Assistant."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry

DOMAIN = "kittentts"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the KittenTTS component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up KittenTTS from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["tts"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["tts"])