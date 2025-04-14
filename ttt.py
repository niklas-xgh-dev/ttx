import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FILE_PATH = "niklas-xgh-dev_ttx_analysis.txt"  # Update this to your file path

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_summary(text):
    """Generate a summary of the text using OpenAI API."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "developer",
                "content": "You are a helpful assistant that summarizes technical documents. Your summary should capture the key points, concepts, and instructions in the document. Be concise but comprehensive."
            },
            {
                "role": "user",
                "content": f"Summarize the following text:\n\n{text}"
            }
        ]
    )
    
    return response.choices[0].message.content

def main():
    # Read the file from the hardcoded path
    try:
        text = read_file(FILE_PATH)
        print(f"Successfully read file: {FILE_PATH}")
        print(f"File size: {len(text)} characters")
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Generate summary
    try:
        print("Generating summary...")
        summary = generate_summary(text)
    except Exception as e:
        print(f"Error generating summary: {e}")
        return
    
    # Print summary to console
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(summary)

if __name__ == "__main__":
    main()