# Audio Visualization Module - Main Documentation

## Overview

The audio visualization module (`audio_viz/`) is a standalone music visualization system that creates real-time, dynamic shader-based animations synchronized with audio input. This module is separate from the main Turkish NLP toolkit and can be built and run independently.

## Quick Start

```bash
# Build and run the visualization
cd audio_viz
cargo run --release
```

The application will open a window and start visualizing audio from your default microphone. Press ESC to exit.

## System Requirements

- **Rust**: 1.70 or later
- **Graphics**: GPU with Vulkan, Metal, or DirectX 12 support
- **Audio**: Microphone or audio input device (optional)
- **OS**: Linux, macOS, or Windows

## Features

### Audio Analysis
- **FFT-based frequency analysis**: Separates audio into bass (20-250 Hz), mid (250-2000 Hz), and high (2000-20000 Hz) frequency bands
- **Beat detection**: Real-time beat detection with intensity tracking using energy-based algorithm
- **Low-latency processing**: Optimized for <10ms latency

### Visual Effects
The shader dynamically responds to different audio characteristics:
- **Bass pulse**: Pulsing circular effects responding to bass frequencies
- **Mid-frequency waves**: Animated wave patterns for mid-range frequencies
- **High-frequency sparkles**: Sparkle effects for high frequencies
- **Orbital patterns**: Smooth orbital movements triggered by melodic content
- **Beat flash**: Visual flash effects synchronized with detected beats
- **Energy-reactive background**: Background gradient that responds to overall audio energy

## Architecture

```
audio_viz/
├── src/
│   ├── main.rs              # Application entry point
│   ├── audio_analyzer.rs    # FFT and frequency analysis
│   ├── audio_input.rs       # Audio capture from microphone
│   └── renderer.rs          # WGPU rendering and shader management
├── shaders/
│   └── music_viz.wgsl       # WGSL fragment shader
├── Cargo.toml               # Dependencies and build config
├── README.md                # Detailed technical documentation
└── EXAMPLES.md              # Usage examples and tutorials
```

## Technical Details

### Audio Processing Pipeline
1. **Capture**: Audio samples captured from microphone at 44.1 kHz
2. **Windowing**: Hann window applied to reduce spectral leakage
3. **FFT**: 2048-point FFT computes frequency spectrum
4. **Band Extraction**: Frequency bins grouped into bass, mid, and high bands
5. **Beat Detection**: Energy-based algorithm detects beats with 200ms cooldown
6. **Visualization**: Audio data sent to GPU shader as uniform buffer

### Rendering Pipeline
- **API**: WGPU (cross-platform abstraction over Vulkan, Metal, DirectX 12)
- **Shader**: WGSL fragment shader running at 60+ FPS
- **Performance**: GPU-accelerated with minimal CPU overhead

### Beat Detection Algorithm
1. Maintains 1-second history of bass energy values
2. Calculates mean and standard deviation
3. Triggers beat when energy exceeds threshold (mean + 1.5 × std dev)
4. Implements 200ms cooldown to prevent duplicate detections

## Dependencies

Core libraries:
- **rustfft**: Fast Fourier Transform implementation
- **cpal**: Cross-platform audio I/O
- **wgpu**: Modern graphics API (Vulkan/Metal/DX12)
- **winit**: Cross-platform window creation
- **bytemuck**: Safe type casting for shader uniforms

## Building from Source

```bash
# Navigate to audio_viz directory
cd audio_viz

# Build in release mode (recommended)
cargo build --release

# Run
cargo run --release

# Run tests
cargo test
```

## Customization

### Adjusting Visual Effects
Edit `shaders/music_viz.wgsl` to customize:
- Color schemes and gradients
- Pattern intensity and scale
- Movement speed and animation style
- Effect combinations and blending

### Tuning Audio Analysis
Modify `src/audio_analyzer.rs` to adjust:
- FFT size (affects frequency resolution vs latency)
- Frequency band ranges (bass/mid/high boundaries)
- Beat detection sensitivity (threshold multiplier)
- History duration for smoothing

### Example: Custom Color Scheme
```wgsl
// In shaders/music_viz.wgsl, modify bass_pulse function:
fn bass_pulse(uv: vec2<f32>, bass: f32, beat: f32) -> vec3<f32> {
    // ... existing code ...
    
    // Change color from red/purple to blue/cyan
    let color = vec3<f32>(0.1, 0.5, 0.9) * pulse * (bass * 2.0);
    return color;
}
```

## Performance Optimization

- **Release builds**: Always use `--release` for optimal performance
- **FFT size**: Balance between frequency resolution (larger) and latency (smaller)
- **GPU utilization**: Shader effects are GPU-accelerated for minimal CPU impact
- **Frame rate**: Target 60+ FPS on modern hardware

## Troubleshooting

### No audio device found
- Ensure microphone is connected and enabled
- Check system audio permissions
- Verify default input device in OS settings

### Poor performance or low FPS
- Build with `--release` flag
- Update GPU drivers
- Close other GPU-intensive applications
- Try reducing window size

### No beat detection
- Increase audio input volume
- Play music with clear bass/kick drum
- Adjust beat detection threshold in `audio_analyzer.rs`

## Integration with Main Project

While the audio visualization module is standalone, it follows the project's architecture principles:
- **Rust core**: Performance-critical components in Rust
- **Modern libraries**: Uses current ecosystem standards (wgpu, cpal)
- **Documentation**: Comprehensive inline and external docs
- **Testing**: Unit tests for core functionality

## Future Enhancements

Potential improvements (not yet implemented):
- [ ] BPM estimation and tempo visualization
- [ ] Multiple visualization modes/presets
- [ ] User-configurable color schemes via UI
- [ ] Audio file playback support
- [ ] Recording/screenshot functionality
- [ ] MIDI input support
- [ ] VR/AR visualization mode

## Related Documentation

- [Audio Visualization README](audio_viz/README.md) - Detailed module documentation
- [Examples](audio_viz/EXAMPLES.md) - Usage examples and code snippets
- [Main Project README](../README.md) - Durak NLP toolkit documentation

## License

This component follows the main project's license. See the root LICENSE file for details.
