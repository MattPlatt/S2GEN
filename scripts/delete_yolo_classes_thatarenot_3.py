import os

# Path to the labels folder
labels_folder = r"C:\Python\NN\S2gen\data\generated\drawings\labels"

# Loop through each file in the labels folder
for label_file in os.listdir(labels_folder):
    if label_file.endswith(".txt"):  # Process only text files
        file_path = os.path.join(labels_folder, label_file)

        # Read the contents of the file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Filter out lines that are not class 3
        filtered_lines = [line for line in lines if line.startswith("3 ")]

        # Write the filtered lines back to the file
        with open(file_path, "w") as file:
            file.writelines(filtered_lines)

print("Processing complete: Non-class 3 records removed from all files.")
