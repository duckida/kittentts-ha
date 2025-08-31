# KittenTTS for Home Assistant

This custom integration brings [KittenTTS](https://github.com/KittenML/KittenTTS) to Home Assistant, allowing you to generate high-quality speech from text directly within your smart home.

## About KittenTTS

KittenTTS is an ultra-lightweight (under 25MB) text-to-speech model with only 15 million parameters. It's designed for high-quality voice synthesis while maintaining a small footprint and runs without requiring a GPU.

## Installation

1. Install the KittenTTS package:
   ```
   pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   ```

2. Copy the `kittentts` folder to your Home Assistant's `custom_components` directory:
   ```
   <config_dir>/custom_components/kittentts/
   ```

3. Restart Home Assistant

## Configuration

Add the following to your `configuration.yaml` file:

```yaml
tts:
  - platform: kittentts
    language: "en"
    voice: "expr-voice-2-f"  # Optional, see available voices below
    model: "KittenML/kitten-tts-nano-0.2"  # Optional
```

### Available Voices

- `expr-voice-2-m` - Male voice 2
- `expr-voice-2-f` - Female voice 2 (default)
- `expr-voice-3-m` - Male voice 3
- `expr-voice-3-f` - Female voice 3
- `expr-voice-4-m` - Male voice 4
- `expr-voice-4-f` - Female voice 4
- `expr-voice-5-m` - Male voice 5
- `expr-voice-5-f` - Female voice 5

## Usage

Once configured, you can use the TTS service in automations or scripts:

```yaml
service: tts.speak
data:
  entity_id: tts.kittentts
  message: "Hello from KittenTTS!"
  cache: true
```

Or with a specific voice:

```yaml
service: tts.speak
data:
  entity_id: tts.kittentts
  message: "Hello from KittenTTS!"
  options:
    voice: "expr-voice-3-m"
  cache: true
```

## Requirements

- Home Assistant 2023.5 or newer
- KittenTTS package
- soundfile package

These will be automatically installed if specified in the manifest.

## Author

Created by [duckida](https://github.com/duckida)

Repository: [https://github.com/duckida/kittentts-ha](https://github.com/duckida/kittentts-ha)