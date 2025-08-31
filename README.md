# KittenTTS for Home Assistant

This custom integration brings [KittenTTS](https://github.com/KittenML/KittenTTS) to Home Assistant, allowing you to generate high-quality speech from text directly within your smart home.

## About KittenTTS

KittenTTS is an ultra-lightweight (under 25MB) text-to-speech model with only 15 million parameters. It's designed for high-quality voice synthesis while maintaining a small footprint and runs without requiring a GPU.

## Installation

### For Home Assistant OS / Supervised / Container Users

1. Add this repository to HACS:
   - Go to HACS → Integrations
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add `https://github.com/duckida/kittentts-ha` as a custom repository with category "Integration"
   - Click "Explore & Download Repositories"
   - Find "KittenTTS" and click "Download"

2. Restart Home Assistant

3. Add the integration:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "KittenTTS" and select it
   - Follow the configuration steps

### For Advanced Users (Manual Installation)

1. Copy the `kittentts` folder to your Home Assistant's `custom_components` directory:
   ```
   <config_dir>/custom_components/kittentts/
   ```

2. Restart Home Assistant

3. Add the integration via the UI (Settings → Devices & Services → Add Integration → KittenTTS)

## Configuration

Configuration is done through the UI during the integration setup. You can configure:

- Language (default: "en")
- Voice (default: "expr-voice-2-f")
- Model (default: "KittenML/kitten-tts-nano-0.2")

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

## Troubleshooting

### Python 3.13 Compatibility

Home Assistant uses Python 3.13, which may cause compatibility issues with some of KittenTTS's dependencies. The integration includes compatible versions of dependencies in the manifest, but if you encounter issues:

1. Check the Home Assistant logs for specific error messages
2. Ensure you're using the latest version of this integration
3. If problems persist, please open an issue on the GitHub repository

### Alternative Installation Method

If the automatic dependency installation fails, you can try manually installing the KittenTTS wheel:

1. Download the wheel file:
   ```
   https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   ```

2. For Home Assistant Container users, you can install it directly in the container:
   ```
   docker exec -it homeassistant pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   ```

3. For Home Assistant OS users, this method is not recommended as it requires accessing the underlying OS.

### Common Error Messages

- `kittentts is not available`: This indicates that KittenTTS could not be imported. Check the Home Assistant logs for more details.
- Dependency resolution errors: These are handled by Home Assistant's package management system.

## Requirements

The integration automatically installs the following dependencies:
- soundfile==0.12.1
- numpy>=1.26.0
- spacy>=3.8.0
- phonemizer>=3.2.0

## Author

Created by [duckida](https://github.com/duckida)

Repository: [https://github.com/duckida/kittentts-ha](https://github.com/duckida/kittentts-ha)