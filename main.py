import numpy as np
from scipy.io.wavfile import write

MAX_INT_16 = 32767


def generate_white_noise(sample_rate: int = 44100, duration: int = 1) -> None:
    """Generate white noise
    Parameters
    ----------
    sample_rate : int
        sample rate of noise in Hz (default 44100)
    duration : int, optional
        total duration of noise in seconds (default 1)"""
    white_noise = np.array([])
    for i in range(duration):
        white_noise = np.append(white_noise, np.random.uniform(-1, 1, sample_rate))
    white_noise = white_noise.flatten()
    scaled = np.int16(
        white_noise / np.max(np.abs(white_noise)) * MAX_INT_16
    )  # scale to max int 16
    try:
        write("test.wav", sample_rate, scaled)
    except Exception as e:
        raise Exception(f"Failed to save file: {e}")

def generate_brown_noise(sample_rate: int = 44100, duration:int 1) -> None:
    pass


def main():
    print("Hello from brown-noise-generator!")
    generate_white_noise(44100, 5)


if __name__ == "__main__":
    main()
