import os
import csv
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_metadata(image_path):
    """Extracts metadata from an image file."""
    metadata = {}
    try:
        image = Image.open(image_path)
        info = image.getexif()
        if info is not None:
            for tag_id, value in info.items():
                tag = TAGS.get(tag_id, tag_id)
                # Convert value to string to handle bytes, tuples, etc.
                metadata[tag] = str(value)
    except Exception as e:
        print(f"Error extracting metadata from {image_path}: {e}")
    return metadata

def scan_directory(directory):
    """Scans a directory and returns a list of image files."""
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return []
    
    image_files = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_files.append(os.path.join(root, file))
    
    return image_files

def save_to_csv(metadata_list, output_file):
    """Saves metadata to a CSV file."""
    if not metadata_list:
        print("No metadata to save.")
        return

    try:
        # Collect all possible fieldnames
        all_fieldnames = set()
        for metadata in metadata_list:
            all_fieldnames.update(metadata.keys())
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(all_fieldnames))
            writer.writeheader()
            for metadata in metadata_list:
                writer.writerow(metadata)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main(directory, output_file):
    """Main function to extract image metadata and save it to a CSV."""
    print(f"Scanning directory: {directory}")
    image_files = scan_directory(directory)
    print(f"Found {len(image_files)} image files.")
    
    metadata_list = []
    for image_path in image_files:
        metadata = extract_metadata(image_path)
        if metadata:  # Only add non-empty metadata
            metadata['File Name'] = os.path.basename(image_path)
            metadata['File Path'] = image_path
            metadata_list.append(metadata)

    save_to_csv(metadata_list, output_file)
    print(f"Metadata extraction complete. Saved to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extractor.py <directory> <output_file>")
        sys.exit(1)
    
    directory = sys.argv[1]
    output_file = sys.argv[2]
    
    main(directory, output_file)
