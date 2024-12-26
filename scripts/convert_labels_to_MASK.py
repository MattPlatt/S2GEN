import os
import json
from PIL import Image

# Paths
images_folder = r"C:\Python\NN\S2gen\data\val\drawings\images"
labels_folder = r"C:\Python\NN\S2gen\data\val\drawings\labels"
output_json = r"C:\Python\NN\S2gen\data\val\drawings\coco_annotations.json"

# Initialize COCO format dictionary
coco_format = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 0, "name": "dashed_line"}]  # Only one class
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

                # Define segmentation (polygon) for the dashed line's bounding box
                segmentation = [[x1, y1, x1 + bbox[2], y1, x1 + bbox[2], y1 + bbox[3], x1, y1 + bbox[3]]]

                # Add annotation info to COCO format
                coco_format["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": 0,  # Single class 'dashed_line'
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
