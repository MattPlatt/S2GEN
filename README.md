# Object Detection and Instance Segmentation for converting Images to SysML 2.0

## Problem Statement

This project focuses on creating and training a Convolutional Neural Network (CNN) utilizing instance segmentation and object detection to automatically read and convert Systems Engineering Diagrams into a portable and reusable format for disparate systems, with a primary application in SysML 2.0. The initial focus is specifically on cable block diagrams and their associated engineering standards, ensuring the process aligns with established guidelines for accuracy and consistency. However, the methodology is designed to be adaptable, meaning that if successful, it could be extended to other types of engineering models, such as electrical schematics, piping and instrumentation diagrams (P&IDs), and mechanical layouts. This flexibility highlights the broader potential of the approach, offering a scalable solution to streamline data extraction and integration across various standardized formats, ultimately enhancing Model-Based Systems Engineering (MBSE) workflows.

The training process involves the generation of synthetic datasets using Python scripts that programmatically create cable block diagrams and annotate them dynamically. This approach ensures a diverse and extensive dataset, reducing the dependency on labor-intensive manual labeling while enhancing the model’s ability to generalize. By employing iterative training and validation, the AI refines its understanding of the diagram elements, ensuring high accuracy and adaptability. Furthermore, the modularity of the AI framework allows for future extensions to recognize components in other diagram types, making it a scalable and versatile solution for engineering design and data interoperability.

## Overview

This project automates the creation, annotation, and preprocessing of training data for AI models focused on detecting block diagram blocks, cables, connectors, and other classes that are standardized. Due to exponential complication, many classes have been ommited in the interim to establish a Minimal Viable Product (MVP) to proof the concept. The system addresses the complexity of structured data layouts and prepares high-quality datasets for training object detection and instance segmentation models.

## Training the Models

The system is divided into several modules and workflows, outlined below:

### 1. **Image Generation**
- **Randomized Diagram Creation**: Automatically generate synthetic images containing randomly placed blocks, connectors, and cables using Python's PIL library and custom scripts.
- **Customizable Blocks and Connectors**: The system allows flexibility in the number, size, and placement of blocks and connectors, ensuring varied training data.
- **Cable Routing and Annotation**: Includes logic to connect blocks with dashed cables and annotate them with YOLO-compliant labels.

### 2. **Label Generation**
- **YOLO Format Labels**: Each generated image includes corresponding YOLO labels for object detection tasks. Labels are normalized and stored in .txt files.
- **Custom Class Definitions**: The system supports multiple object classes such as blocks, connectors, cables, and group boxes.

### 3. **Image Slicing**
- **Slicing with Overlap**: Generated images are sliced into smaller patches with a configurable overlap (e.g., 25%) for training efficiency. 
- **Label Adjustment**: Sliced images include adjusted bounding boxes to ensure labels are correctly aligned with the new coordinates of each slice.

### 4. **Dataset Conversion**
- **YOLO to JSON Conversion**: YOLO annotations are converted to COCO-style JSON format for use with Detectron2's instance segmentation and object detection models.
- **Segmentation Masks**: The system generates masks for cables, blocks, and connectors, supporting instance segmentation tasks.

### 5. **Cable-Specific Training**
- **Focused Cable Detection**: A dedicated dataset and model are created exclusively for cables due to their complexity. This model focuses on detecting cables independently of other objects.

### 6. **Comprehensive Model Training**
- **Other Object Detection**: The remaining images, which include blocks and connectors, are processed and used to train another model to handle these objects.
- **Separate and Combined Models**: The pipeline is modular, allowing separate models for cables and other objects or a combined detection approach.

## Key Features
- **Randomized Diagram Variability**: Generate diverse images with customizable block, connector, and cable configurations.
- **Scalable Annotation System**: Supports thousands of images and labels for large-scale dataset creation.
- **Instance Segmentation Ready**: Prepares data for advanced segmentation models like Detectron2.

## Workflow Steps for development and training

