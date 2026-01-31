mod audio_analyzer;
mod audio_input;
mod renderer;

use audio_analyzer::AudioAnalyzer;
use audio_input::AudioInput;
use renderer::Renderer;

use winit::{
    event::*,
    event_loop::EventLoop,
    keyboard::{PhysicalKey, KeyCode},
};
use std::sync::Arc;
use anyhow::Result;

/// Main application state
struct App {
    renderer: Renderer,
    audio_input: AudioInput,
    audio_analyzer: AudioAnalyzer,
}

impl App {
    async fn new(window: Arc<winit::window::Window>) -> Result<Self> {
        // Initialize renderer
        let renderer = Renderer::new(window).await;

        // Initialize audio input
        let mut audio_input = AudioInput::new()?;
        audio_input.start()?;

        // Initialize audio analyzer with appropriate FFT size
        let sample_rate = audio_input.sample_rate() as usize;
        let fft_size = 2048;
        let audio_analyzer = AudioAnalyzer::new(sample_rate, fft_size);

        Ok(Self {
            renderer,
            audio_input,
            audio_analyzer,
        })
    }

    fn update(&mut self) {
        // Get audio samples
        let samples = self.audio_input.get_samples(2048);
        
        if !samples.is_empty() {
            // Analyze audio
            let bands = self.audio_analyzer.process_samples(&samples);
            let beat_intensity = self.audio_analyzer.get_beat_intensity();
            
            // Update renderer with audio data
            self.renderer.update_audio_data(bands, beat_intensity);
        }
    }

    fn resize(&mut self, new_size: winit::dpi::PhysicalSize<u32>) {
        self.renderer.resize(new_size);
    }

    fn render(&mut self) -> Result<(), wgpu::SurfaceError> {
        self.renderer.render()
    }
}

fn main() -> Result<()> {
    env_logger::init();

    // Create event loop and window
    let event_loop = EventLoop::new().unwrap();
    let window = Arc::new(
        event_loop.create_window(
            winit::window::WindowAttributes::default()
                .with_title("Audio Visualization - Music Dancing Shader")
                .with_inner_size(winit::dpi::LogicalSize::new(1280, 720))
        ).unwrap()
    );

    // Initialize application
    let mut app = pollster::block_on(App::new(window.clone()))?;

    println!("Audio Visualization System Started");
    println!("=====================================");
    println!("This system analyzes audio in real-time and creates");
    println!("synchronized visual animations using shaders.");
    println!("");
    println!("Features:");
    println!("  - FFT-based frequency analysis (bass, mid, high)");
    println!("  - Beat detection and intensity tracking");
    println!("  - Real-time shader-based visualization");
    println!("  - Different visual effects for different frequency bands");
    println!("  - Orbital patterns for melodic content");
    println!("");
    println!("Press ESC to exit");
    println!("=====================================");

    // Run event loop
    let _ = event_loop.run(move |event, elwt| {
        match event {
            Event::WindowEvent {
                ref event,
                window_id,
            } if window_id == window.id() => match event {
                WindowEvent::CloseRequested
                | WindowEvent::KeyboardInput {
                    event: KeyEvent {
                        state: ElementState::Pressed,
                        physical_key: PhysicalKey::Code(KeyCode::Escape),
                        ..
                    },
                    ..
                } => elwt.exit(),
                WindowEvent::Resized(physical_size) => {
                    app.resize(*physical_size);
                }
                WindowEvent::RedrawRequested => {
                    app.update();
                    match app.render() {
                        Ok(_) => {}
                        Err(wgpu::SurfaceError::Lost) => app.resize(window.inner_size()),
                        Err(wgpu::SurfaceError::OutOfMemory) => elwt.exit(),
                        Err(e) => eprintln!("Render error: {:?}", e),
                    }
                }
                _ => {}
            },
            Event::AboutToWait => {
                window.request_redraw();
            }
            _ => {}
        }
    });

    Ok(())
}
