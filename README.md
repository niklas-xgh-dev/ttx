# TTX: Text-to-Anything

A technical implementation for converting textual content into multiple output modalities using OpenAI's APIs.

## Technical Overview

TTX (Text-to-Anything) implements a multi-modal content generation system that transforms input text into both audio narrations and visual assets. The system leverages OpenAI's APIs with optimized parameter configurations for high-quality output across different media types.

## Architectural Components

```mermaid
graph TD
    A[Input Text] --> B[Content Parser]
    B --> |Structured Data| C[Content Formatter]
    
    C --> |Audio Text| D1[TTS Preprocessor]
    C --> |Image Prompt| D2[TTI Preprocessor]
    
    D1 --> |Optimized Text| E1[OpenAI TTS API]
    D2 --> |Engineered Prompt| E2[OpenAI TTI API]
    
    E1 --> |Audio Stream| F1[MP3 Encoder]
    E2 --> |Image Data| F2[Image Processor]
    
    F1 --> G1[Audio Output]
    F2 --> G2[Image Output]
    
    H[Environment Configuration] --> |API Keys| C
    H --> |TTS Parameters| E1
    H --> |TTI Parameters| E2
    
    subgraph "Audio Pipeline"
    D1
    E1
    F1
    end
    
    subgraph "Image Pipeline"
    D2
    E2
    F2
    end
    
    style D1 fill:#f96,stroke:#333,stroke-width:2px
    style E1 fill:#f96,stroke:#333,stroke-width:2px
    style F1 fill:#f96,stroke:#333,stroke-width:2px
    style D2 fill:#bbf,stroke:#33a,stroke-width:2px
    style E2 fill:#bbf,stroke:#33a,stroke-width:2px
    style F2 fill:#bbf,stroke:#33a,stroke-width:2px
```

## OpenAI SDK Integration

### Text-to-Speech (TTS) Implementation

```python
with client.audio.speech.with_streaming_response.create(
    model = os.getenv("TTS_MODEL"),
    voice = os.getenv("TTS_VOICE"),
    speed = float(os.getenv("TTS_SPEED")),
    input = formatted_text,
    instructions = os.getenv("TTS_INSTRUCTIONS"),
) as stream_response:
    stream_response.stream_to_file(audio_output_path)
```

### Text-to-Image (TTI) Implementation

```python
response = client.images.generate(
    model = os.getenv("IMAGE_MODEL"),
    prompt = formatted_prompt,
    n = 1,
    size = os.getenv("IMAGE_SIZE"),
    quality = os.getenv("IMAGE_QUALITY"),
    response_format = os.getenv("IMAGE_FORMAT"),
    style = os.getenv("IMAGE_STYLE"),
)

# Process image data based on response format
image_data = response.data[0]
if hasattr(image_data, 'url') and image_data.url:
    # Download and save image from URL
    img_response = requests.get(image_data.url)
    with open(image_output_path, "wb") as img_file:
        img_file.write(img_response.content)
elif hasattr(image_data, 'b64_json') and image_data.b64_json:
    # Decode and save base64 data
    img_data = base64.b64decode(image_data.b64_json)
    with open(image_output_path, "wb") as img_file:
        img_file.write(img_data)
```

## API Parameters

### TTS Parameters (Audio Generation)

| Parameter | Type | Description | Typical Values |
|-----------|------|-------------|----------------|
| `model` | string | TTS model identifier | "gpt-4o-mini-tts" |
| `voice` | string | Base voice profile | "ash", "nova", "echo" |
| `speed` | float | Playback rate modifier | 1.0 (normal), 2.0-2.2 (fast) |
| `input` | string | Source text for narration | Formatted input text |
| `instructions` | string | Voice customization directives | Structured voice parameters |

### TTI Parameters (Image Generation)

| Parameter | Type | Description | Typical Values |
|-----------|------|-------------|----------------|
| `model` | string | Image model identifier | "dall-e-3" |
| `prompt` | string | Image generation prompt | Formatted visual prompt |
| `n` | integer | Number of images to generate | 1 (for dall-e-3) |
| `size` | string | Image dimensions | "1024x1024", "1792x1024", "1024x1792" |
| `quality` | string | Image fidelity setting | "standard", "hd" |
| `response_format` | string | Return data format | "url", "b64_json" |
| `style` | string | Aesthetic style | "vivid", "natural" |

## Protocol Implementation Notes

### TTS Pipeline Technical Details

- Uses streaming response pattern for efficient memory usage
- Implements chunked data handling for progressive file generation
- MP3 output with 24kHz sampling rate and variable bitrate (~48 kbps)
- Supports customized voice parameters for specialized content delivery

### TTI Pipeline Technical Details

- Non-streaming synchronous request/response pattern
- Two-stage processing for URL responses (fetch and save)
- Single-stage for base64 responses (decode and save)
- PNG output with dimensions based on vertical/horizontal content needs
- Vertical formats (1024x1792) optimized for social media platforms

## Parameter Engineering

### Voice Parameter Format

```
Personality/affect: Technical authority with analytical precision
Voice: Medium-deep, clear articulation, precise diction
Tone: Matter-of-fact, technically engaged, micro-variations for emphasis
Dialect: Technical vernacular with standardized pronunciation
Pronunciation: Careful enunciation of technical terms
Features: Consistent pacing with micro-pauses between sections
```

### Image Prompt Engineering

Image prompts follow a structured format with:
- Subject specification with clear visual attributes
- Composition instructions for aspect ratio optimization
- Style directives for visual consistency
- Background and foreground element specification
- Format-specific optimizations (vertical/horizontal)

## Configuration Reference

```
# TTS Configuration
TTS_MODEL=gpt-4o-mini-tts
TTS_VOICE=ash
TTS_SPEED=2.2
TTS_INSTRUCTIONS="Personality/affect: Technical authority with analytical precision. Voice: Medium-deep, clear articulation, precise diction. Tone: Matter-of-fact, technically engaged, micro-variations for emphasis. Dialect: Technical vernacular with standardized pronunciation. Pronunciation: Careful enunciation of technical terms. Features: Consistent pacing with micro-pauses between logical sections."

# TTI Configuration
IMAGE_MODEL=dall-e-3
IMAGE_SIZE=1024x1792
IMAGE_QUALITY=standard
IMAGE_FORMAT=url
IMAGE_STYLE=vivid
```

## License

MIT