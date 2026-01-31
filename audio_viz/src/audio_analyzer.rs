use rustfft::{FftPlanner, num_complex::Complex};
use std::sync::{Arc, Mutex};

/// Represents different frequency bands for audio analysis
#[derive(Debug, Clone, Copy)]
pub struct FrequencyBands {
    pub bass: f32,      // 20-250 Hz
    pub mid: f32,       // 250-2000 Hz
    pub high: f32,      // 2000-20000 Hz
}

impl FrequencyBands {
    pub fn new() -> Self {
        Self {
            bass: 0.0,
            mid: 0.0,
            high: 0.0,
        }
    }
}

/// Audio analyzer that performs FFT and extracts frequency information
pub struct AudioAnalyzer {
    sample_rate: usize,
    fft_size: usize,
    planner: FftPlanner<f32>,
    window: Vec<f32>,
    frequency_bands: Arc<Mutex<FrequencyBands>>,
    beat_detector: BeatDetector,
}

impl AudioAnalyzer {
    pub fn new(sample_rate: usize, fft_size: usize) -> Self {
        let planner = FftPlanner::new();
        let window = Self::create_hann_window(fft_size);
        
        Self {
            sample_rate,
            fft_size,
            planner,
            window,
            frequency_bands: Arc::new(Mutex::new(FrequencyBands::new())),
            beat_detector: BeatDetector::new(sample_rate),
        }
    }

    /// Create Hann window for FFT windowing
    fn create_hann_window(size: usize) -> Vec<f32> {
        (0..size)
            .map(|i| {
                0.5 * (1.0 - f32::cos(2.0 * std::f32::consts::PI * i as f32 / (size - 1) as f32))
            })
            .collect()
    }

    /// Process audio samples and extract frequency bands
    pub fn process_samples(&mut self, samples: &[f32]) -> FrequencyBands {
        if samples.len() < self.fft_size {
            return FrequencyBands::new();
        }

        // Apply window function and convert to complex numbers
        let mut input: Vec<Complex<f32>> = samples[..self.fft_size]
            .iter()
            .zip(&self.window)
            .map(|(&sample, &window)| Complex::new(sample * window, 0.0))
            .collect();

        // Perform FFT
        let fft = self.planner.plan_fft_forward(self.fft_size);
        fft.process(&mut input);

        // Calculate magnitude spectrum
        let magnitudes: Vec<f32> = input
            .iter()
            .take(self.fft_size / 2)
            .map(|c| c.norm())
            .collect();

        // Extract frequency bands
        let bands = self.extract_frequency_bands(&magnitudes);
        
        // Update beat detector
        self.beat_detector.process(bands.bass);
        
        // Store in shared state
        if let Ok(mut fb) = self.frequency_bands.lock() {
            *fb = bands;
        }

        bands
    }

    /// Extract frequency bands from magnitude spectrum
    fn extract_frequency_bands(&self, magnitudes: &[f32]) -> FrequencyBands {
        let freq_resolution = self.sample_rate as f32 / self.fft_size as f32;

        // Define frequency ranges (in Hz)
        let bass_range = (20.0, 250.0);
        let mid_range = (250.0, 2000.0);
        let high_range = (2000.0, 20000.0);

        let bass = self.average_magnitude_in_range(magnitudes, freq_resolution, bass_range);
        let mid = self.average_magnitude_in_range(magnitudes, freq_resolution, mid_range);
        let high = self.average_magnitude_in_range(magnitudes, freq_resolution, high_range);

        FrequencyBands { bass, mid, high }
    }

    /// Calculate average magnitude in a frequency range
    fn average_magnitude_in_range(
        &self,
        magnitudes: &[f32],
        freq_resolution: f32,
        range: (f32, f32),
    ) -> f32 {
        let start_bin = (range.0 / freq_resolution) as usize;
        let end_bin = ((range.1 / freq_resolution) as usize).min(magnitudes.len());

        if start_bin >= end_bin {
            return 0.0;
        }

        let sum: f32 = magnitudes[start_bin..end_bin].iter().sum();
        sum / (end_bin - start_bin) as f32
    }

    pub fn get_frequency_bands(&self) -> Arc<Mutex<FrequencyBands>> {
        self.frequency_bands.clone()
    }

    pub fn get_beat_intensity(&self) -> f32 {
        self.beat_detector.get_intensity()
    }

    pub fn is_beat(&self) -> bool {
        self.beat_detector.is_beat()
    }
}

/// Simple beat detector based on bass energy
struct BeatDetector {
    history: Vec<f32>,
    history_size: usize,
    last_beat_time: f32,
    time_counter: f32,
    sample_rate: f32,
    beat_detected: bool,
    intensity: f32,
}

impl BeatDetector {
    fn new(sample_rate: usize) -> Self {
        Self {
            history: Vec::new(),
            history_size: 43, // ~1 second at 43 fps
            last_beat_time: 0.0,
            time_counter: 0.0,
            sample_rate: sample_rate as f32,
            beat_detected: false,
            intensity: 0.0,
        }
    }

    fn process(&mut self, bass_energy: f32) {
        self.history.push(bass_energy);
        if self.history.len() > self.history_size {
            self.history.remove(0);
        }

        self.time_counter += 1.0 / 43.0; // Assume ~43 fps

        if self.history.len() < self.history_size {
            self.beat_detected = false;
            self.intensity = 0.0;
            return;
        }

        // Calculate average and variance
        let avg: f32 = self.history.iter().sum::<f32>() / self.history.len() as f32;
        let variance: f32 = self.history
            .iter()
            .map(|&x| (x - avg).powi(2))
            .sum::<f32>()
            / self.history.len() as f32;
        
        let threshold = avg + variance.sqrt() * 1.5;

        // Detect beat with cooldown period
        let cooldown_passed = (self.time_counter - self.last_beat_time) > 0.2; // 200ms cooldown
        
        if bass_energy > threshold && cooldown_passed {
            self.beat_detected = true;
            self.last_beat_time = self.time_counter;
            self.intensity = (bass_energy - threshold) / threshold;
        } else {
            self.beat_detected = false;
            // Decay intensity
            self.intensity *= 0.95;
        }
    }

    fn is_beat(&self) -> bool {
        self.beat_detected
    }

    fn get_intensity(&self) -> f32 {
        self.intensity.min(1.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_bands_creation() {
        let bands = FrequencyBands::new();
        assert_eq!(bands.bass, 0.0);
        assert_eq!(bands.mid, 0.0);
        assert_eq!(bands.high, 0.0);
    }

    #[test]
    fn test_audio_analyzer_creation() {
        let analyzer = AudioAnalyzer::new(44100, 2048);
        assert_eq!(analyzer.sample_rate, 44100);
        assert_eq!(analyzer.fft_size, 2048);
    }

    #[test]
    fn test_hann_window() {
        let window = AudioAnalyzer::create_hann_window(1024);
        assert_eq!(window.len(), 1024);
        // First and last values should be near zero
        assert!(window[0] < 0.01);
        assert!(window[window.len() - 1] < 0.01);
        // Middle value should be near 1.0
        assert!((window[512] - 1.0).abs() < 0.01);
    }

    #[test]
    fn test_process_samples() {
        let mut analyzer = AudioAnalyzer::new(44100, 2048);
        let samples: Vec<f32> = (0..2048).map(|_| 0.5).collect();
        let bands = analyzer.process_samples(&samples);
        
        // Should return non-negative values
        assert!(bands.bass >= 0.0);
        assert!(bands.mid >= 0.0);
        assert!(bands.high >= 0.0);
    }
}
