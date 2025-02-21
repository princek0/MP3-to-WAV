#!/usr/bin/env python3
"""
This script converts all MP3 files in the specified input folder to WAV format
with a 16 kHz sample rate (mono), saving the resulting files into the specified
output folder. It preserves the original file names, replacing the ".mp3"
extension with ".wav".
"""

import os
import argparse
from pydub import AudioSegment

def convert_mp3_to_wav(input_folder: str, output_folder: str) -> None:
    """
    Convert all MP3 files in the input folder to WAV files in the output folder,
    with a 16 kHz sample rate and mono audio.
    
    :param input_folder: Path to the folder containing .mp3 files.
    :param output_folder: Path to the folder where .wav files will be saved.
    """
    # Check if input folder exists
    if not os.path.isdir(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Create output folder if it doesn't exist
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # Get a list of all files in the input folder
    files = os.listdir(input_folder)

    # Filter only MP3 files (case-insensitive)
    mp3_files = [f for f in files if f.lower().endswith(".mp3")]

    # Convert each MP3 file to WAV
    for mp3_file in mp3_files:
        input_path = os.path.join(input_folder, mp3_file)
        output_filename = os.path.splitext(mp3_file)[0] + ".wav"
        output_path = os.path.join(output_folder, output_filename)

        print(f"Processing: {mp3_file} -> {output_filename}")
        try:
            audio = AudioSegment.from_mp3(input_path)
            # Set sample rate to 16 kHz and make it mono
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(output_path, format="wav")
        except Exception as e:
            print(f"Failed to convert '{mp3_file}': {e}")
        else:
            print(f"Saved WAV to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch convert MP3 files to 16 kHz mono WAV."
    )
    parser.add_argument(
        "--input_folder",
        default=None,
        help="Path to the folder containing MP3 files."
    )
    parser.add_argument(
        "--output_folder",
        default=None,
        help="Path to the folder where converted WAV files will be stored."
    )

    args = parser.parse_args()

    # If folders aren't provided via command line, ask for them interactively
    input_folder = args.input_folder
    if input_folder is None:
        input_folder = input("Enter the path to your MP3 files folder: ").strip()

    output_folder = args.output_folder
    if output_folder is None:
        output_folder = input("Enter the path where WAV files should be saved: ").strip()

    # Verify FFmpeg is installed
    try:
        AudioSegment.from_file("test")
    except Exception as e:
        if "ffmpeg" in str(e).lower():
            print("\nError: FFmpeg is not installed. Please install FFmpeg:")
            print("Windows (using chocolatey): choco install ffmpeg")
            print("Or download from: https://ffmpeg.org/download.html")
            return

    convert_mp3_to_wav(input_folder, output_folder)

if __name__ == "__main__":
    main() 