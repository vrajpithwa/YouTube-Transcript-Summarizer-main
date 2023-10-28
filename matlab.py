import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Set the sampling frequency and sampling rate
fs = 8000  # Sampling frequency (Hz)
T = 1 / fs  # Sampling rate (seconds)

# Read the speech signal from a WAV file
wav_file = wave.open('"C:\Users\DELL\Desktop\Recording.wav"', 'r')
num_frames = wav_file.getnframes()
signal = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

# Perform sampling of the signal
t = np.arange(0, num_frames / wav_file.getframerate(), T)
sampled_signal = signal.resample(signal, len(t))

# Quantize the sampled signal to 8 bits
quantized_signal = np.round(sampled_signal / 256).astype(np.int8)

# Convert the quantized signal to PCM
pcm_signal = np.packbits(quantized_signal)

# Write the PCM signal to a new WAV file
with wave.open('pcm_signal.wav', 'wb') as f:
    f.setnchannels(1)  # Mono channel
    f.setsampwidth(1)  # 8-bit samples
    f.setframerate(fs)
    f.writeframes(pcm_signal)

# Generate the waveform of the PCM signal
pcm_signal = np.frombuffer(pcm_signal, dtype=np.uint8)
pcm_signal = np.unpackbits(pcm_signal)
pcm_signal = np.array(pcm_signal, dtype=np.int16)
pcm_signal[pcm_signal == 0] = -32768  # Convert 0 to -32768 to visualize the waveform
plt.plot(pcm_signal)
plt.xlabel('Time (samples)')
plt.ylabel('Amplitude')
plt.title('PCM Signal Waveform')
plt.show()