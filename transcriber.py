#!/usr/bin/env python3

import os
import torch
import whisper
import warnings

# Ignore FutureWarning from PyTorch module
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

INDEX_FILE = 'transcription_index.txt'  # File to store names of transcribed audio files

def transcribe_audio(audio_path):
    """Transcribes the given audio file and saves the transcription to a .txt file."""
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print("CUDA available:", cuda_available)

    # Load Whisper model on GPU if available, otherwise use CPU
    model = whisper.load_model("large-v3-turbo", device="cuda" if cuda_available else "cpu")

    # Transcribe the audio file
    result = model.transcribe(audio_path)
    print("Transcription:", result['text'])

    # Get base name of the audio file (without extension)
    base_name = os.path.splitext(audio_path)[0]
    
    # Save transcription to a text file with same base name
    output_file = base_name + ".txt"
    with open(output_file, "w") as f:
        f.write(result['text'])
    
    print(f"Transcription saved to {output_file}")

def load_transcription_index():
    """Loads the list of already transcribed files from the index."""
    if not os.path.exists(INDEX_FILE):
        return set()
    
    with open(INDEX_FILE, "r") as f:
        transcribed_files = f.read().splitlines()
    return set(transcribed_files)

def update_transcription_index(audio_file):
    """Updates the transcription index by adding the new transcribed file."""
    with open(INDEX_FILE, "a") as f:
        f.write(audio_file + "\n")

def transcribe_folder(folder_path):
    """Transcribes all audio files in the folder that are not in the transcription index."""
    # Load transcription index to avoid reprocessing files
    transcribed_files = load_transcription_index()

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        audio_path = os.path.join(folder_path, file_name)

        # Only process .wav, .mp3, or .m4a files (other formats supported by Whisper)
        if os.path.isfile(audio_path) and file_name.endswith(('.wav', '.mp3', '.m4a')):
            
            # Check if the file has already been transcribed
            if file_name not in transcribed_files:
                print(f"Transcribing {file_name}...")
                
                # Transcribe the audio file
                transcribe_audio(audio_path)

                # Update index after successful transcription
                update_transcription_index(file_name)
            else:
                print(f"Skipping {file_name}, already transcribed.")

if __name__ == "__main__":
    folder = 'audio_notes/logs/local'  # The folder where your audio files are stored
    if os.path.exists(folder):
        transcribe_folder(folder)
    else:
        print(f"Folder {folder} not found.")
