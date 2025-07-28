import numpy as np
from scipy.io.wavfile import write
from time import perf_counter

MAX_INT_16 = 32767


def get_white_noise(sample_rate: int = 44100, duration: int = 1) -> np.array:
    white_noise = np.array([])
    for i in range(duration):
        white_noise = np.append(white_noise, np.random.uniform(-1, 1, sample_rate))
    white_noise = white_noise.flatten()
    return white_noise


def generate_brown_noise(sample_rate: int = 44100, duration: int = 1) -> None:
    """Generate brown noise
    Parameters
    ----------
    sample_rate : int
        sample rate of noise in Hz (default 44100)
    duration : int, optional
        total duration of noise in seconds (default 1)"""
    white_noise = get_white_noise(sample_rate, duration)
    brown_noise = np.zeros(sample_rate * duration)
    brown_noise[0] = white_noise[0]

    for i in range(1, duration * sample_rate):
        temp = brown_noise[i - 1] + white_noise[i]
        if temp < -1:
            temp += 1
        if temp > 1:
            temp -= 1
        brown_noise[i] = temp

    brown_noise = brown_noise.flatten()
    scaled = np.int16(
        brown_noise / np.max(np.abs(brown_noise)) * MAX_INT_16
    )  # scale to max int 16
    try:
        write("brown_noise.wav", sample_rate, scaled)
    except Exception as e:
        raise Exception(f"Failed to save file: {e}")


def main():
    print("Hello from brown-noise-generator!")
    sample_rate = 44100
    duration = 120

    start_time = perf_counter()
    generate_brown_noise(sample_rate, duration)
    end_time = perf_counter()
    print(
        f"Time took to run sample rate: {sample_rate}Hz for duration {duration}s {end_time - start_time:.6f} seconds"
    )


if __name__ == "__main__":
    main()
