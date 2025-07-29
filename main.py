#!/usr/env python
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, lfilter
from argparse import ArgumentParser

MAX_INT_16 = 32767


def generate_brown_noise(
    sample_rate: int = 44100,
    duration: int = 1,
    cutoff: int = 10000,
    order: int = 6,
    filepath: str = "brown_noise.wav",
) -> None:
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
    filtered = low_pass_filter(scaled, cutoff, sample_rate, order)
    try:
        write(filepath, sample_rate, filtered)
    except Exception as e:
        raise Exception(f"Failed to save file: {e}")


def get_white_noise(sample_rate: int = 44100, duration: int = 1) -> np.array:
    white_noise = np.array([])
    for i in range(duration):
        white_noise = np.append(white_noise, np.random.uniform(-1, 1, sample_rate))
    white_noise = white_noise.flatten()
    return white_noise


def low_pass_filter(data: np.array, cutoff: int, fs: float, order: int = 5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_lowpass(cutoff: int, fs: float, order: int = 5):
    return butter(order, cutoff, fs=fs, btype="low", analog=False)


def main():
    parser = ArgumentParser(
        prog="Brown Noise Generator",
        description="Generate brown noise on demand",
    )
    parser.add_argument(
        "sample_rate", help="Noise sample rate in hz", type=int, default=44100
    )
    parser.add_argument("duration", help="Duration of the noise", type=int, default=5)
    parser.add_argument(
        "-c",
        "--cutoff",
        help="Cutoff in hz for low pass filter",
        type=float,
        default=10000,
    )
    parser.add_argument(
        "-o", "--order", help="Order value for low pass filter", type=int, default=6
    )
    parser.add_argument("output_file", type=str, default="brown_noise.wav")
    args = parser.parse_args()
    print("Generating your noise...")

    generate_brown_noise(
        args.sample_rate, args.duration, args.cutoff, args.order, args.output_file
    )

    print(f"Generated successfully. Saved to {args.output_file}")


if __name__ == "__main__":
    main()
