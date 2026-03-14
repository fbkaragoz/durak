# Audio Visualization System / Müzik Görselleştirme Sistemi

A real-time music visualization system that creates dynamic shader-based animations synchronized with audio analysis.

Müziğin ritmi, frekansları ve enerjisiyle senkronize, gerçek zamanlı shader tabanlı animasyonlar üreten bir müzik görselleştirme sistemi.

## Features / Özellikler

### Audio Analysis / Ses Analizi
- **FFT-based frequency analysis**: Separates audio into bass, mid, and high frequency bands
- **Beat detection**: Detects beats and measures their intensity
- **Real-time processing**: Low-latency audio processing for smooth visualization
- **Support for microphone input**: Visualize any audio source in real-time

**FFT tabanlı frekans analizi**: Sesi bass, orta ve yüksek frekans bantlarına ayırır
**Beat tespiti**: Beat'leri tespit eder ve yoğunluğunu ölçer
**Gerçek zamanlı işleme**: Akıcı görselleştirme için düşük gecikmeli ses işleme
**Mikrofon desteği**: Herhangi bir ses kaynağını gerçek zamanlı görselleştirir

### Visual Effects / Görsel Efektler
- **Bass pulse**: Pulsing circular effects responding to bass frequencies
- **Mid-frequency waves**: Wave patterns for mid-range frequencies
- **High-frequency sparkles**: Sparkle effects for high frequencies
- **Orbital patterns**: Smooth orbital movements for melodic content (vocal detection)
- **Beat flash**: Visual flash effects synchronized with detected beats
- **Energy-reactive background**: Background gradient that responds to overall audio energy

**Bass nabız**: Bass frekanslarına tepki veren dairesel nabız efektleri
**Orta frekans dalgaları**: Orta aralık frekanslar için dalga desenleri
**Yüksek frekans parıltıları**: Yüksek frekanslar için parıltı efektleri
**Orbital desenler**: Melodik içerik için yumuşak orbital hareketler (vokal tespiti)
**Beat ışıltısı**: Tespit edilen beat'lerle senkronize görsel ışıltı efektleri
**Enerji-reaktif arka plan**: Genel ses enerjisine tepki veren arka plan gradyanı

## Architecture / Mimari

```
┌─────────────────────────────────────────┐
│   Audio Input (audio_input.rs)         │  ← Microphone/File
│   - Real-time capture                   │
│   - Sample buffering                    │
├─────────────────────────────────────────┤
│   Audio Analyzer (audio_analyzer.rs)   │  ← FFT Processing
│   - FFT computation                     │
│   - Frequency band extraction           │
│   - Beat detection                      │
├─────────────────────────────────────────┤
│   Renderer (renderer.rs)                │  ← WGPU/Vulkan
│   - Shader management                   │
│   - Uniform buffer updates              │
│   - Frame rendering                     │
├─────────────────────────────────────────┤
│   Fragment Shader (music_viz.wgsl)     │  ← Visual Generation
│   - Frequency-based effects             │
│   - Rhythm synchronization              │
│   - Dynamic color and movement          │
└─────────────────────────────────────────┘
```

## Building and Running / Derleme ve Çalıştırma

### Prerequisites / Ön Gereksinimler

- Rust 1.70+ 
- A graphics driver supporting Vulkan/Metal/DirectX 12
- A microphone or audio input device (optional)

### Build / Derleme

```bash
cd audio_viz
cargo build --release
```

### Run / Çalıştırma

```bash
cargo run --release
```

The application will open a window and start visualizing audio from your default microphone. Press ESC to exit.

Uygulama bir pencere açar ve varsayılan mikrofonunuzdan gelen sesi görselleştirmeye başlar. Çıkmak için ESC'ye basın.

## Technical Details / Teknik Detaylar

### Audio Processing
- **Sample Rate**: 44.1 kHz (adjustable)
- **FFT Size**: 2048 samples
- **Window Function**: Hann window for smooth frequency analysis
- **Frequency Bands**:
  - Bass: 20-250 Hz
  - Mid: 250-2000 Hz
  - High: 2000-20000 Hz

### Graphics
- **API**: WGPU (supports Vulkan, Metal, DirectX 12)
- **Shader Language**: WGSL (WebGPU Shading Language)
- **Rendering**: Real-time fragment shader with full-screen quad
- **Performance**: Optimized for 60+ FPS with minimal latency

### Beat Detection Algorithm
The beat detector uses a simple but effective energy-based algorithm:
1. Maintains a history of bass energy values
2. Calculates mean and variance of the history
3. Detects beats when current energy exceeds threshold (mean + 1.5 * std dev)
4. Implements cooldown period to avoid double-detections

## Performance Considerations / Performans Değerlendirmeleri

- **Low Latency**: Audio processing optimized for minimal delay (<10ms)
- **GPU Acceleration**: All visual effects computed on GPU for maximum performance
- **Efficient FFT**: Uses rustfft library with optimized FFT algorithms
- **Parallel Processing**: Audio analysis and rendering run in parallel

**Düşük Gecikme**: Ses işleme minimum gecikme için optimize edilmiş (<10ms)
**GPU Hızlandırma**: Tüm görsel efektler maksimum performans için GPU'da hesaplanır
**Verimli FFT**: Optimize FFT algoritmaları ile rustfft kütüphanesi kullanır
**Paralel İşleme**: Ses analizi ve render paralel çalışır

## Customization / Özelleştirme

### Modifying Visual Effects
Edit `shaders/music_viz.wgsl` to customize:
- Color schemes
- Pattern intensity
- Movement speed
- Effect combinations

### Adjusting Audio Analysis
Modify `audio_analyzer.rs` to change:
- FFT size (affects frequency resolution)
- Frequency band ranges
- Beat detection sensitivity
- Smoothing parameters

## Dependencies / Bağımlılıklar

- **rustfft**: Fast Fourier Transform implementation
- **cpal**: Cross-platform audio I/O
- **wgpu**: Modern graphics API
- **winit**: Cross-platform window creation
- **bytemuck**: Safe casting between types

## Future Enhancements / Gelecek Geliştirmeler

- [ ] Tempo/BPM estimation and display
- [ ] Multiple visualization modes
- [ ] User-configurable color schemes
- [ ] Audio file playback support
- [ ] Recording/screenshot functionality
- [ ] Spectral analysis visualization
- [ ] MIDI input support
- [ ] VR/AR mode

## License

This component follows the main project's license. See the root LICENSE file.

## Author

Part of the Durak project by fbkaragoz
