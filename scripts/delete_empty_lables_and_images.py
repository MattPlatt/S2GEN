import os

def delete_empty_labels_and_images(label_folder, image_folder):
    # Get list of all label files in the label folder
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_folder, label_file)
        # Check if the label file is empty
        if os.path.getsize(label_path) == 0:
            # Get the corresponding image file name (same base name with .png extension)
            image_file = label_file.replace('.txt', '.png')
            image_path = os.path.join(image_folder, image_file)

            # Delete the label file and the corresponding image file
            os.remove(label_path)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Deleted: {label_path} and {image_path}")
            else:
                print(f"Image file not found: {image_path}, but label file was deleted: {label_path}")
        else:
            print(f"Label file is not empty: {label_path}")

    print("Cleanup completed!")

# Example usage
delete_empty_labels_and_images(
    label_folder=r"C:\Python\NN\S2gen\data\generated\drawings\sliced_labels",
    image_folder=r"C:\Python\NN\S2gen\data\generated\drawings\sliced_images"
)
