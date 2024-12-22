# Artificial Intelligence Training System for Block Diagrams

## Problem Statement

The ability to read and convert images of cable block diagrams that follow standardized formatting across engineering organizations allows for rapid re-usability, portability, and versatility of existing data into a portable and easily digestible format. This system targets conversion into SysML 2.0, the latest version of the Model-Based Systems Engineering (MBSE) Systems Modeling Language. SysML 2.0 introduces a simpler, more powerful, and portable data format that is easier to work with compared to its predecessors.

By training an AI model capable of converting these images into SysML 2.0, the resulting code can be seamlessly injected into MBSE tools for future engineering modeling use cases. Additionally, this approach enables adaptability to other formats as required, offering a highly flexible solution for engineering design and data interoperability.

Due to the complexity and time sink associated with manually labeling massive amounts of cable block diagram examples, it was more efficient to create a Python script that dynamically generates cable block diagrams and programmatically places annotations around each object for training. This approach drastically reduces manual labor and allows for generating an unlimited number of training images, significantly saving time and resources.

## Overview

This project automates the creation, annotation, and preprocessing of training data for AI models focused on detecting block diagrams, connectors, and cables. The system addresses the complexity of structured data layouts and prepares high-quality datasets for training object detection and instance segmentation models.

## System Architecture and Workflow

The system is divided into several modules and workflows, outlined below:

### 1. **Image Generation**
- **Randomized Diagram Creation**: Automatically generate synthetic images containing randomly placed blocks, connectors, and cables using Python's PIL library and custom scripts.
- **Customizable Blocks and Connectors**: The system allows flexibility in the number, size, and placement of blocks and connectors, ensuring varied training data.
- **Cable Routing and Annotation**: Includes logic to connect blocks with dashed cables and annotate them with YOLO-compliant labels.

![diagram_1](https://github.com/user-attachments/assets/ebf8e6ee-859b-4c44-9bb5-ec3814221f6c)



### 2. **Label Generation**
- **YOLO Format Labels**: Each generated image includes corresponding YOLO labels for object detection tasks. Labels are normalized and stored in `.txt` files.
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

## Future Plans
- **Installation and Usage Documentation**: Detailed steps for installing dependencies and running the system will be added.
- **Extended Dataset Features**: Incorporate additional classes and annotations for more complex diagrams.
- **Enhanced Models**: Explore advanced architectures to improve detection and segmentation accuracy.

