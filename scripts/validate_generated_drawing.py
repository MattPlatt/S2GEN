import os
from PIL import Image, ImageDraw, ImageFont

def plot_yolo_labels(image_path, label_path, output_path):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Read the YOLO label file
    with open(label_path, 'r') as file:
        labels = file.readlines()

    # Updated Class to label name mapping
    class_names = {
        0: 'Cable',
        1: 'Connector',
        3: 'Cable',
        5: 'Dashed Line with Arrow',  # Keeping one instance
        6: 'Double Box',
        7: 'Module',
        8: 'Call Out',  # Call Out class ID
        9: 'Double Connector',
        10: 'Call Out Circle',
        11: 'Spare',
        12: 'Group Box',
        13: 'Spider Web of Angled Connections',
        14: 'Verticle Structure',
        15: 'Double Call Out',
        16: 'SFP',
        17: 'Extended Group Box',
        18: 'Double Extended Group Box',
        19: 'Extended Module',
        20: 'Rounded Connector',
        21: 'Double Group Box',
        22: 'Double Extended Block',
        23: 'Double Block',
        24: 'Crooked Cable'

    }


    # Define colors for different classes (optional)
    class_colors = {
        0: 'blue',
        1: 'green',
        2: 'purple',  # For both Group Box and Bounding Box
        3: 'orange',
        4: 'cyan',
        5: 'red',
        6: 'brown',
        7: 'black',
        8: 'pink',
        9: 'gray',
        10: 'red',
        11: 'green',
        12: 'orange',
        13: 'green',
        14: 'blue',
        15: 'blue',
        16: 'yellow',
        17: 'yellow',
        18: 'green',
        19: 'purple',
        20: 'red',
        21: 'red'
        
    }

    # Load a font (optional, for better text rendering)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Loop over each label
    for label in labels:
        # Handle cases where there might be extra whitespace or empty lines
        label = label.strip()
        if not label:
            continue

        # Parse the label
        try:
            class_id, center_x, center_y, box_width, box_height = map(float, label.split())
        except ValueError:
            print(f"Invalid label format in file {label_path}: {label}")
            continue

        class_id = int(class_id)

        # Convert relative coordinates to absolute pixel coordinates
        abs_center_x = center_x * width
        abs_center_y = center_y * height
        abs_width = box_width * width
        abs_height = box_height * height

        # Calculate the top-left and bottom-right coordinates
        top_left_x = abs_center_x - abs_width / 2
        top_left_y = abs_center_y - abs_height / 2
        bottom_right_x = abs_center_x + abs_width / 2
        bottom_right_y = abs_center_y + abs_height / 2

        # Draw the bounding box
        color = class_colors.get(class_id, 'red')
        draw.rectangle([(top_left_x, top_left_y), (bottom_right_x, bottom_right_y)], outline=color, width=1)

        # Add label name
        class_name = class_names.get(class_id, 'Unknown')
        text = f"{class_name}"

        # Calculate text size using available method
        try:
            # For Pillow >= 8.0.0
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            try:
                # For older versions of Pillow
                text_width, text_height = font.getsize(text)
            except AttributeError:
                # As a last resort
                mask = font.getmask(text)
                text_width, text_height = mask.size

        # Adjust text position to ensure it's within the image boundaries
        text_x = max(top_left_x, 0)
        text_y = max(top_left_y - text_height - 2, 0)

        # Draw text background rectangle for better visibility (optional)
        draw.rectangle(
            [(text_x, text_y), (text_x + text_width, text_y + text_height)],
            fill='white'
        )

        # Draw the text
        draw.text((text_x, text_y), text, fill=color, font=font)

    # Save the output image with labels
    image.save(output_path)
    print(f"Labeled image saved: {output_path}")

def process_images_with_labels(image_folder, label_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the image folder
    for image_filename in os.listdir(image_folder):
        if image_filename.endswith(('.png', '.jpg', '.jpeg')):
            # Define full paths for image and corresponding label
            image_path = os.path.join(image_folder, image_filename)
            label_filename = os.path.splitext(image_filename)[0] + '.txt'  # Label file with same name but .txt extension
            label_path = os.path.join(label_folder, label_filename)

            if os.path.exists(label_path):
                # Define output path
                output_path = os.path.join(output_folder, image_filename)

                # Call the function to plot YOLO labels on the image
                plot_yolo_labels(image_path, label_path, output_path)
            else:
                print(f"Label not found for {image_filename}, skipping.")

# Paths to your folders
image_folder = r"C:\Python\NN\S2gen\data\generated\drawings\images"
label_folder = r"C:\Python\NN\S2gen\data\generated\drawings\labels"
output_folder = r"C:\Python\NN\S2gen\data\generated\drawings\images_with_labels"

# Process all images and their corresponding labels
process_images_with_labels(image_folder, label_folder, output_folder)
