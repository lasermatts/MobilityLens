import os
import subprocess
from datetime import datetime

# Set the default directory to "/camera_module/image_output/"
DEFAULT_OUTPUT_DIR = 'image_output/'

def ensure_dir_exists(dir_path):
    """
    Ensure the specified directory exists. If it doesn't, create it.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def capture_image(output_dir=DEFAULT_OUTPUT_DIR, filename_prefix='image'):
    """
    Capture an image using libcamera.
    The image is saved in the specified directory with a filename that's a combination of the given prefix and the current timestamp.
    """
    # Ensure the output directory exists
    ensure_dir_exists(output_dir)

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Construct the filename
    filename = f"{filename_prefix}_{timestamp}.jpg"
    output_path = os.path.join(output_dir, filename)
    
    # Capture the image
    cmd = ['libcamera-still', '-o', output_path]
    subprocess.run(cmd, check=True)
    print(f"Image saved to: {output_path}")

if __name__ == "__main__":
    # Example usage: capturing an image in the default directory with a prefix 'capture'
    capture_image(filename_prefix='capture')
