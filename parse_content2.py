import re
import sys

def parse_content(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    # Define the pattern to match content between 'Next speaker: narrative_writer' and '--------------------------------------------------------------------------------'
    pattern = r'Next speaker: narrative_writer(.*?)--------------------------------------------------------------------------------'

    # Find all matches in the text
    matches = re.findall(pattern, text, re.DOTALL)
    
    return matches

# Check if file path is provided in argv
if len(sys.argv) != 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

# Get the file path from command-line argument
file_path = sys.argv[1]

# Call the function and print the result
captured_contents = parse_content(file_path)
if captured_contents:
    for i, content in enumerate(captured_contents, 1):
        print(f"\n{content.strip()}\n{'-' * 80}")
else:
    print("No content found between the specified markers.")

