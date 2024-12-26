import os

# Path to the folder containing your label files
labels_folder = r"C:\Python\NN\S2gen\data\generated\drawings\labels"

# Function to remove class 3 and 12 rows from a label file
def remove_class_3_and_12_labels(label_file):
    with open(label_file, 'r') as file:
        lines = file.readlines()

    # Filter out lines where the class is '3' or '12'
    filtered_lines = [line for line in lines if not (line.startswith('3 ') or line.startswith('12 '))]

    # Write the filtered lines back to the file
    with open(label_file, 'w') as file:
        file.writelines(filtered_lines)

# Iterate over all label files in the folder
for filename in os.listdir(labels_folder):
    if filename.endswith('.txt'):  # Only process .txt files (YOLO labels)
        label_file = os.path.join(labels_folder, filename)
        remove_class_3_and_12_labels(label_file)

print("Class 3 and 12 labels removed from all label files.")
