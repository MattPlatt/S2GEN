import os
import cv2
import numpy as np

def slice_image_and_adjust_labels(image_folder, label_folder, output_image_folder, output_label_folder, num_slices_width=5, num_slices_height=5, overlap_percentage_width=0.25, overlap_percentage_height=0.25):
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))

        # Load the image
        image = cv2.imread(image_path)
        original_height, original_width, _ = image.shape

        # Calculate slice size and overlap in pixels
        slice_width = original_width // num_slices_width
        slice_height = original_height // num_slices_height
        overlap_width = int(slice_width * overlap_percentage_width)
        overlap_height = int(slice_height * overlap_percentage_height)

        # Adjust slice width and height to account for overlap
        step_width = slice_width - overlap_width
        step_height = slice_height - overlap_height

        # Loop through the image with overlap in a grid pattern for slicing
        slice_idx = 0
        for i in range(num_slices_height):
            for j in range(num_slices_width):
                # Calculate slice boundaries
                x_start = j * step_width
                y_start = i * step_height
                x_end = x_start + slice_width
                y_end = y_start + slice_height

                # Ensure we stay within bounds of the original image
                x_end = min(x_end, original_width)
                y_end = min(y_end, original_height)

                # Slice the image
                slice_img = image[y_start:y_end, x_start:x_end]
                
                # Create a consistent naming pattern for images and labels: "imagename_i_j"
                slice_name_base = f"{os.path.splitext(image_file)[0]}_{i}_{j}"
                slice_image_name = f"{slice_name_base}.png"

                # Save the sliced image
                cv2.imwrite(os.path.join(output_image_folder, slice_image_name), slice_img)

                # Adjust the YOLO labels for the current slice
                new_labels = []
                if os.path.exists(label_path):
                    with open(label_path, 'r') as label_file:
                        lines = label_file.readlines()

                    for line in lines:
                        cls, cx, cy, w_box, h_box = map(float, line.strip().split())

                        # Convert original normalized coordinates to absolute values
                        abs_x = cx * original_width
                        abs_y = cy * original_height
                        abs_w = w_box * original_width
                        abs_h = h_box * original_height

                        # Calculate bounding box edges in the original image
                        box_x_min = abs_x - abs_w / 2
                        box_x_max = abs_x + abs_w / 2
                        box_y_min = abs_y - abs_h / 2
                        box_y_max = abs_y + abs_h / 2

                        # Check if the bounding box intersects with the slice
                        if box_x_max > x_start and box_x_min < x_end and box_y_max > y_start and box_y_min < y_end:
                            # Adjust the bounding box coordinates relative to the slice
                            new_x_min = max(0, box_x_min - x_start)
                            new_x_max = min(slice_width, box_x_max - x_start)
                            new_y_min = max(0, box_y_min - y_start)
                            new_y_max = min(slice_height, box_y_max - y_start)

                            # Calculate the new bounding box center and size
                            new_cx = (new_x_min + new_x_max) / 2 / slice_width
                            new_cy = (new_y_min + new_y_max) / 2 / slice_height
                            new_w_box = (new_x_max - new_x_min) / slice_width
                            new_h_box = (new_y_max - new_y_min) / slice_height

                            # Make sure the new bounding box is within valid range [0, 1]
                            if 0 <= new_cx <= 1 and 0 <= new_cy <= 1 and 0 <= new_w_box <= 1 and 0 <= new_h_box <= 1:
                                new_labels.append(f"{cls} {new_cx} {new_cy} {new_w_box} {new_h_box}\n")

                # Save the label file, even if empty
                slice_label_name = f"{slice_name_base}.txt"
                with open(os.path.join(output_label_folder, slice_label_name), 'w') as slice_label_file:
                    slice_label_file.writelines(new_labels)

    print("Slicing and label adjustment completed!")

# Example usage
slice_image_and_adjust_labels(
    image_folder=r"C:\Python\NN\S2gen\data\generated\drawings\images",
    label_folder=r"C:\Python\NN\S2gen\data\generated\drawings\labels",
    output_image_folder=r"C:\Python\NN\S2gen\data\generated\drawings\sliced_images",
    output_label_folder=r"C:\Python\NN\S2gen\data\generated\drawings\sliced_labels",
    num_slices_width=5,  # Number of slices along the width
    num_slices_height=5,  # Number of slices along the height
    overlap_percentage_width=0.25,  # Horizontal overlap percentage
    overlap_percentage_height=0.25  # Vertical overlap percentage
)
