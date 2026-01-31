# Audio Visualization Examples

This directory contains examples demonstrating different use cases of the audio visualization system.

## Example 1: Real-time Microphone Visualization

The main binary (`cargo run --release`) captures audio from your default microphone and visualizes it in real-time.

```bash
cd audio_viz
cargo run --release
```

Features demonstrated:
- Real-time audio capture from microphone
- FFT-based frequency analysis
- Beat detection
- Dynamic shader-based visualization

## Example 2: Using the Audio Analyzer (Code Example)

```rust
use audio_analyzer::AudioAnalyzer;

// Create analyzer with sample rate and FFT size
let mut analyzer = AudioAnalyzer::new(44100, 2048);

// Process audio samples
let samples: Vec<f32> = get_audio_samples(); // Your audio source
let bands = analyzer.process_samples(&samples);

// Access frequency bands
println!("Bass: {}", bands.bass);
println!("Mid: {}", bands.mid);
println!("High: {}", bands.high);

// Check for beat
if analyzer.is_beat() {
    println!("Beat detected! Intensity: {}", analyzer.get_beat_intensity());
}
```

## Example 3: Custom Shader Integration

To create your own visual effects:

1. Copy `shaders/music_viz.wgsl` to create your own shader
2. Modify the fragment shader function to create custom effects
3. Update `renderer.rs` to load your shader:

```rust
let shader_source = include_str!("../shaders/my_custom_shader.wgsl");
```

## Technical Notes

### Frequency Bands
- **Bass**: 20-250 Hz - Deep, low-frequency sounds (kick drums, bass guitar)
- **Mid**: 250-2000 Hz - Main melodic content (vocals, most instruments)
- **High**: 2000-20000 Hz - Bright sounds (cymbals, hi-hats, high harmonics)

### Beat Detection
The beat detector uses an energy-based algorithm:
1. Tracks history of bass energy
2. Calculates threshold based on mean + 1.5 * standard deviation
3. Triggers beat when energy exceeds threshold
4. Implements 200ms cooldown to prevent double-detections

### Performance Tips
- Use `--release` build for optimal performance (60+ FPS)
- Adjust FFT size to balance frequency resolution vs latency
- Lower window size for faster response, higher for better frequency detail
- System should maintain <10ms audio latency for smooth visualization

## Troubleshooting

### No audio device found
Ensure you have a microphone connected and accessible by the system.

### Poor performance
- Build with `--release` flag
- Close other GPU-intensive applications
- Check GPU drivers are up to date

### No beat detection
- Increase audio volume
- Play music with clear bass/kick drum
- Adjust threshold in `audio_analyzer.rs` if needed
