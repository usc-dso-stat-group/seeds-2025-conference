import os
import pandas as pd

# Read the speaker names from the CSV file
input_csv = "speaker_list.csv"
df = pd.read_csv(input_csv)

# Extract speaker names
speaker_names = df["Speaker Name"]

# Create the 'abstracts' directory if it doesn't exist
output_folder = "abstracts"
os.makedirs(output_folder, exist_ok=True)

# Function to format file names
def format_filename(name):
    parts = name.split()
    first = parts[0].lower()
    last = parts[-1].lower()
    return f"{last}_{first}.txt"

# Create a text file for each speaker
for name in speaker_names:
    filename = format_filename(name)
    file_path = os.path.join(output_folder, filename)
    with open(file_path, "w") as f:
        #f.write(f"Abstract for {name}\n")
        f.write("")  # Placeholder content

print(f"Files have been created in the '{output_folder}' folder.")

