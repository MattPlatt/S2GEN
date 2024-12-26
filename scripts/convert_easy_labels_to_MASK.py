import os
import json
from PIL import Image

# Paths
images_folder = r"C:\Python\NN\S2gen\data\train\drawings\sliced_images"
labels_folder = r"C:\Python\NN\S2gen\data\train\drawings\sliced_labels"
output_json = r"C:\Python\NN\S2gen\data\train\drawings\sliced_coco_annotations.json"

# Class names and their corresponding IDs
class_names = {
    0: 'Block',
    1: 'Connector',
    3: 'Cable',
    5: 'Dashed Line with Arrow',
    6: 'Double Box',
    7: 'Module',
    8: 'Call Out',
    9: 'Double Connector',
    10: 'Call Out Circle',
    11: 'Spare',
    12: 'Group Box',
    13: 'Spider Web of Angled Connections',
    14: 'Vertical Structure',
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

# Initialize COCO format dictionary
coco_format = {
    "images": [],
    "annotations": [],
    "categories": [{"id": i, "name": name} for i, name in class_names.items()]
}

# Annotation and image counters
annotation_id = 0
image_id = 0

# Loop through each image and corresponding YOLO label file
for image_filename in os.listdir(images_folder):
    if image_filename.endswith((".jpg", ".png")):
        # Process image
        image_path = os.path.join(images_folder, image_filename)
        img = Image.open(image_path)
        width, height = img.size

        # Add image info to COCO format
        coco_format["images"].append({
            "file_name": image_filename,
            "height": height,
            "width": width,
            "id": image_id
        })

        # Process label file
        label_filename = os.path.splitext(image_filename)[0] + ".txt"
        label_path = os.path.join(labels_folder, label_filename)
        
        with open(label_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Parse YOLO label format
                class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())
                
                # Convert YOLO format to COCO format
                x_center *= width
                y_center *= height
                box_width *= width
                box_height *= height
                x1 = int(x_center - box_width / 2)
                y1 = int(y_center - box_height / 2)
                bbox = [x1, y1, int(box_width), int(box_height)]

                # Define segmentation (polygon) for the bounding box
                segmentation = [[x1, y1, x1 + bbox[2], y1, x1 + bbox[2], y1 + bbox[3], x1, y1 + bbox[3]]]

                # Add annotation info to COCO format
                coco_format["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": int(class_id),  # Use class_id directly from the YOLO file
                    "bbox": bbox,
                    "area": bbox[2] * bbox[3],
                    "iscrowd": 0,
                    "segmentation": segmentation
                })
                
                annotation_id += 1

        image_id += 1

# Save COCO annotations as a JSON file
with open(output_json, 'w') as outfile:
    json.dump(coco_format, outfile)

print(f"COCO-format annotations saved to {output_json}")
