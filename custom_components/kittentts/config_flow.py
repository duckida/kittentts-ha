"""Config flow for KittenTTS."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN

# Available voices in KittenTTS
VOICES = [
    'expr-voice-2-m', 'expr-voice-2-f', 
    'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f',
    'expr-voice-5-m', 'expr-voice-5-f'
]

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
                    vol.Optional("language", default="en"): str,
                    vol.Optional("voice", default="expr-voice-2-f"): vol.In(VOICES),
                    vol.Optional("model", default="KittenML/kitten-tts-nano-0.2"): str,
                }
            ),
        )