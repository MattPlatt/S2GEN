from PIL import Image
import os

def convert_to_binary(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)
            # Convert to grayscale
            gray_image = image.convert('L')
            # Binarize the image (threshold at 128)
            binary_image = gray_image.point(lambda p: p > 128 and 255)
            # Save the binary image
            binary_image.save(os.path.join(output_dir, filename))

# Example usage
input_directory = r"C:\Python\NN\S2gen\data\generated\drawings\images"
output_directory = r"C:\Python\NN\S2gen\data\generated\drawings\binary_images"
convert_to_binary(input_directory, output_directory)
