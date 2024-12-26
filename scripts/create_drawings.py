from PIL import Image, ImageDraw, ImageFont
import random
import os

class BlockDiagram:
    def __init__(self, image_size=(2752, 2176)):
        self.image_size = image_size
        self.image = Image.new('RGB', self.image_size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.blocks = []
        self.all_connectors = []
        self.other_lines = []
        self.labels = []  # Store labels for YOLO
        
        # Load your connector image from the specified path and resize to 1/2 of its size
        self.connector_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\connector4.png")
        self.connector_image = self.connector_image.resize(
            ((self.connector_image.width // 2), (self.connector_image.height // 2)), Image.Resampling.LANCZOS
        )
        self.double_connector_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\double_connector2.png")
        self.double_connector_image = self.double_connector_image.resize(
            (self.double_connector_image.width // 2, self.double_connector_image.height // 2), Image.Resampling.LANCZOS
        )

        self.spare_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\spare.png")
        self.spare_image = self.spare_image.resize(
            (self.spare_image.width // 3, self.spare_image.height // 3), Image.Resampling.LANCZOS
        )

        self.double_call_out = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\double_call_out.png")
        self.double_call_out = self.double_call_out.resize(
            (self.double_call_out.width // 6, self.double_call_out.height // 6), Image.Resampling.LANCZOS
        )

        self.font = ImageFont.load_default()  # Default font for labels
        self.rj_font = ImageFont.load_default()  # For the RJ-45 text, replace with custom if needed

    def is_overlapping(self, new_block, min_distance=100):
        x1, y1 = new_block[0]
        w1, h1 = new_block[1]

        for block in self.blocks:
            x2, y2 = block[0]
            w2, h2 = block[1]

            if not (x1 + w1 + min_distance < x2 or x2 + w2 + min_distance < x1 or y1 + h1 + min_distance < y2 or y2 + h2 + min_distance < y1):
                return True
        return False

    def yolo_format(self, x_center, y_center, width, height):
        """Convert to YOLO format with relative coordinates."""
        return f" {x_center / self.image_size[0]:.6f} {y_center / self.image_size[1]:.6f} {width / self.image_size[0]:.6f} {height / self.image_size[1]:.6f}"

    def add_label(self, class_id, x, y, w, h):
        """Add a YOLOv5 label to the labels list."""
        x_center = x + w / 2
        y_center = y + h / 2
        self.labels.append(f"{class_id}{self.yolo_format(x_center, y_center, w, h)}")




    def paste_connector(self, position, side='right', label="RJ-45"):
        # Flip the connector image if it's to be placed on the left side
        if side == 'left':
            connector_image = self.connector_image.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            connector_image = self.connector_image

        # Offset the connector's position by 1/2 of its width towards the center of the block
        offset_position = (position[0] - connector_image.width // 2, position[1])

        # Paste the connector with transparency
        self.image.paste(connector_image, offset_position, connector_image)

        # Add connector label (class 1)
        self.add_label(1, offset_position[0] - 1, offset_position[1] - 1, connector_image.width + 2, connector_image.height + 2)

        # Adjust the label position based on the side the connector is placed on
        if side == 'left':
            text_position = (offset_position[0] + 10, offset_position[1] + 0.75)  # Adjust position upwards
        else:  # side == 'right'
            text_position = (offset_position[0] + connector_image.width - 35, offset_position[1] + 0.75)  # Adjust text to fit the right side

        # Draw the connector text label inside the bounds of the connector
        self.draw.text(text_position, label, fill="black", font=self.rj_font)


    def draw_small_block_above(self, x, y, block_width):
        # Dynamic position for the small block above "BLOCK-2"
        gap = random.randint(50, 150)  # Dynamic distance between BLOCK-2 and the new block
        
        # Double the size of the small block
        small_block_width = (block_width // 3) * 2
        small_block_height = 100  # Doubling the height

        # Position the small block centered above "BLOCK-2"
        small_block_x = x + (block_width - small_block_width) // 2
        small_block_y = y - small_block_height - gap

        # Draw the small block using dashed lines
        dash_length = 5
        for i in range(small_block_x, small_block_x + small_block_width, dash_length * 2):
            self.draw.line([(i, small_block_y), (i + dash_length, small_block_y)], fill="black", width=2)
            self.draw.line([(i, small_block_y + small_block_height), (i + dash_length, small_block_y + small_block_height)], fill="black", width=2)
        for i in range(small_block_y, small_block_y + small_block_height, dash_length * 2):
            self.draw.line([(small_block_x, i), (small_block_x, i + dash_length)], fill="black", width=2)
            self.draw.line([(small_block_x + small_block_width, i), (small_block_x + small_block_width, i + dash_length)], fill="black", width=2)

        # Add text "Peripheral" in the top center of the new block
        text_position = (small_block_x + small_block_width // 2 - 30, small_block_y + 85)
        self.draw.text(text_position, "Peripheral", fill="black", font=self.font)

        # Add block label for the small block (class 0)
        self.add_label(0, small_block_x - 2, small_block_y -2, small_block_width + 7, small_block_height + 7)

        # Draw the dashed line between the small block and "BLOCK-2" using the same style
        line_start = (small_block_x + small_block_width // 2, small_block_y + small_block_height)
        line_end = (x + block_width // 2, y)

        lable_start = ((small_block_x + small_block_width // 2)+1, small_block_y + small_block_height)
        lable_end = ((x + block_width // 2)+1, y)
        
        # Draw the dashed line using the existing pattern
        if line_start[1] != line_end[1]:  # Vertical dashed line
            dash_length = 14
            gap = 6
            step = 1 if line_end[1] > line_start[1] else -1
            for i in range(line_start[1], line_end[1], step * (dash_length + gap)):
                self.draw.line([(line_start[0], i), (line_start[0], i + dash_length * step)], fill="black", width=1)



        # Add label for the dashed line connecting the blocks
        self.add_cable_label(lable_start, lable_end, "cable_mid")

        # Rotate and place the double_connector_image at the top middle of the small block
        rotated_connector = self.double_connector_image.rotate(90, expand=True)
        connector_x = small_block_x + small_block_width // 2 - rotated_connector.width // 2
        connector_y = small_block_y - rotated_connector.height + 40
        self.image.paste(rotated_connector, (connector_x, connector_y), rotated_connector)


        # Add label for the double connector (class_id = 11, adjust as needed)
        self.add_label(9, connector_x -2, connector_y -1, rotated_connector.width +2, rotated_connector.height+2)

        connector_center_x = connector_x + rotated_connector.width // 2
        connector_center_y = connector_y

        # # Add label for the double connector (class_id = 11, adjust as needed)
        # self.add_label(9, connector_x, connector_y, rotated_connector.width, rotated_connector.height)

        # Paste spare/port/slot image
        # Paste spare/port/slot image
        spare = self.spare_image
        spare_x = small_block_x + small_block_width -60
        spare_y = small_block_y +(small_block_height // 3)
        self.image.paste(spare, (spare_x, spare_y), spare)

        self.add_label(11, spare_x -2, spare_y -2, spare.width +2, spare.height +2)


        return (connector_center_x, connector_center_y)  # Return the center coordinates of the connector


    def draw_small_block_below(self, x, y, block_width, block_height):
        # Fixed gap distance between "BLOCK-1" and "Mouse"
        gap = 50

        # Define the size of the "Mouse" block
        small_block_width = (block_width // 3) * 2
        small_block_height = 100  # Height of the small block

        # Position the "Mouse" block centered below "BLOCK-1"
        small_block_x = x + (block_width - small_block_width) // 2
        small_block_y = y + block_height + gap  # Placed directly below with a gap

        # Draw the "Mouse" block using dashed lines
        dash_length = 5
        for i in range(small_block_x, small_block_x + small_block_width, dash_length * 2):
            self.draw.line([(i, small_block_y), (i + dash_length, small_block_y)], fill="black", width=2)
            self.draw.line([(i, small_block_y + small_block_height), (i + dash_length, small_block_y + small_block_height)], fill="black", width=2)
        for i in range(small_block_y, small_block_y + small_block_height, dash_length * 2):
            self.draw.line([(small_block_x, i), (small_block_x, i + dash_length)], fill="black", width=2)
            self.draw.line([(small_block_x + small_block_width, i), (small_block_x + small_block_width, i + dash_length)], fill="black", width=2)

        # Add text "Mouse" in the top center of the new block
        text_position = (small_block_x + small_block_width // 2 - 20, small_block_y + 10)
        self.draw.text(text_position, "Mouse", fill="black", font=self.font)

        # Add block label for the "Mouse" block (class 0)
        self.add_label(0, small_block_x - 2, small_block_y -2, small_block_width + 7, small_block_height + 7)

        # Draw the dashed line between "BLOCK-1" and "Mouse"
        line_start = (x + block_width // 2, y + block_height)  # Bottom center of "BLOCK-1"
        line_end = (small_block_x + small_block_width // 2, small_block_y)  # Top center of "Mouse"
        
        # Draw the dashed line using the existing pattern
        if line_start[1] != line_end[1]:  # Vertical dashed line
            dash_length = 14
            gap = 6
            step = 1 if line_end[1] > line_start[1] else -1
            for i in range(line_start[1], line_end[1], step * (dash_length + gap)):
                self.draw.line([(line_start[0], i), (line_start[0], i + dash_length * step)], fill="black", width=1)


        # Add label for the dashed line connecting the blocks
        self.add_cable_label(line_start, line_end, "cable_mid")

        # Rotate and place the double_connector_image at the very bottom of the small block
        rotated_connector = self.double_connector_image.rotate(-90, expand=True)
        connector_x = small_block_x + small_block_width // 2 - rotated_connector.width // 2
        connector_y = small_block_y + small_block_height - rotated_connector.height // 3
        self.image.paste(rotated_connector, (connector_x, connector_y), rotated_connector)

        # Add label for the double connector (class_id = 11, adjust as needed)
        self.add_label(9, connector_x -2, connector_y -2, rotated_connector.width +2, rotated_connector.height+2)

        # Calculate the connector position to return
        connector_center_x = connector_x + rotated_connector.width // 2
        connector_center_y = connector_y

        # # Add label for the double connector (class_id = 11, adjust as needed)
        # self.add_label(9, connector_x, connector_y, rotated_connector.width, rotated_connector.height)

        # Paste spare/port/slot image
        spare = self.spare_image
        spare_x = small_block_x + small_block_width -60
        spare_y = small_block_y +(small_block_height // 3)
        self.image.paste(spare, (spare_x, spare_y), spare)

        self.add_label(11, spare_x -2, spare_y -2, spare.width +2, spare.height +2)

        return (connector_center_x, connector_center_y)  # Return the center coordinates of the connector


    def draw_block(self, top_left, size, block_name, num_connectors, side, connector_width=40, connector_height=20):
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

        # Add block label near the top inside the block
        block_label_position = (x + width // 2 - 20, y + 10)  # Inside near the top
        self.draw.text(block_label_position, block_name, fill="black", font=self.font)

        # Add block label (class 0)
        self.add_label(0, x - 2, y - 2, width + 7, height + 7)  # Add 1 pixel buffer around the block

        connectors = []

        if block_name == "BLOCK-2":  # Check if it's the lower left-hand block
            # Draw the two modules and get their positions
            module1, module2 = self.draw_two_modules(x, y, width, height)

            # Calculate connector positions within the modules
            module_connectors = []
            for idx, module in enumerate([module1, module2]):
                module_x, module_y, module_width, module_height = module
                connector_y = module_y + module_height // 2  # Center in the module
                connector_x = module_x + module_width  # Right side of the module
                self.paste_connector((connector_x, connector_y - connector_height // 2), side='right')
                module_connectors.append((connector_x, connector_y))

            connectors.extend(module_connectors)

        else:
            # Calculate the available space for connectors
            available_height = height - 50  # Leave some buffer space from the top and bottom
            connector_spacing = available_height // (num_connectors + 1)  # Evenly distribute connectors

            for i in range(num_connectors):
                connector_y = y + connector_spacing * (i + 1)
                if side == 'right':
                    connector_x = x + width  # Position for connectors on the right
                    self.paste_connector((connector_x, connector_y - connector_height // 2), side='right')
                elif side == 'left':
                    connector_x = x  # Position for connectors on the left
                    self.paste_connector((connector_x, connector_y - connector_height // 2), side='left')
                else:
                    connector_x = x + width if i >= num_connectors // 2 else x  # Left/Right side split for middle block
                    side_to_use = 'right' if i >= num_connectors // 2 else 'left'
                    self.paste_connector((connector_x, connector_y - connector_height // 2), side=side_to_use)

                connectors.append((connector_x, connector_y))

        return connectors



    def draw_blocks_and_connect(self, block_above, block_below):
        # Call draw_small_block_above and draw_small_block_below to get connector positions
        connector_above = self.draw_small_block_above(block_above[0], block_above[1], block_above[2])
        connector_below = self.draw_small_block_below(block_below[0], block_below[1], block_below[2], block_below[3])

        # Draw cable between the double connectors using their XY coordinates
        self.draw_cable_for_double_connectors(connector_above, connector_below)


    def draw_cable_for_double_connectors(self, start_connector, end_connector):
        start_x, start_y = start_connector
        end_x, end_y = end_connector

        # Calculate the midpoint
        mid_x = (start_x + end_x) // 2

        # Define the points for the L-shaped cable
        line_1_start = (start_x, start_y)
        line_1_end = (start_x, (start_y + end_y) // 2)  # Vertical line going down to halfway
        line_2_start = (start_x, (start_y + end_y) // 2)
        line_2_end = (end_x, (start_y + end_y) // 2)  # Horizontal line to the right
        line_3_start = (end_x, (start_y + end_y) // 2)
        line_3_end = (end_x, end_y + 109)  # Vertical line going up to the endpoint

        # Dash pattern: evenly spaced short dashes
        dash_length = 14
        gap_length = 6

        # Function to draw a dashed line
        def draw_dashed_line(start, end, horizontal):
            x1, y1 = start
            x2, y2 = end

            # start = x1 + 1, y1
            # end = x2, y2 - 60

            if horizontal:  # Horizontal line
                step = 1 if x2 > x1 else -1
                for i in range(x1, x2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, x2) if step == 1 else max(i - dash_length, x2)
                    self.draw.line([(i, y1), (dash_end, y1)], fill="black", width=1)
            else:  # Vertical line
                step = 1 if y2 > y1 else -1
                for i in range(y1, y2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, y2) if step == 1 else max(i - dash_length, y2)
                    self.draw.line([(x1, i), (x1, dash_end)], fill="black", width=1)

        # Draw the cable segments using the dashed line pattern
        draw_dashed_line(line_1_start, line_1_end, horizontal=False)  # Vertical segment
        draw_dashed_line(line_2_start, line_2_end, horizontal=True)   # Horizontal segment
        draw_dashed_line(line_3_start, line_3_end, horizontal=False)  # Vertical segment

        # Add labels (above and below the middle horizontal line)
        cable_text = "Cable-1234"
        cable_length_text = "Green 3ft"

        # Determine the middle of the horizontal line
        text_x = (line_2_start[0] + line_2_end[0]) // 2

        # Place text "Cable-1234" above the cable
        text_y_above = line_2_start[1] - 15  # Above the cable
        self.draw.text((text_x, text_y_above), cable_text, fill="black")

        # Place text "Green 3ft" below the cable
        text_y_below = line_2_start[1] + 5  # Below the cable
        self.draw.text((text_x, text_y_below), cable_length_text, fill="black")

        # Adjusted labels
        self.add_cable_label(line_1_start, line_1_end, "cable_start")
        self.add_cable_label(line_2_start, line_2_end, "cable_mid")
        self.add_cable_label(line_3_start, line_3_end, "cable_start")





    def check_proximity(self, line, threshold=10):
        x1, y1, x2, y2 = line
        for other_line in self.other_lines:
            ox1, oy1, ox2, oy2 = other_line
            if abs(x1 - ox1) < threshold and abs(y1 - oy1) < threshold:
                return True
        return False

    def draw_cable(self, start_connector, end_connector, connector_width, base_offset=10, step_offset=10, cable_index=0):
        start_x, start_y = start_connector
        end_x, end_y = end_connector

        # Offset the cable's start and end points to the tip of the connector image
        if start_x > end_x:
            start_x -= connector_width // 2  # Adjust start point for left-to-right connections
            end_x += connector_width // 2    # Adjust end point for left-to-right connections
        else:
            start_x += connector_width // 2  # Adjust start point for right-to-left connections
            end_x -= connector_width // 2    # Adjust end point for right-to-left connections

        # Check if blocks are above or below the Y-line (the middle of the canvas)
        canvas_mid_y = self.image_size[1] // 2  # Y-line, mid-point of the canvas

        # Initialize horizontal_offset to ensure it's defined
        horizontal_offset = 0

        # If blocks are above the Y-line
        if start_y < canvas_mid_y and end_y < canvas_mid_y:
            if start_y > end_y:
                # Moving upward, apply a positive horizontal offset
                horizontal_offset = cable_index * 40
            else:
                # Moving downward, apply a negative horizontal offset
                horizontal_offset = -cable_index * 40

        # If blocks are below the Y-line
        elif start_y > canvas_mid_y and end_y > canvas_mid_y:
            if start_y > end_y:
                # Moving upward, apply a positive horizontal offset (larger offset below)
                horizontal_offset = cable_index * 50
            else:
                # Moving downward, apply a negative horizontal offset (larger offset below)
                horizontal_offset = -cable_index * 50

        # Calculate vertical offsets
        offset_start_y = start_y + base_offset - 12
        offset_end_y = end_y + base_offset - 12

        # Define the points for the L-shaped cable
        mid_x = (start_x + end_x) // 2

        line_1_start = (start_x, offset_start_y)
        line_1_end = (mid_x + horizontal_offset, offset_start_y)
        line_2_start = (mid_x + horizontal_offset, offset_start_y)
        line_2_end = (mid_x + horizontal_offset, offset_end_y)
        line_3_start = (mid_x + horizontal_offset, offset_end_y)
        line_3_end = (end_x, offset_end_y)

        # Dash pattern: evenly spaced short dashes
        dash_length = 15
        gap_length = 6

        # Function to draw a dashed line with overlap at the corners
        def draw_dashed_line(start, end, horizontal=True):
            x1, y1 = start
            x2, y2 = end

            if horizontal:  # Horizontal line
                step = 1 if x2 > x1 else -1
                for i in range(x1, x2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, x2) if step == 1 else max(i - dash_length, x2)
                    self.draw.line([(i, y1), (dash_end, y1)], fill="black", width=1)
            else:  # Vertical line
                step = 1 if y2 > y1 else -1
                for i in range(y1, y2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, y2) if step == 1 else max(i - dash_length, y2)
                    self.draw.line([(x1, i), (x1, dash_end)], fill="black", width=1)

        # Draw the cable segments using the dashed line pattern
        draw_dashed_line(line_1_start, line_1_end, horizontal=True)
        draw_dashed_line(line_2_start, line_2_end, horizontal=False)
        draw_dashed_line(line_3_start, line_3_end, horizontal=True)

        # Add labels (above and below the middle horizontal line)
        cable_text = "Cable-1234"
        cable_length_text = "Green 3ft"

        # Determine the middle of the longest horizontal line (line_1)
        longest_horizontal_start = line_1_start
        longest_horizontal_end = line_1_end
        text_x = (longest_horizontal_start[0] + longest_horizontal_end[0]) // 2

        # Place text "Cable-1234" above the cable
        text_y_above = longest_horizontal_start[1] - 15  # Above the cable
        self.draw.text((text_x, text_y_above), cable_text, fill="black")

        # Place text "Green 3ft" below the cable
        text_y_below = longest_horizontal_start[1] + 5  # Below the cable
        self.draw.text((text_x, text_y_below), cable_length_text, fill="black")

        # Adjusted labels
        self.add_cable_label(line_1_start, line_1_end, "cable_start")
        self.add_cable_label(line_2_start, line_2_end, "cable_mid")
        self.add_cable_label(line_3_start, line_3_end, "cable_start")


    def draw_dashed_line_with_arrow(self, start, end, box_position=None):
        """Draw a shortened dashed line with an arrow at the end."""
        dash_length = 10
        gap_length = 6

        # Draw dashed line
        x1, y1 = start
        x2, y2 = end

        # # Ensure the line stops just before the box
        # if box_position:
        #     x2 = box_position[0] # Adjust the endpoint so the dashed line stops before the box

        # Adjust the length of the dashed line
        step = 1 if x2 > x1 else -1
        for i in range(x1, x2 - 10, step * (dash_length + gap_length)):  # Subtracting to stop the line earlier
            self.draw.line([(i, y1), (i + dash_length * step, y1)], fill="black", width=1)

        # Adjust arrow size to make the arrowhead more narrow
        arrow_length = 8  # Length of the arrowhead along the line
        arrow_width = 3   # Half of the width of the arrowhead (smaller value makes it more narrow)

        # Draw the arrowhead at the end of the dashed line
        arrow_tip = (x2, y2)
        arrow_left = (x2 - arrow_length * step, y2 - arrow_width)
        arrow_right = (x2 - arrow_length * step, y2 + arrow_width)
        self.draw.polygon([arrow_tip, arrow_left, arrow_right], fill="black")

        # Load and resize the call_out image as before
        call_out_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\call_out.png")
        call_out_image = call_out_image.resize(
            (call_out_image.width // 8, call_out_image.height // 8), Image.Resampling.LANCZOS
        )

        # Paste the call_out image above and to the right of the connector
        call_out_position_x = x2 - 120
        call_out_position_y = y2 - call_out_image.height + 4  # Adjust based on desired placement
        self.image.paste(call_out_image, (call_out_position_x, call_out_position_y), call_out_image)

        # Add label for the call_out
        self.add_label(8, call_out_position_x, call_out_position_y, call_out_image.width, call_out_image.height)

        # Draw the random number inside the circle in the call_out image
        random_number = str(random.randint(1, 99))
        circle_center_x = call_out_position_x + 4.5 + ((call_out_image.width / 2.5) - 4) / 2
        circle_center_y = call_out_position_y + 2.75 + (call_out_image.height / 2.25) / 2

        # Load and draw the font for the random number
        font_size = 12
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Calculate the position to center the text
        average_char_width = font_size * 0.6
        text_width = len(random_number) * average_char_width
        text_height = font_size
        text_x = circle_center_x + 37
        text_y = circle_center_y - text_height / 2

        # Draw the random number inside the call_out circle
        self.draw.text((text_x, text_y), random_number, fill="black", font=font)

        # Add label for the dashed line with arrow
        self.add_label(5, (max(x1, x2)-45), y1 - 7, 45, 14)  # class_id = 5

        self.add_label(10, call_out_position_x+46, call_out_position_y+2, (call_out_image.width/2.25)-5, (call_out_image.height/2.25)+1)





    def draw_double_box(self, top_left, box_width, box_height):
        """Draw a double box with specified texts and add labels."""
        x, y = top_left
        inner_box_width = box_width // 2

        # Draw outer box
        self.draw.rectangle([x, y, x + box_width, y + box_height], outline="black", width=2)

        # Draw the inner dividing line
        self.draw.line([(x + inner_box_width, y), (x + inner_box_width, y + box_height)], fill="black", width=2)

        # Add specified text inside each half
        text_margin = 10
        text_position_left = (x + text_margin, y + box_height // 2 - 10)
        text_position_right = (x + inner_box_width + text_margin, y + box_height // 2 - 10)
        self.draw.text(text_position_left, "01A", fill="black", font=self.font)
        self.draw.text(text_position_right, "T40", fill="black", font=self.font)

        # Add label for the double box (class_id = 7)
        self.add_label(6, x-2, y-2, box_width + 6, box_height+5)

        # Add text "Patch #2" to the right of the double box
        patch_text_position = (x + box_width + 10, y + box_height // 2 - 10)
        self.draw.text(patch_text_position, "Patch #2", fill="black", font=self.font)

        # Use getbbox to get the size of the text
        bbox = self.font.getbbox("Patch #2")
        patch_text_width = bbox[2] - bbox[0]
        patch_text_height = bbox[3] - bbox[1]







    def add_cable_label(self, start, end, cable_type):
        # Calculate bounding box dimensions with a buffer
        buffer = 3  # Buffer around the cable segment
        min_x, max_x = sorted([start[0], end[0]])
        min_y, max_y = sorted([start[1], end[1]])

        # Adjust the bounding box with the buffer
        min_x -= buffer
        max_x += buffer
        min_y -= buffer
        max_y += buffer

        box_width = max_x - min_x
        box_height = max_y - min_y
        x_center = min_x + box_width / 2
        y_center = min_y + box_height / 2

        # Assign the same class ID to both cable types
        label_dict = {"cable_start": 3, "cable_mid": 3}  # Both map to class ID 3
        class_id = label_dict[cable_type]

        # Add label to the list
        self.add_label(class_id, min_x, min_y, box_width, box_height)



    def draw_dashed_cable(self, start_connector, end_connector, connector_width):
        start_x, start_y = start_connector
        end_x, end_y = end_connector

        # Offset the cable's start and end points to the tip of the connector image
        if start_x > end_x:
            start_x -= connector_width // 2  # Adjust start point for left-to-right connections
            end_x += connector_width // 2    # Adjust end point for left-to-right connections
        else:
            start_x += connector_width // 2  # Adjust start point for right-to-left connections
            end_x -= connector_width // 2    # Adjust end point for right-to-left connections

        # Define the points for the dashed cable
        mid_x = (start_x + end_x) // 2

        line_1_start = (start_x, start_y)
        line_1_end = (mid_x, start_y)
        line_2_start = (mid_x, start_y)
        line_2_end = (mid_x, end_y)
        line_3_start = (mid_x, end_y)
        line_3_end = (end_x, end_y)

        # Dash pattern: evenly spaced short dashes
        dash_length = 5
        gap_length = 3

        # Function to draw a dashed line
        def draw_dashed_line(start, end, horizontal=True):
            x1, y1 = start
            x2, y2 = end

            if horizontal:  # Horizontal line
                step = 1 if x2 > x1 else -1
                for i in range(x1, x2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, x2) if step == 1 else max(i - dash_length, x2)
                    self.draw.line([(i, y1), (dash_end, y1)], fill="black", width=2)
            else:  # Vertical line
                step = 1 if y2 > y1 else -1
                for i in range(y1, y2, step * (dash_length + gap_length)):
                    dash_end = min(i + dash_length, y2) if step == 1 else max(i - dash_length, y2)
                    self.draw.line([(x1, i), (x1, dash_end)], fill="black", width=2)

        # Draw the cable segments using the dashed line pattern
        draw_dashed_line(line_1_start, line_1_end, horizontal=True)
        draw_dashed_line(line_2_start, line_2_end, horizontal=False)
        draw_dashed_line(line_3_start, line_3_end, horizontal=True)

        # Add cable label for the dashed cable
        self.add_cable_label(line_1_start, line_1_end, "cable_mid")
        self.add_cable_label(line_2_start, line_2_end, "cable_mid")
        self.add_cable_label(line_3_start, line_3_end, "cable_mid")

    def draw_connection_between_small_blocks(self, start_position, end_position):
        # Use the tip of the double connector images for connection
        start_connector_y = start_position[1] - self.double_connector_image.height // 2
        end_connector_y = end_position[1] - self.double_connector_image.height // 2

        # Place double connectors on both small blocks
        self.paste_double_connector((start_position[0], start_connector_y), 'right')
        self.paste_double_connector((end_position[0], end_connector_y), 'left')

        # Draw the dashed line directly between the connectors
        line_start = (start_position[0] + self.double_connector_image.width // 2, start_connector_y)
        line_end = (end_position[0] - self.double_connector_image.width // 2, end_connector_y)
        
        # Draw the dashed line with arrow
        self.draw_dashed_line_with_arrow(line_start, line_end)

        # Add the cable label for the connection
        self.add_cable_label(line_start, line_end, "cable_mid")



    def draw_combined_connection(self, block_1_pos, block_2_pos, connector_width, distance_between_connectors=50):
        """Draw a combined connection from two connectors on one block to two on another."""
        
        # Determine the start and end points of the connectors
        start_block_x, start_block_y = block_1_pos
        end_block_x, end_block_y = block_2_pos
        
        # Add connectors to Block 1
        connector_1_start_y = start_block_y - distance_between_connectors
        connector_2_start_y = start_block_y
        self.paste_connector((start_block_x, connector_1_start_y), side='right')
        self.paste_connector((start_block_x, connector_2_start_y), side='right')
        
        # Add connectors to Block 2
        connector_1_end_y = end_block_y + distance_between_connectors
        connector_2_end_y = end_block_y
        self.paste_connector((end_block_x, connector_1_end_y), side='left')
        self.paste_connector((end_block_x, connector_2_end_y), side='left')
        
        # Coordinates for the combined cable
        start_x = start_block_x + connector_width // 2
        end_x = end_block_x - connector_width // 2
        combined_y_start = (connector_1_start_y + connector_2_start_y) // 2
        combined_y_end = (connector_1_end_y + connector_2_end_y) // 2
        
        # Draw lines from connectors to the combined line
        self.draw_dashed_line_with_arrow((start_block_x, connector_1_start_y), (start_x, combined_y_start))
        self.draw_dashed_line_with_arrow((start_block_x, connector_2_start_y), (start_x, combined_y_start))
        
        # Draw the combined cable from Block 1 to Block 2
        self.draw_dashed_line_with_arrow((start_x, combined_y_start), (end_x, combined_y_end))
        
        # Draw lines from the combined line to connectors on Block 2
        self.draw_dashed_line_with_arrow((end_x, combined_y_end), (end_block_x, connector_1_end_y))
        self.draw_dashed_line_with_arrow((end_x, combined_y_end), (end_block_x, connector_2_end_y))


    def draw_two_modules(self, block_x, block_y, block_width, block_height):
        """Draw two small modules inside the bottom-left block and add labels for them."""
        
        # Define module dimensions as a fraction of the block size
        module_width = block_width // 3
        module_height = block_height // 4

        # Calculate the positions for the two modules (evenly spaced)
        space_between_modules = 20  # Set a gap between the modules
        total_modules_height = (2 * module_height) + space_between_modules

        # Position the first module
        module1_x = block_x + block_width - module_width  # Attached to the right side
        module1_y = block_y + (block_height - total_modules_height) // 2

        # Position the second module right below the first one
        module2_x = module1_x
        module2_y = module1_y + module_height + space_between_modules

        # Draw the two modules
        self._draw_single_module(module1_x, module1_y, module_width, module_height)
        self._draw_single_module(module2_x, module2_y, module_width, module_height)

        # Add labels for the modules
        self.add_label(7, module1_x -2, module1_y -2, module_width + 5, module_height + 5)
        self.add_label(7, module2_x -2, module2_y -2, module_width + 5, module_height + 5)

        # Load the call_out image and resize to half its size
        call_out_image = Image.open(r"C:\Python\NN\S2gen\data\generated\connectors\call_out.png")
        call_out_image = call_out_image.resize(
            (call_out_image.width // 8, call_out_image.height // 8), Image.Resampling.LANCZOS
        )

        # Determine positions to paste the call_out image above and to the right of the connectors
        for module_x, module_y in [(module1_x, module1_y), (module2_x, module2_y)]:
            # Position for the connector in the module
            connector_y = (module_y + module_height // 2)
            connector_x = (module_x + module_width)

            # Paste the call_out image above and to the right of the connector
            call_out_position_x = (connector_x + call_out_image.width // 2) + 35
            call_out_position_y = connector_y - call_out_image.height -2 # 10 pixels above


            # # Add label for the call out Circle in the image. 
            # self.add_label(10, call_out_position_x+46, call_out_position_y+2, (call_out_image.width/2.25)-5, (call_out_image.height/2.25)+1)

            # # Add label for the call out Circle in the image. 
            # self.add_label(10, call_out_position_x+73, call_out_position_y+2, (call_out_image.width/2.25)-5, (call_out_image.height/2.25)+1)

                        # Draw a random number inside the circle
            random_number = str(7)

            # Calculate the center position of the circle
            circle_center_x = call_out_position_x + 46 + ((call_out_image.width / 2.25) - 5) / 2
            circle_center_y = call_out_position_y + 4 + ((call_out_image.height / 2.25)-1) / 2

            # Load a font
            font_size = 12  # Adjust the font size as needed
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

            # Estimate text size (since we can't use font.getsize())
            average_char_width = font_size * 0.6  # Approximate width of a character
            text_width = len(random_number) * average_char_width
            text_height = font_size  # Approximate text height

            # Calculate the position to center the text
            text_x = circle_center_x - text_width / 2
            text_y = circle_center_y - text_height / 2


            # Repeat for the second call_out position (if necessary)
            call_out_position_x = (connector_x + call_out_image.width // 2) - 40
            call_out_position_y = connector_y - call_out_image.height -6
            self.image.paste(call_out_image, (call_out_position_x, call_out_position_y), call_out_image)

            # Add label for the call_out (class_id = 10, adjust as needed)
            self.add_label(8, call_out_position_x, call_out_position_y, call_out_image.width, call_out_image.height)

            # Add label for the call out Circle in the image. 
            self.add_label(10, call_out_position_x+46, call_out_position_y+2, (call_out_image.width/2.25)-5, (call_out_image.height/2.25)+1)

            # Draw a random number inside the circle
            random_number = str(7)

            # Calculate the center position of the circle
            circle_center_x = call_out_position_x + 46 + ((call_out_image.width / 2.25) - 5) / 2
            circle_center_y = call_out_position_y + 4 + ((call_out_image.height / 2.25)-1) / 2

            # Load a font
            font_size = 12  # Adjust the font size as needed
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

            # Estimate text size (since we can't use font.getsize())
            average_char_width = font_size * 0.6  # Approximate width of a character
            text_width = len(random_number) * average_char_width
            text_height = font_size  # Approximate text height

            # Calculate the position to center the text
            text_x = circle_center_x - text_width / 2
            text_y = circle_center_y - text_height / 2

            # Draw the random number
            self.draw.text((text_x, text_y), random_number, fill="black", font=font)



        # Return the module positions for placing connectors and text later
        return (module1_x, module1_y, module_width, module_height), (module2_x, module2_y, module_width, module_height)





    def _draw_single_module(self, module_x, module_y, module_width, module_height):
        """Draw a single module using dashed lines."""
        dash_length = 5
        # Draw the module using dashed lines
        for i in range(module_x, module_x + module_width, dash_length * 2):
            self.draw.line([(i, module_y), (i + dash_length, module_y)], fill="black", width=2)
            self.draw.line([(i, module_y + module_height), (i + dash_length, module_y + module_height)], fill="black", width=2)
        for i in range(module_y, module_y + module_height, dash_length * 2):
            self.draw.line([(module_x, i), (module_x, i + dash_length)], fill="black", width=2)


    def _add_connector(self, connector_x, connector_y, side):
        """Add a connector to the module with a YOLO bounding box."""
        # Flip the connector image if it's on the left side
        if side == 'left':
            connector_image = self.connector_image.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            connector_image = self.connector_image

        # Offset the connector's position
        offset_position = (connector_x - connector_image.width // 2, connector_y - connector_image.height // 2)

        # Paste the connector with transparency
        self.image.paste(connector_image, offset_position, connector_image)

        # Add a YOLO label for the connector
        self.add_label(1, offset_position[0], offset_position[1], connector_image.width, connector_image.height)

        # Optionally add text inside the connector (e.g., "RJ-45")
        text_position = (offset_position[0] + 10, offset_position[1])
        self.draw.text(text_position, "RJ-45", fill="black")

    def draw_dashed_box(self, min_x, min_y, max_x, max_y, label_class_id):
        """Draws a dashed box around the specified coordinates with long dash segments in the corners."""

        # Dash pattern: short and long dash lengths
        short_dash_length = 10
        long_dash_length = 50
        gap_length = 7
        line_width = 2  # Line width used in drawing

        # Define total length of the box sides
        top_length = max_x - min_x
        side_length = max_y - min_y

        def draw_dashed_line_with_corner(start, end, is_horizontal=True):
            x1, y1 = start
            x2, y2 = end

            if is_horizontal:
                # Draw long dash at the beginning of the line (corner)
                self.draw.line([(x1, y1), (min(x1 + long_dash_length, x2), y1)], fill="black", width=line_width)
                x1 += long_dash_length + gap_length

                # Draw middle dashed line with short and long dashes alternating
                while x1 + 2 * short_dash_length + long_dash_length + 2 * gap_length < x2:
                    self.draw.line([(x1, y1), (x1 + short_dash_length, y1)], fill="black", width=line_width)
                    x1 += short_dash_length + gap_length
                    self.draw.line([(x1, y1), (x1 + short_dash_length, y1)], fill="black", width=line_width)
                    x1 += short_dash_length + gap_length
                    self.draw.line([(x1, y1), (x1 + long_dash_length, y1)], fill="black", width=line_width)
                    x1 += long_dash_length + gap_length

                # Draw long dash at the end of the line (corner)
                self.draw.line([(x2 - long_dash_length, y1), (x2, y1)], fill="black", width=line_width)
            else:
                # Vertical lines
                # Draw long dash at the beginning of the line (corner)
                self.draw.line([(x1, y1), (x1, min(y1 + long_dash_length, y2))], fill="black", width=line_width)
                y1 += long_dash_length + gap_length

                # Draw middle dashed line with short and long dashes alternating
                while y1 + 2 * short_dash_length + long_dash_length + 2 * gap_length < y2:
                    self.draw.line([(x1, y1), (x1, y1 + short_dash_length)], fill="black", width=line_width)
                    y1 += short_dash_length + gap_length
                    self.draw.line([(x1, y1), (x1, y1 + short_dash_length)], fill="black", width=line_width)
                    y1 += short_dash_length + gap_length
                    self.draw.line([(x1, y1), (x1, y1 + long_dash_length)], fill="black", width=line_width)
                    y1 += long_dash_length + gap_length

                # Draw long dash at the end of the line (corner)
                self.draw.line([(x1, y2 - long_dash_length), (x1, y2)], fill="black", width=line_width)

        # Draw the top and bottom sides, ensuring they have long dashes at the corners
        draw_dashed_line_with_corner((min_x, min_y), (max_x, min_y), is_horizontal=True)
        draw_dashed_line_with_corner((min_x, max_y), (max_x, max_y), is_horizontal=True)

        # Draw the left and right sides, ensuring they have long dashes at the corners
        draw_dashed_line_with_corner((min_x, min_y), (min_x, max_y), is_horizontal=False)
        draw_dashed_line_with_corner((max_x, min_y), (max_x, max_y), is_horizontal=False)

        # Add a label for the group box
        self.add_label(label_class_id, min_x - 5, min_y - 5, max_x - min_x + 10, max_y - min_y + 10)







    def create_block_in_quadrant(self, quadrant, block_name, num_connectors, allow_right_dashed_line=False):
        quadrant_x, quadrant_y = quadrant[:2]
        max_width = quadrant[0] + self.image_size[0] // 2  # Adjust to allow room for the dashed line and double box
        max_height = quadrant[1] + self.image_size[1] // 2
        width = random.randint(200, 350)  # Restrict width to make room for the dashed line and double box
        height = random.randint(200, 350)

        # Ensure the block can fit within the quadrant
        max_width = max(max_width - 150, quadrant_x + width + 150)
        max_height = max(max_height - 150, quadrant_y + height + 150)

        # Calculate valid ranges for x and y, ensuring the range is not empty
        x_range_start = quadrant_x + 150
        x_range_end = max(max_width - width - 150, x_range_start)
        y_range_start = quadrant_y + 150
        y_range_end = max(max_height - height - 150, y_range_start)

        # Randomly select x and y within the valid range
        x = random.randint(x_range_start, x_range_end)
        y = random.randint(y_range_start, y_range_end)

        # Create the block
        block = ((x, y), (width, height), block_name, num_connectors, 'right')
        if not self.is_overlapping(block):
            self.blocks.append(block)
            connectors = self.draw_block(*block)
            self.all_connectors.append(connectors)

            if allow_right_dashed_line:
                # Draw dashed line with an arrow pointing to the right from the right side of the block
                start_dashed_line = (x + width, y + height // 2)
                end_dashed_line = (start_dashed_line[0] + 150, start_dashed_line[1])
                self.draw_dashed_line_with_arrow(start_dashed_line, end_dashed_line)

                # Draw the double box at the tip of the arrow
                double_box_top_left = (end_dashed_line[0] + 20, end_dashed_line[1] - 30)  # Adjust position to align
                self.draw_double_box(double_box_top_left, 120, 60)

        return block
        
    def create_and_connect_block_pair(self, quadrant_left, quadrant_right, block_name_left, block_name_right,
                                    num_connectors, has_module=False, place_arrow_on_right_block=False):
        """Helper function to create a pair of blocks (left and right) and connect them."""
        margin = 175  # Define a margin to keep blocks away from edges

        # ----- Left block (customizable) -----
        quadrant_x, quadrant_y = quadrant_left[:2]
        width_left = random.randint(200, 350)
        height_left = random.randint(200, 350)

        # Left block position ranges
        min_x_left = quadrant_x + margin
        max_x_left = quadrant_x + self.image_size[0] // 2 - width_left - margin
        min_y_left = quadrant_y + margin
        max_y_left = quadrant_y + self.image_size[1] // 2 - height_left - margin

        # Ensure the ranges are valid
        if max_x_left < min_x_left:
            max_x_left = min_x_left
        if max_y_left < min_y_left:
            max_y_left = min_y_left

        x_left = random.randint(min_x_left, max_x_left)
        y_left = random.randint(min_y_left, max_y_left)

        # Create the left block
        left_block = ((x_left, y_left), (width_left, height_left), block_name_left, num_connectors, 'right')
        if not self.is_overlapping(left_block):
            self.blocks.append(left_block)
            left_connectors = self.draw_block(*left_block)
            self.all_connectors.append(left_connectors)

            if block_name_left == "BLOCK-1":
                # Draw the small block below "BLOCK-1" with the same methodology
                self.draw_small_block_below(x_left, y_left, width_left, height_left)

            if has_module:
                self.draw_two_modules(x_left, y_left, width_left, height_left)

        # ----- Right block (skinnier and taller) -----
        quadrant_x, quadrant_y = quadrant_right[:2]
        width_right = random.randint(100, 150)   # Skinnier
        height_right = random.randint(400, 600)  # Taller

        # Right block position ranges
        min_x_right = self.image_size[0] // 2 + margin
        max_x_right = self.image_size[0] * 3 // 4 - width_right - margin
        min_y_right = quadrant_y + margin
        max_y_right = quadrant_y + self.image_size[1] // 2 - height_right - margin

        # Adjust max_y_right to ensure the block stays within the image vertically
        if max_y_right < min_y_right:
            max_y_right = min_y_right

        x_right = random.randint(min_x_right, max_x_right)
        y_right = random.randint(min_y_right, max_y_right)

        # Create the right block
        right_block = ((x_right, y_right), (width_right, height_right), block_name_right, num_connectors, 'left')
        if not self.is_overlapping(right_block):
            self.blocks.append(right_block)
            right_connectors = self.draw_block(*right_block)
            self.all_connectors.append(right_connectors)

            if place_arrow_on_right_block:
                # Number of arrows and double boxes to draw
                num_arrows = 6  # Original one plus 5 more
                spacing = 65    # Spacing between arrows

                # Starting y-coordinate for the arrows
                total_arrow_height = spacing * (num_arrows - 1)
                start_y = y_right + height_right // 2 - (total_arrow_height // 2)

                for i in range(num_arrows):
                    y_offset = i * spacing
                    current_y = start_y + y_offset

                    # Draw dashed line with an arrow pointing to the right
                    start_dashed_line = (x_right + width_right, current_y)
                    end_dashed_line = (start_dashed_line[0] + 300, current_y)  # Keep the length at 300 pixels
                    self.draw_dashed_line_with_arrow(start_dashed_line, end_dashed_line)

                    # Draw the double box at the tip of the arrow with half the original size
                    double_box_top_left = (end_dashed_line[0], end_dashed_line[1] - 15)
                    self.draw_double_box(double_box_top_left, 60, 30)

        # ----- Connect the two blocks -----
        for i in range(num_connectors):
            self.draw_cable(left_connectors[i], right_connectors[i],
                            self.connector_image.width, base_offset=10, step_offset=10, cable_index=i)

        return left_block, right_block




    def create_diagram(self):
        # Define quadrants
        left_section = self.image_size[0] // 2
        top_section = self.image_size[1] // 2

        quadrants = [
            (0, 0),                     # Top left
            (0, top_section),           # Bottom left
            (left_section, 0),          # Top right
            (left_section, top_section) # Bottom right
        ]

        margin = 100  # Reduced margin to allow more space within quadrants

        # ----- Top-left and Top-right blocks -----
        top_left_block, top_right_block = self.create_and_connect_block_pair(
            quadrant_left=quadrants[0],
            quadrant_right=quadrants[2],
            block_name_left="BLOCK-1",
            block_name_right="BLOCK-3",
            num_connectors=4,
            place_arrow_on_right_block=True  # Place arrow and double box on the top-right block
        )

        # ----- Bottom-left block (static position) -----
        # Adjusted static position for BLOCK-2
        static_x_left = 150  # Adjusted x-coordinate
        static_y_left = self.image_size[1] - 500  # Adjusted y-coordinate to place it higher

        width_left = 300
        height_left = 300

        # Create BLOCK-2 at the static position
        block_name_left = "BLOCK-2"
        num_connectors_left = 2
        left_block = ((static_x_left, static_y_left), (width_left, height_left), block_name_left, num_connectors_left, 'right')

        self.blocks.append(left_block)
        left_connectors = self.draw_block(*left_block)
        self.all_connectors.append(left_connectors)

        # Add modules to BLOCK-2 if needed
        self.draw_two_modules(static_x_left, static_y_left, width_left, height_left)

        # ----- Bottom-right block (dynamic position) -----
        # Adjusted to prevent it from going off-screen
        width_right = random.randint(100, 150)
        height_right = random.randint(400, 500)  # Reduced height to prevent bottom overlap

        # Right block position ranges
        min_x_right = left_section + margin
        max_x_right = self.image_size[0] - width_right - margin
        min_y_right = top_section + margin
        max_y_right = self.image_size[1] - height_right - margin

        # Ensure the ranges are valid
        if max_x_right < min_x_right:
            max_x_right = min_x_right
        if max_y_right < min_y_right:
            max_y_right = min_y_right

        x_right = random.randint(min_x_right, max_x_right)
        y_right = random.randint(min_y_right, max_y_right)

        # Create BLOCK-4 at dynamic position
        block_name_right = "BLOCK-4"
        num_connectors_right = 2
        right_block = ((x_right, y_right), (width_right, height_right), block_name_right, num_connectors_right, 'left')

        self.blocks.append(right_block)
        right_connectors = self.draw_block(*right_block)
        self.all_connectors.append(right_connectors)

        # ----- Connect BLOCK-2 and BLOCK-4 -----
        for i in range(num_connectors_left):
            self.draw_cable(left_connectors[i], right_connectors[i],
                            self.connector_image.width, base_offset=10, step_offset=10, cable_index=i)

        # Extract the positions and sizes for the small blocks
        block_above_position = (static_x_left, static_y_left, width_left)
        block_below_position = (top_left_block[0][0], top_left_block[0][1], top_left_block[1][0], top_left_block[1][1])

        # Draw the connection between the small blocks
        self.draw_blocks_and_connect(block_above_position, block_below_position)

        # Now let's handle bounding boxes and labels for the whole group

        # Get positions and sizes for left and right blocks
        left_blocks_positions = [block[0] for block in [top_left_block, left_block]]
        right_blocks_positions = [block[0] for block in [top_right_block, right_block]]
        left_blocks_sizes = [block[1] for block in [top_left_block, left_block]]
        right_blocks_sizes = [block[1] for block in [top_right_block, right_block]]

        # Adjust padding for bounding boxes
        padding = 50

        # Calculate outer bounds for left group (top-left and bottom-left blocks)
        left_min_x = max(min([pos[0] for pos in left_blocks_positions]) - padding, 0)
        left_min_y = max(min([pos[1] for pos in left_blocks_positions]) - padding, 0)
        left_max_x = min(max([pos[0] + size[0] for pos, size in zip(left_blocks_positions, left_blocks_sizes)]) + padding, self.image_size[0])
        left_max_y = min(max([pos[1] + size[1] for pos, size in zip(left_blocks_positions, left_blocks_sizes)]) + padding, self.image_size[1])

        # Calculate outer bounds for right group (top-right and bottom-right blocks)
        right_min_x = max(min([pos[0] for pos in right_blocks_positions]) - padding, 0)
        right_min_y = max(min([pos[1] for pos in right_blocks_positions]) - padding, 0)
        right_max_x = min(max([pos[0] + size[0] for pos, size in zip(right_blocks_positions, right_blocks_sizes)]) + padding, self.image_size[0])
        right_max_y = min(max([pos[1] + size[1] for pos, size in zip(right_blocks_positions, right_blocks_sizes)]) + padding, self.image_size[1])

        # Draw dashed boxes for left and right group bounds, adding group box annotations
        self.draw_dashed_box(left_min_x, left_min_y, left_max_x, left_max_y, label_class_id=12)
        self.draw_dashed_box(right_min_x, right_min_y, right_max_x, right_max_y, label_class_id=12)


        # Add group box names in the top center of each group box
        left_group_label_position = ((left_min_x + left_max_x) // 2 - 60, left_min_y + 20)
        right_group_label_position = ((right_min_x + right_max_x) // 2 - 60, right_min_y + 20)
        self.draw.text(left_group_label_position, "LEFT GROUP", fill="black", font=self.font)
        self.draw.text(right_group_label_position, "RIGHT GROUP", fill="black", font=self.font)

        # Add a bounding box around the entire image contents
        bounding_min_x = max(min(left_min_x, right_min_x) - padding, 0)  # Adding extra padding
        bounding_min_y = max(min(left_min_y, right_min_y) - padding, 0)
        bounding_max_x = min(max(left_max_x, right_max_x) + padding, self.image_size[0])
        bounding_max_y = min(max(left_max_y, right_max_y) + padding, self.image_size[1])

        # Add a bounding box around the entire image contents with annotation
        self.draw_dashed_box(bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y, label_class_id=12)

        # Add a bounding box name
        bounding_box_label_position = ((bounding_min_x + bounding_max_x) // 2 - 60, bounding_min_y + 20)
        self.draw.text(bounding_box_label_position, "BOUNDING BOX", fill="black", font=self.font)

        # Note: We have kept the group boxes in the image but removed any annotations for them.






    # Modify the save_image_and_labels method to use the image name directly
    def save_image_and_labels(self, output_image_path, output_label_path, image_name):
        # Save image
        os.makedirs(output_image_path, exist_ok=True)
        self.image.save(os.path.join(output_image_path, image_name))

        # Save labels
        label_name = image_name.replace('.png', '.txt')
        os.makedirs(output_label_path, exist_ok=True)
        with open(os.path.join(output_label_path, label_name), 'w') as label_file:
            label_file.write("\n".join(self.labels))


def create_multiple_diagrams(image_numbers, output_dir_images, output_dir_labels):
    for i in image_numbers:
        diagram = BlockDiagram()
        diagram.create_diagram()
        diagram.save_image_and_labels(output_dir_images, output_dir_labels, f"diagram_{i}.png")

# Example usage
output_images_directory = r"C:\Python\NN\S2gen\data\generated\drawings\images"
output_labels_directory = r"C:\Python\NN\S2gen\data\generated\drawings\labels"

# Generate odd numbers starting from 1 up to 4999 (2500 images)
image_numbers_odd = list(range(1, 1, 2))  # 1, 3, 5, ..., 4999

create_multiple_diagrams(image_numbers_odd, output_images_directory, output_labels_directory)

