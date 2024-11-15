import re

# Read the file content
with open('novelist_agent_limit_run_log.txt', 'r') as file:
    text = file.read()

# Regular expression to match each chapter's content
pattern = r"\*\*Chapter [0-9]+: [^\*]+\*\*.*?--"

# Find all matches
chapters = re.findall(pattern, text, re.DOTALL)

# Print the extracted chapters
for chapter in chapters:
    print(chapter)
    print("\n" + "-"*40 + "\n")

