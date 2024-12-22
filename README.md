# S2GEN

# S2gen: AI-Powered SysML Model Generation

## Overview
Welcome to **S2gen**, a cutting-edge project leveraging state-of-the-art deep learning models to analyze complex diagrams and automatically generate SysML 2.0 models. This project showcases the intersection of artificial intelligence, machine learning, and systems engineering, with a focus on automating traditionally manual workflows.

## Project Goals
This project was designed to:

1. Develop an AI pipeline capable of detecting and classifying elements in engineering diagrams (blocks, connectors, dashed lines, etc.).
2. Extract textual information from identified diagram elements using Optical Character Recognition (OCR).
3. Automate the generation of SysML 2.0 models, integrating detected objects and their relationships into a unified representation.
4. Build a robust and modular framework for instance segmentation and logic inference using tools like Detectron2 and Tesseract OCR.

## Key Features
- **Custom Object Detection**: Training and inference pipelines built on Detectron2 for instance segmentation of blocks, connectors, cables, and dashed lines.
- **OCR Integration**: Enhanced text extraction using Tesseract OCR, fine-tuned for engineering diagrams.
- **SysML 2.0 Export**: Automated generation of SysML 2.0 code representing the relationships between diagram elements.
- **Slicing and Scaling**: Efficient handling of large diagrams by slicing them into smaller segments for focused processing.
- **Data Augmentation**: Advanced augmentations (e.g., brightness, contrast, rotations) to improve model generalization.

## Workflow

### 1. **Data Preparation**
- **Dataset**: Labeled engineering diagrams in COCO format, with categories for blocks, connectors, cables, and dashed lines.
- **Dataset Registration**: Using Detectron2's dataset registration API to load and process training and validation data.

### 2. **Model Training**
- **Instance Segmentation**: Mask R-CNN (ResNet-101 FPN backbone) trained on annotated engineering diagrams.
- **Custom Classes**: 9 primary classes trained, including blocks, connectors, and dashed lines with arrows.
- **Augmentations**: Applied transformations like random brightness, contrast, rotations, and flips to improve robustness.
- **Checkpointing**: Regular model checkpoints saved during training.

### 3. **Inference and Post-Processing**
- **Detection and Segmentation**: Run inference on validation images to predict bounding boxes and masks for diagram elements.
- **Text Extraction**: Use OCR on bounding boxes to extract text labels for blocks and other elements.
- **Relationship Logic**: Apply geometric rules to infer relationships between diagram elements (e.g., cables connecting blocks).

### 4. **SysML 2.0 Generation**
- **Logic Integration**: Convert detected objects and relationships into SysML 2.0 textual representations.
- **Export**: Save SysML code in a structured format for further use in systems engineering tools.

## Repository Structure
```plaintext
S2gen/
|-- data/
|   |-- train/
|   |-- val/
|-- scripts/
|   |-- train.py
|   |-- infer.py
|   |-- preprocess.py
|-- models/
|   |-- mask_rcnn_r101_fpn.pth
|-- outputs/
|   |-- predictions.json
|   |-- sysml_output.txt
|-- README.md
```

## Technologies Used
- **Deep Learning Frameworks**: PyTorch, Detectron2
- **Optical Character Recognition**: Tesseract OCR
- **Data Formats**: COCO JSON annotations
- **Languages**: Python
- **Visualization**: OpenCV

## Achievements
1. Successfully trained and fine-tuned Mask R-CNN models for multi-class instance segmentation.
2. Implemented a robust OCR pipeline with adaptive thresholding and morphological transformations for improved text extraction.
3. Automated SysML 2.0 generation, reducing manual modeling time for complex diagrams.
4. Built a modular framework with extensible pipelines for future diagram types and use cases.

## Challenges Overcome
- **OCR Accuracy**: Developed techniques to focus on specific regions of bounding boxes, improving text recognition for engineering fonts and styles.
- **Dataset Preparation**: Converted and augmented raw data into COCO format with consistent annotations.
- **Model Generalization**: Used extensive augmentations and parameter tuning to enhance model robustness.

## Installation and Usage
### Prerequisites
- Python 3.8+
- NVIDIA GPU with CUDA support

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/S2gen.git
   cd S2gen
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download trained models:
   Place pre-trained weights in the `models/` directory.

### Running the Project
#### Train the Model
```bash
python scripts/train.py
```
#### Run Inference
```bash
python scripts/infer.py --image data/val/easy/diagram_8001.png
```
#### Generate SysML Code
```bash
python scripts/sysml_generator.py --predictions outputs/predictions.json
```

## Future Enhancements
1. Expand the dataset to include more complex diagram elements like extended blocks and group boxes.
2. Integrate NLP techniques for improved OCR results and text parsing.
3. Implement real-time diagram processing using optimized inference pipelines.
4. Explore additional AI architectures (e.g., Transformer-based models) for enhanced detection accuracy.

## Why This Project?
This project demonstrates:
- Expertise in deep learning and AI frameworks (e.g., Detectron2, Tesseract OCR).
- A systematic approach to solving complex engineering problems.
- Integration of diverse technologies to achieve end-to-end automation.

I aim to leverage the knowledge gained from this project to contribute to the field of Artificial Intelligence and pursue advanced studies in AI. This repository showcases my ability to design and implement innovative solutions to real-world problems.

## Contact
For questions or collaboration, please reach out to:
- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

Thank you for visiting this repository! I hope this work demonstrates my technical proficiency and passion for advancing artificial intelligence applications.

