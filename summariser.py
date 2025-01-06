import os
import re
import json
from datetime import datetime
from openai import OpenAI

def read_text_file(file_path):
    """
    Reads a text file and returns its content as a string.
    """
    with open(file_path, 'r') as f:
        return f.read()

def extract_date_from_filename(filename):
    """
    Extracts a date from the filename and returns it in the 'nnth of month, year' format.
    Assumes the filename contains a date in the format YYYY-MM-DD.
    """
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        date_str = match.group(0)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_suffix = get_day_suffix(date_obj.day)
        formatted_date = date_obj.strftime(f'%-d{day_suffix} of %B, %Y')
        return formatted_date
    return None

def get_day_suffix(day):
    """Returns the ordinal suffix for a given day (1st, 2nd, 3rd, etc.)."""
    if 11 <= day <= 13:
        return 'th'
    elif day % 10 == 1:
        return 'st'
    elif day % 10 == 2:
        return 'nd'
    elif day % 10 == 3:
        return 'rd'
    else:
        return 'th'

def summarize_content(content):
    """
    Summarizes the extracted content using the OpenAI model.
    """
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
      model="hermes-2-pro-llama-3-8b",
      messages=[
        {"role": "system", "content": "You are a personal assistant. The following is a daily voice log that has been transcribed. Provide a comprehensive summary and overview of the voice log. Comment on what appear to be transcription errors, if relevant"},
        {"role": "user", "content": content}
      ],
      temperature=0.7,
    )

    return completion.choices[0].message.content

def create_markdown_file(output_path, title, summary, date_str):
    """
    Creates a new markdown file with the given title, date, and places the summary under a specified section.
    """
    section_name = "Summary"
    
    with open(output_path, 'w') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Date:** {date_str}\n\n")
        f.write(f"{section_name}:\n")
        f.write("\n")
        f.write(summary)

def load_index(index_file):
    """
    Loads the index file containing processed files and their summaries.
    """
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            return json.load(f)
    return {}

def save_index(index_file, index):
    """
    Saves the index file containing processed files and their summaries.
    """
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=4)

def process_text_files(input_dir, output_dir, index_file, model_name):
    """
    Processes all text files in the input directory, summarizes their content, and saves the summaries.
    Keeps a record of dates extracted from filenames.
    """
    index = load_index(index_file)
    date_vector = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            file_modified_time = os.path.getmtime(file_path)
            file_modified_time_str = datetime.fromtimestamp(file_modified_time).isoformat()

            if filename not in index or index[filename]['modified_time'] != file_modified_time_str:
                # Extract the date from the filename
                formatted_date = extract_date_from_filename(filename)
                if formatted_date:
                    date_vector.append(formatted_date)

                # Read the input text file
                text_content = read_text_file(file_path)

                # Summarize the content using the OpenAI model
                summary = summarize_content(text_content)

                # Create a new markdown file with the summary under a specified section
                output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_{model_name}.md")
                title = "Summary of Daily Notes"
                
                create_markdown_file(output_file, title, summary, formatted_date)

                # Update the index
                index[filename] = {
                    'modified_time': file_modified_time_str,
                    'summary_file': output_file
                }

    # Save the updated index
    save_index(index_file, index)

    # Return the vector of formatted dates
    return date_vector

def main():
    # Specify the model name
    model_name = "hermes-2-pro-llama-3-8b"

    # Specify the path to the input and output directories
    input_dir = "/home/luke/repos/interface/audio_notes/logs/local"
    output_dir = f"/home/luke/repos/interface/audio_notes/logs/{model_name}/Daily_notes"
    index_file = os.path.join(output_dir, "index.json")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all text files in the input directory
    date_vector = process_text_files(input_dir, output_dir, index_file, model_name)

    # Print the vector of formatted dates
    print("Formatted Dates:")
    for date in date_vector:
        print(date)

if __name__ == "__main__":
    main()
