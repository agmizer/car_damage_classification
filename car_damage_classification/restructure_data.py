"""
Script to convert CarDD COCO format dataset to directory structure
compatible with flow_from_directory.

This script reads the COCO annotations and organizes images into
subdirectories based on their damage type labels.
"""

import json
import os
import shutil
from collections import defaultdict

def convert_cardd_to_directory(coco_dir, output_dir):
    """
    Convert CarDD COCO format to directory structure.
    
    Args:
        coco_dir: Path to CarDD_COCO directory
        output_dir: Path where converted dataset will be saved
    """
    # Paths
    train_json = os.path.join(coco_dir, 'annotations', 'instances_train2017.json')
    val_json = os.path.join(coco_dir, 'annotations', 'instances_val2017.json')
    test_json = os.path.join(coco_dir, 'annotations', 'instances_test2017.json')

    train_img_dir = os.path.join(coco_dir, 'train2017')
    val_img_dir = os.path.join(coco_dir, 'val2017')
    test_img_dir = os.path.join(coco_dir, 'test2017')

    # Create output directories
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    def process_split(json_path, img_dir, split_name):
        """Process a single split (train/val/test)"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Create category mapping
        category_map = {cat['id']: cat['name'] for cat in data['categories']}

        # Map image_id to list of category names
        image_categories = defaultdict(set)

        # Process annotations
        for ann in data['annotations']:
            image_id = ann['image_id']
            category_id = ann['category_id']
            category_name = category_map[category_id]
            image_categories[image_id].add(category_name)

        # Create image_id to filename mapping
        image_map = {img['id']: img['file_name'] for img in data['images']}

        # Organize images by their primary category (first category found)
        # If an image has multiple damage types, we'll use the first one
        for image_id, categories in image_categories.items():
            filename = image_map[image_id]
            # Use the first category (or you could use a different strategy)
            category = list(categories)[0]

            # Create category directory
            category_dir = os.path.join(output_dir, split_name, category)
            os.makedirs(category_dir, exist_ok=True)

            # Copy image
            src = os.path.join(img_dir, filename)
            dst = os.path.join(category_dir, filename)

            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copied {filename} to {split_name}/{category}/")

    # Process each split
    print("Processing training set...")
    process_split(train_json, train_img_dir, 'train')

    print("\nProcessing validation set...")
    process_split(val_json, val_img_dir, 'val')

    print("\nProcessing test set...")
    process_split(test_json, test_img_dir, 'test')

    print(f"\nConversion complete! Dataset saved to: {output_dir}")

if __name__ == "__main__":
    # Adjust these paths as needed
    SRC_DIR = "../CarDD_release/CarDD_COCO"
    OUTPUT_DIR = "../dataset_cardd"

    convert_cardd_to_directory(SRC_DIR, OUTPUT_DIR)
