use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::{Device, Stream, StreamConfig};
use std::sync::{Arc, Mutex};
use anyhow::{Result, Context};

/// Audio input handler that captures audio from a device
pub struct AudioInput {
    device: Device,
    config: StreamConfig,
    buffer: Arc<Mutex<Vec<f32>>>,
    stream: Option<Stream>,
}

impl AudioInput {
    /// Create a new audio input from the default input device
    pub fn new() -> Result<Self> {
        let host = cpal::default_host();
        let device = host
            .default_input_device()
            .context("No input device available")?;

        let config = device
            .default_input_config()
            .context("Failed to get default input config")?
            .into();

        Ok(Self {
            device,
            config,
            buffer: Arc::new(Mutex::new(Vec::new())),
            stream: None,
        })
    }

    /// Start capturing audio
    pub fn start(&mut self) -> Result<()> {
        let buffer = self.buffer.clone();
        let err_fn = |err| eprintln!("Audio stream error: {}", err);

        // Build stream for f32 format
        let stream = self.build_stream_f32(buffer, err_fn)?;

        stream.play().context("Failed to play stream")?;
        self.stream = Some(stream);
        Ok(())
    }

    fn build_stream_f32(
        &self,
        buffer: Arc<Mutex<Vec<f32>>>,
        err_fn: impl Fn(cpal::StreamError) + Send + 'static,
    ) -> Result<Stream>
    {
        let stream = self
            .device
            .build_input_stream(
                &self.config,
                move |data: &[f32], _: &_| {
                    if let Ok(mut buf) = buffer.lock() {
                        buf.extend_from_slice(data);
                        // Keep only recent samples (2 seconds worth)
                        let max_len = 88200; // 2 seconds at 44100 Hz
                        if buf.len() > max_len {
                            let drain_count = buf.len() - max_len;
                            buf.drain(0..drain_count);
                        }
                    }
                },
                err_fn,
                None,
            )
            .context("Failed to build input stream")?;

        Ok(stream)
    }

    /// Get captured audio samples
    pub fn get_samples(&self, count: usize) -> Vec<f32> {
        if let Ok(buf) = self.buffer.lock() {
            let len = buf.len();
            if len >= count {
                buf[len - count..].to_vec()
            } else {
                buf.clone()
            }
        } else {
            Vec::new()
        }
    }

    /// Get sample rate
    pub fn sample_rate(&self) -> u32 {
        self.config.sample_rate.0
    }

    /// Stop capturing audio
    pub fn stop(&mut self) {
        self.stream = None;
    }
}

/// Audio file loader for testing
pub struct AudioFileLoader;

impl AudioFileLoader {
    /// Load audio from a WAV file
    pub fn load_wav(path: &str) -> Result<(Vec<f32>, u32)> {
        let mut reader = hound::WavReader::open(path)
            .context("Failed to open WAV file")?;
        
        let spec = reader.spec();
        let sample_rate = spec.sample_rate;

        let samples: Result<Vec<f32>> = match spec.sample_format {
            hound::SampleFormat::Float => {
                reader.samples::<f32>()
                    .collect::<Result<Vec<_>, _>>()
                    .context("Failed to read float samples")
            }
            hound::SampleFormat::Int => {
                let samples: Vec<i32> = reader.samples::<i32>()
                    .collect::<Result<Vec<_>, _>>()
                    .context("Failed to read int samples")?;
                
                let max_val = i32::MAX as f32;
                Ok(samples.iter().map(|&s| s as f32 / max_val).collect())
            }
        };

        Ok((samples?, sample_rate))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_audio_input_creation() {
        // This test may fail on systems without audio input
        if let Ok(input) = AudioInput::new() {
            assert!(input.sample_rate() > 0);
        }
    }
}
