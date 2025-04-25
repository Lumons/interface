import os
import json
import pandas as pd
import torch
import whisper
import openai
from datetime import datetime
import lmstudio as lms
import warnings
from supabase import create_client, Client
from dotenv import load_dotenv

# Ignore FutureWarning from PyTorch module
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# Constants
INDEX_FILE = 'transcription_index.txt'  # File to store names of transcribed audio files
AUDIO_FOLDER = 'audio_notes/logs/local'  # Folder containing audio files
CSV_FILE = 'audio_transcriptions.csv'  # CSV to store transcriptions


load_dotenv()

# Fetch Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Supabase URL or Key not set in environment variables.")


def load_whisper_model():
    """Load the Whisper model, using GPU if available."""
    cuda_available = torch.cuda.is_available()
    print("CUDA available:", cuda_available)
    return whisper.load_model("large-v3-turbo", device="cuda" if cuda_available else "cpu")

def transcribe_audio(audio_path, model):
    """Transcribes the given audio file and returns the transcription."""
    result = model.transcribe(audio_path)
    transcription = result['text']
    print(f"Transcription for {audio_path}: {transcription}")
    return transcription

def get_embedding(content):
    model = lms.embedding_model("nomic-embed-text-v1.5")
    embedding = model.embed(content)
    return embedding

def load_transcription_index():
    """Loads the list of already transcribed files from the index."""
    if not os.path.exists(INDEX_FILE):
        return set()
    with open(INDEX_FILE, "r") as f:
        return set(f.read().splitlines())

def update_transcription_index(file_name):
    """Updates the transcription index by adding the new transcribed file."""
    with open(INDEX_FILE, "a") as f:
        f.write(file_name + "\n")

def append_to_csv(file_name, transcription):
    """Appends the metadata of a transcribed file to the CSV."""
    date = datetime.now().strftime("%Y-%m-%d")
    new_row = pd.DataFrame([{
        "Date": date,
        "File Name": file_name,
        "Transcription": transcription
    }])
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
    else:
        updated_df = new_row
    updated_df.to_csv(CSV_FILE, index=False)
    print(f"Metadata for {file_name} added to {CSV_FILE}.")

def insert_to_supabase(file_name, transcription, embedding, client):
    """Inserts audio file metadata and embedding into the Supabase database."""
    try:
        # Extract date and time from the filename
        date_str = os.path.splitext(file_name)[0]  # Remove file extension
        date_obj = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
        
        # Convert datetime to string in ISO format
        date_iso = date_obj.isoformat()

        # Prepare data dictionary
        data = {
            "filename": file_name,
            "datetime": date_iso,
            "contents": transcription,
            "embeddings": embedding
        }
        
        # Insert into Supabase
        response = client.table('log-entries').insert(data).execute()
        if response.data:
            print(f"Inserted {file_name} into Supabase Table 'log-entries':", response.data)
        else:
            print(f"Failed to insert {file_name}. Error: {response.error}.")
    except Exception as e:
        print(f"Exception occurred: {e}")

def transcribe_folder(folder_path):
    """Transcribes all audio files in the folder that are not in the transcription index."""
    # Load the transcription index
    transcribed_files = load_transcription_index()
    # Load the Whisper model
    model = load_whisper_model()
    # Create a Supabase client
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    for file_name in os.listdir(folder_path):
        audio_path = os.path.join(folder_path, file_name)
        if os.path.isfile(audio_path) and file_name.endswith(('.wav', '.mp3', '.m4a')):
            if file_name not in transcribed_files:
                print(f"Transcribing {file_name}...")
                try:
                    # Transcribe the audio
                    transcription = transcribe_audio(audio_path, model)
                    
                    # Generate embedding for the transcription
                    embedding = get_embedding(transcription)

                    # Append metadata to CSV
                    append_to_csv(file_name, transcription)
                    
                    # Insert into Supabase
                    insert_to_supabase(file_name, transcription, embedding, client)
                    
                    # Update the transcription index
                    update_transcription_index(file_name)
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
            else:
                print(f"Skipping {file_name}, already transcribed.")

if __name__ == "__main__":
    # Ensure the audio folder exists
    if os.path.exists(AUDIO_FOLDER):
        transcribe_folder(AUDIO_FOLDER)
    else:
        print(f"Folder {AUDIO_FOLDER} not found.")