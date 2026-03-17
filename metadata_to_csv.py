import os
import csv
import logging
from PIL import Image
from PIL.ExifTags import TAGS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_metadata(file_path):
    """Extract basic metadata from image file using Pillow."""
    try:
        with Image.open(file_path) as image:
            metadata = {
                'filename': os.path.basename(file_path),
                'filepath': file_path,
                'format': image.format,
                'size': f"{image.size[0]}x{image.size[1]}",
                'mode': image.mode
            }
            
            # Extract EXIF data if available
            exifdata = image.getexif()
            if exifdata:
                for tag_id, value in exifdata.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[f'exif_{tag}'] = str(value)
            
            return metadata
    except Exception as e:
        logging.error(f"Error reading image {file_path}: {e}")
        return None

def save_metadata_to_csv(image_dir, output_csv):
    """Extract metadata from images in the specified directory and save it to a CSV file."""
    if not os.path.isdir(image_dir):
        logging.error(f"The directory {image_dir} does not exist.")
        return

    # Prepare to collect metadata
    metadata_list = []
    all_fieldnames = set()
    
    # Walk through the directory and process each image file
    for root, dirs, files in os.walk(image_dir):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                file_path = os.path.join(root, filename)
                # Extract metadata using the local extractor function
                metadata = extract_metadata(file_path)
                if metadata:
                    metadata_list.append(metadata)
                    all_fieldnames.update(metadata.keys())
                    logging.info(f"Extracted metadata from {file_path}")
                else:
                    logging.warning(f"No metadata found for {file_path}")

    # Write the collected metadata to a CSV file
    if metadata_list:
        try:
            with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = sorted(all_fieldnames)  # Use all collected fieldnames
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for data in metadata_list:
                    writer.writerow(data)

            logging.info(f"Metadata saved to {output_csv}")
        except IOError as e:
            logging.error(f"Could not write to CSV file {output_csv}: {e}")
    else:
        logging.info("No metadata to save.")

if __name__ == "__main__":
    # Example usage: Adjust the paths as necessary
    image_directory = "."
    output_file = "output_metadata.csv"
    
    if os.path.exists(image_directory):
        save_metadata_to_csv(image_directory, output_file)
    else:
        print(f"Directory {image_directory} does not exist. Please provide a valid path.")

# TODO: 
# - Add support for more image formats if needed.
# - Consider adding CLI arguments for directory and output file.
# - Implement more detailed error handling for different types of exceptions.
