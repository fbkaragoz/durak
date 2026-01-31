// Fragment shader that visualizes music with dynamic effects based on frequency bands
// The shader receives audio analysis data via uniforms and creates animated visuals

struct AudioData {
    bass: f32,
    mid: f32,
    high: f32,
    beat_intensity: f32,
    time: f32,
    _padding: [f32; 3],
}

@group(0) @binding(0)
var<uniform> audio: AudioData;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) vertex_index: u32) -> VertexOutput {
    var out: VertexOutput;
    
    // Full-screen quad
    let x = f32(i32(vertex_index) / 2) * 4.0 - 1.0;
    let y = f32(i32(vertex_index) % 2) * 4.0 - 1.0;
    
    out.position = vec4<f32>(x, y, 0.0, 1.0);
    out.uv = vec2<f32>((x + 1.0) * 0.5, 1.0 - (y + 1.0) * 0.5);
    
    return out;
}

// Smooth noise function for organic movement
fn noise2d(p: vec2<f32>) -> f32 {
    let s = vec2<f32>(113.0, 157.0);
    var v = p;
    let d = dot(v + 0.5, s);
    v = fract(vec2<f32>(d * 1e4)) - 0.5;
    return dot(v, v) * 2.0 - 0.5;
}

// Fractal Brownian Motion for complex patterns
fn fbm(p: vec2<f32>, octaves: i32) -> f32 {
    var value = 0.0;
    var amplitude = 0.5;
    var frequency = 1.0;
    var p_var = p;
    
    for (var i = 0; i < octaves; i = i + 1) {
        value = value + amplitude * noise2d(p_var * frequency);
        frequency = frequency * 2.0;
        amplitude = amplitude * 0.5;
    }
    
    return value;
}

// Create circular/orbital patterns for vocal detection
fn orbital_pattern(uv: vec2<f32>, time: f32, intensity: f32) -> f32 {
    let center = vec2<f32>(0.5, 0.5);
    let dist = distance(uv, center);
    
    let angle = atan2(uv.y - center.y, uv.x - center.x);
    let rotation = time * intensity;
    
    let wave = sin(angle * 6.0 + rotation + dist * 10.0) * 0.5 + 0.5;
    let ring = smoothstep(0.3, 0.31, dist) - smoothstep(0.49, 0.5, dist);
    
    return wave * ring * intensity;
}

// Create bass-driven pulsing effect
fn bass_pulse(uv: vec2<f32>, bass: f32, beat: f32) -> vec3<f32> {
    let center = vec2<f32>(0.5, 0.5);
    let dist = distance(uv, center);
    
    // Pulsing radius based on bass and beat
    let pulse_radius = 0.3 + bass * 0.3 + beat * 0.2;
    let pulse = smoothstep(pulse_radius + 0.05, pulse_radius, dist);
    
    // Deep red/purple color for bass
    let color = vec3<f32>(0.8, 0.1, 0.3) * pulse * (bass * 2.0);
    return color;
}

// Create mid-frequency wave patterns
fn mid_waves(uv: vec2<f32>, mid: f32, time: f32) -> vec3<f32> {
    let wave_freq = 10.0 + mid * 20.0;
    let wave = sin(uv.x * wave_freq + time * 2.0) * cos(uv.y * wave_freq - time * 1.5);
    
    let intensity = (wave * 0.5 + 0.5) * mid;
    
    // Green/cyan color for mids
    let color = vec3<f32>(0.1, 0.7, 0.5) * intensity;
    return color;
}

// Create high-frequency sparkle effects
fn high_sparkles(uv: vec2<f32>, high: f32, time: f32) -> vec3<f32> {
    let sparkle_uv = uv * 20.0;
    let sparkle_time = time * 5.0;
    
    let noise_val = fbm(sparkle_uv + vec2<f32>(sparkle_time), 3);
    let sparkle = smoothstep(0.8, 0.9, noise_val) * high;
    
    // Bright white/yellow sparkles for highs
    let color = vec3<f32>(1.0, 0.9, 0.3) * sparkle * 2.0;
    return color;
}

// Background gradient that responds to overall energy
fn energy_background(uv: vec2<f32>, bass: f32, mid: f32, high: f32) -> vec3<f32> {
    let total_energy = (bass + mid + high) / 3.0;
    
    // Gradient from bottom to top
    let gradient = mix(
        vec3<f32>(0.05, 0.0, 0.1),  // Dark purple at bottom
        vec3<f32>(0.0, 0.05, 0.15), // Dark blue at top
        uv.y
    );
    
    // Brighten based on total energy
    return gradient * (1.0 + total_energy * 0.5);
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let uv = in.uv;
    
    // Start with energy-reactive background
    var color = energy_background(uv, audio.bass, audio.mid, audio.high);
    
    // Add bass pulse effect
    color = color + bass_pulse(uv, audio.bass, audio.beat_intensity);
    
    // Add mid-frequency waves
    color = color + mid_waves(uv, audio.mid, audio.time);
    
    // Add high-frequency sparkles
    color = color + high_sparkles(uv, audio.high, audio.time);
    
    // Add orbital patterns when there's significant mid content (suggesting vocals/melody)
    let vocal_detection = audio.mid * 1.5; // Simplified vocal detection
    if (vocal_detection > 0.3) {
        let orbital = orbital_pattern(uv, audio.time, vocal_detection);
        color = color + vec3<f32>(0.8, 0.4, 0.9) * orbital;
    }
    
    // Beat flash effect
    let flash = audio.beat_intensity * 0.3;
    color = color + vec3<f32>(1.0, 1.0, 1.0) * flash;
    
    // Add some noise texture for visual interest
    let noise = fbm(uv * 5.0 + vec2<f32>(audio.time * 0.1), 4) * 0.05;
    color = color + vec3<f32>(noise);
    
    // Clamp and return
    color = clamp(color, vec3<f32>(0.0), vec3<f32>(1.0));
    
    return vec4<f32>(color, 1.0);
}
