"""Config flow for KittenTTS."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback

from .const import DOMAIN, CONF_VOICE, CONF_MODEL

# Available voices in KittenTTS
VOICES = [
    'expr-voice-2-m', 'expr-voice-2-f', 
    'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f',
    'expr-voice-5-m', 'expr-voice-5-f'
]

DEFAULT_VOICE = "expr-voice-2-f"
DEFAULT_MODEL = "KittenML/kitten-tts-nano-0.2"

class KittenTTSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for KittenTTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="KittenTTS", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(VOICES),
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KittenTTSOptionsFlowHandler(config_entry)


class KittenTTSOptionsFlowHandler(OptionsFlow):
    """Handle KittenTTS options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        
        voice = self.config_entry.options.get(CONF_VOICE, self.config_entry.data.get(CONF_VOICE, DEFAULT_VOICE))
        model = self.config_entry.options.get(CONF_MODEL, self.config_entry.data.get(CONF_MODEL, DEFAULT_MODEL))
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_VOICE, default=voice): vol.In(VOICES),
                    vol.Optional(CONF_MODEL, default=model): str,
                }
            )
        )