from PIL import Image, ImageDraw
import random
import os

class BlockDiagram:
    def __init__(self, image_size=(2752, 2176)):
        self.image_size = image_size
        self.image = Image.new('RGB', self.image_size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.blocks = []
        self.labels = []
        
        # Load and resize the connector image
        self.connector_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\connector4.png")
        self.connector_image = self.connector_image.resize(
            ((self.connector_image.width // 2), (self.connector_image.height // 2)), Image.Resampling.LANCZOS
        )
        self.connector_width = self.connector_image.width
        self.connector_height = self.connector_image.height

    def draw_block(self, top_left, size, block_name):
        """Draws a dashed rectangle representing a block and adds its label."""
        x, y = top_left
        width, height = size

        dash_length = 5
        # Draw dashed rectangle for the block
        for i in range(x, x + width, dash_length * 2):
            self.draw.line([(i, y), (i + dash_length, y)], fill="black", width=2)
            self.draw.line([(i, y + height), (i + dash_length, y + height)], fill="black", width=2)
        for i in range(y, y + height, dash_length * 2):
            self.draw.line([(x, i), (x, i + dash_length)], fill="black", width=2)
            self.draw.line([(x + width, i), (x + width, i + dash_length)], fill="black", width=2)
        
        self.blocks.append(((x, y), (width, height)))
    
    def paste_connector(self, position, side='right', x_offset=0):
        # Rotate or flip the connector image based on the side specified
        if side == 'left':
            connector_image = self.connector_image.transpose(Image.FLIP_LEFT_RIGHT)
        elif side == 'top':
            connector_image = self.connector_image.rotate(90, expand=True)
        elif side == 'bottom':
            connector_image = self.connector_image.rotate(-90, expand=True)
        else:
            connector_image = self.connector_image  # Default for right

        # Offset the connector's position by a small adjustment to improve placement accuracy
        if side == 'right':
            offset_position = (position[0] - connector_image.width // 2 + 5, position[1] - connector_image.height // 2)
        elif side == 'left':
            offset_position = (position[0] - connector_image.width // 2 - 5, position[1] - connector_image.height // 2)
        elif side == 'top':
            offset_position = (position[0] - connector_image.width // 2, position[1] - connector_image.height)
        elif side == 'bottom':
            offset_position = (position[0] - connector_image.width // 2, position[1])

        # Paste the connector with transparency
        self.image.paste(connector_image, offset_position, connector_image)


    def draw_cable(self, start_connector, end_connector, connector_width):
        start_x, start_y = start_connector
        end_x, end_y = end_connector

        # Adjust start and end points for better alignment at connector tips
        start_x = (start_connector[0])
        start_y = start_connector[1]
        end_x = end_connector[0]
        end_y = end_connector[1]

        # Dash pattern: evenly spaced short dashes
        dash_length = 15
        gap_length = 6

        # Function to draw a dashed line
        def draw_dashed_line(start, end):
            x1, y1 = start
            x2, y2 = end

            if x1 == x2:  # Vertical line
                step = 1 if y2 > y1 else -1
                for i in range(y1, y2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, y2) if step == 1 else max(i - dash_length, y2)
                    self.draw.line([(x1, i), (x1, dash_end)], fill="black", width=1)
            else:  # Horizontal line
                step = 1 if x2 > x1 else -1
                for i in range(x1, x2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, x2) if step == 1 else max(i - dash_length, x2)
                    self.draw.line([(i, y1), (dash_end, y1)], fill="black", width=1)

        # Draw the dashed line connecting the start and end points
        draw_dashed_line((start_x, start_y), (end_x, end_y))

        # Add YOLO label for the cable
        self.add_yolo_label(0, min(start_x, end_x)-2, min(start_y, end_y)-2, abs(end_x - start_x)+5, abs(end_y - start_y)+5)

    def create_diagram(self, diagram_type):
        if diagram_type == 1:
            # Horizontal Image
            y_offset = random.randint(0, 850)
            block_top = (25, 50 + y_offset) 
            block_bottom = (25, self.image_size[1] - 100 - y_offset)
            block_size = (2700, 100)
            
            # Draw blocks
            self.draw_block(block_top, block_size, "BLOCK-TOP")
            self.draw_block(block_bottom, block_size, "BLOCK-BOTTOM")

            # Draw connectors and cables
            num_connectors = random.randint(60, 80)
            for i in range(num_connectors):
                connector_top = (block_top[0] + (i + 1) * (block_size[0] // (num_connectors + 1)), ((block_top[1] + block_size[1]) - 35))
                connector_bottom = (block_bottom[0] + (i + 1) * (block_size[0] // (num_connectors + 1)), (block_bottom[1]) + 35)
                self.paste_connector(connector_top, side='bottom')
                self.paste_connector(connector_bottom, side='top')
                connector_top = (block_top[0] + (i + 1) * (block_size[0] // (num_connectors + 1)), ((block_top[1] + block_size[1]) + 47))
                connector_bottom = (block_bottom[0] + (i + 1) * (block_size[0] // (num_connectors + 1)), (block_bottom[1]) - 47)
                self.draw_cable(connector_top, connector_bottom, self.connector_width)
        elif diagram_type == 2:
            # Vertical Image
            x_offset = random.randint(0, 850)
            block_left = (50 + x_offset, 25)
            block_right = (self.image_size[0] - 100 - x_offset, 25)
            block_size = (100, 2100)
            
            # Draw blocks
            self.draw_block(block_left, block_size, "BLOCK-LEFT")
            self.draw_block(block_right, block_size, "BLOCK-RIGHT")

            # Draw connectors and cables
            num_connectors = random.randint(45, 75)
            for i in range(num_connectors):
                connector_left = (block_left[0] + block_size[0], block_left[1] + (i + 1) * (block_size[1] // (num_connectors + 1)))
                connector_right = (block_right[0], block_right[1] + (i + 1) * (block_size[1] // (num_connectors + 1)))
                self.paste_connector(connector_left, side='right')
                self.paste_connector(connector_right, side='left')
                connector_left = ((block_left[0] + block_size[0]) + 47, block_left[1] + (i + 1) * (block_size[1] // (num_connectors + 1)))
                connector_right = ((block_right[0]) - 47, block_right[1] + (i + 1) * (block_size[1] // (num_connectors + 1)))
                self.draw_cable(connector_left, connector_right, self.connector_width)

    def add_yolo_label(self, class_id, x, y, width, height):
        # Normalize the values for YOLO format
        x_center = (x + width / 2) / self.image_size[0]
        y_center = (y + height / 2) / self.image_size[1]
        width /= self.image_size[0]
        height /= self.image_size[1]
        
        # Add YOLO-style label for machine learning purposes
        label = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        self.labels.append(label)

    def save_image(self, output_image_path, image_name):
        """Saves the image to the specified path."""
        os.makedirs(output_image_path, exist_ok=True)
        self.image.save(os.path.join(output_image_path, image_name))

        # Save corresponding YOLO labels
        label_name = os.path.splitext(image_name)[0] + ".txt"
        output_label_path = os.path.join(os.path.dirname(output_image_path), "labels")
        os.makedirs(output_label_path, exist_ok=True)
        with open(os.path.join(output_label_path, label_name), "w") as label_file:
            label_file.writelines(self.labels)

def create_multiple_diagrams(image_numbers, output_dir_images):
    """Generates multiple diagrams."""
    for i in image_numbers:
        diagram = BlockDiagram()
        diagram_type = random.choice([1, 2])  # Randomly choose between horizontal or vertical diagram
        diagram.create_diagram(diagram_type)
        diagram.save_image(output_dir_images, f"diagram_{i}.png")

# Example usage
output_images_directory = r"C:\Python\NN\S2gen\data\generated\drawings\images"

# Generate 10 images
image_numbers = list(range(2, 200, 2))  # 10 images

create_multiple_diagrams(image_numbers, output_images_directory)