1. **Image Generation**:Utilizing Python and PIL create randamized cable block diagram images.
2. **Label Generation and Conversion**: Initially experiment with YOLO; transition to Faster R-CNN ResNet 101, requiring MASK formatting in JSON.![diagram_1](https://github.com/user-attachments/assets/b6a64c40-31bc-42ab-bf55-af9d363d7ae6)![diagram_10](https://github.com/user-attachments/assets/c05865ab-bac6-43f1-a15c-209594104a63)


3. **Image Slicing**: Slice each image with a 25% overlap for enhanced training efficiency.![sliced_image_with_boxes](https://github.com/user-attachments/assets/81e08538-b805-4cf8-b73f-8a7f1a746e16)
7 **Run ResNet 101 on full size image**: Use saved weights to predict and save results in JSON format.
8. **Run ResNet 101 on sliced images with custom settings**: Slice images, run predictions on slices, and adjust bounding box coordinates for the original file.
9. **Combine Predictions**: Merge predictions from both diagram types into a unified COCO JSON format for implementation
10. **Display Predictions**: Visualize combined predictions on the original image for validation.![diagram_8001_annotated (1)](https://github.com/user-attachments/assets/54cf18c3-ee87-4591-8082-3b302b400358)

11. **Run Object Character Recognition (OCR) to capture the location and content of written text within the image.
12. **SysML Conversion**: Convert JSON predictions and OCR into SysMLv2 using custom logic.
13. **Export SysMLv2 File**: Output the final SysMLv2 representation for engineering use utlizing finalized predictions file and captured OCR.

package ConnectionExample {

    // Part definitions for Blocks, Modules, Connectors, and Cables
    part block26: Block { attribute name = ""; }
    part block34: Block { attribute name = ""; }
    part block36: Block { attribute name = ""; }
    part block38: Block { attribute name = ""; }
    part block40: Block { attribute name = ""; }
    part block47: Block { attribute name = "L BLOCK-3"; }
    part module46: Module;
    part module48: Module;

    // Connector definitions
    part connector0: Connector;
    part connector1: Connector;
    part connector2: Connector;
    part connector6: Connector;
    part connector11: Connector;
    part connector20: Connector;
    part connector21: Connector;
    part connector23: Connector;
    part connector28: Connector;
    part connector35: Connector;
    part connector43: Connector;
    part connector45: Connector;

    // Cable parts with unique identifiers
    part cable9: Cable { attribute id = 9; };
    part cable16: Cable { attribute id = 16; };
    part cable25: Cable { attribute id = 25; };
    part cable29: Cable { attribute id = 29; };
    part cable30: Cable { attribute id = 30; };
    part cable32: Cable { attribute id = 32; };

    // Interface definitions for connections between parts
    interface blockConnectorConnection: BinaryInterface connect connector0 to block38 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector1 to block36 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector2 to block26 using Connector;
    interface moduleConnectorConnection: BinaryInterface connect connector2 to module48 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector6 to block26 using Connector;
    interface moduleConnectorConnection: BinaryInterface connect connector6 to module46 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector11 to block47 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector20 to block36 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector21 to block47 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector23 to block36 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector28 to block36 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector35 to block47 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector43 to block38 using Connector;
    interface blockConnectorConnection: BinaryInterface connect connector45 to block47 using Connector;
    interface moduleBlockConnection: BinaryInterface connect module46 to block26 using Module;
    interface moduleBlockConnection: BinaryInterface connect module48 to block26 using Module;

}






## Plans for Implementation of Pipeline

1. **Organize Dataset: Seperate Master Parts List (MPL) and Cable Block Diagrams into two seperate pdfs.
2. **Define locations of each file; C:\Users\muser\Documents\Data\.pdf
3. **Run the model on both which will...
4. **Convert each pdf to seperate images for processing that are both 250 DPI (2752, 2176).
5. **Run OCR on the MPL and save it to a csv for processing
6. **Run each cable block diagram full image to detect and classify Blocks, Connectors, Modules, Spares, Call Outs, Call Out Circles, Dashed line with Arrows, Double Boxes, and Double Connectors. Save predictions.
7. **Slice each cable block diagram image into seperate peices for classifying and detecting cables.
8. **Run Cable Detection Model on image slices.
9. **Convert predictions back into TRUE location on original image using file naming schema.
10. **Combine predictions from both models for each full image.
11. **Run and save OCR on full images to capture text and text locations for conversion
12. **For each full image, convert predictions to sysml2.0 using; combined predictions file, full image OCR data, MPL, and defined relationships between classes.
13. **Run analysis to verify if twins exist between images, if they do, combine them into one Sysml 2.0 block.
14. **Export SysML 2.0 file.
























## Future Plans
- **Installation and Usage Documentation**: Detailed steps for installing dependencies and running the system will be added.
- **Extended Dataset Features**: Incorporate additional classes and annotations for more complex diagrams.
- **Enhanced Models**: Explore advanced architectures to improve detection and segmentation accuracy.
- **Explore simplified data creation and labeling process for future enhancements and re-use in other engineering fields.
- **Train on a wider variety of classes. Especially dashed line with arrow.
- **Development of Master Parts List table parser with OCR linking bubble callout ID's to Part Numbers

