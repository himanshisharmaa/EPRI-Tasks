import pandas as pd 
import json
import os
import argparse
from datetime import datetime
import cv2

def create_coco_structure():
    return {
        "info": {
            "description": "Dataset converted to COCO format",
            "url": "",
            "version": "1.0",
            "year": datetime.now().year,
            "contributor": "",
            "date_created": datetime.now().isoformat()
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

def add_category(categories, name, category_id):
    if name not in [cat["name"] for cat in categories]:
        categories.append({
            "id": category_id,
            "name": name,
            "supercategory": "none"
        })

def csv_to_coco(csv_file, image_dir, output_path):
    coco_data = create_coco_structure()
    categories = []
    annotations = []
    image_info = {}
    category_id_mapping = {}
    annotation_id = 1

    df = pd.read_csv(csv_file, delimiter=",")
    print(df.columns)
    for _, row in df.iterrows():
        
        external_id = row["External ID"]
        print(external_id)
        image_path = os.path.join(image_dir, external_id)
        if not os.path.exists(image_path):
            print(f"Image {image_path} not found")
            continue

        if external_id not in image_info:
            img = cv2.imread(image_path)
            height, width = img.shape[:2]
            image_info[external_id] = {
                "id": len(image_info) + 1,
                "file_name": external_id,
                "height": height,
                "width": width
            }
            coco_data["images"].append(image_info[external_id])

        annotation_data = json.loads(row["Label"].replace("'", "\""))
        for obj in annotation_data["objects"]:
            category_name = obj["value"]
            if category_name not in category_id_mapping:
                category_id_mapping[category_name] = len(category_id_mapping) + 1
                add_category(categories, category_name, category_id_mapping[category_name])

            segmentation = []
            bbox = []
            if "polygon" in obj:
          
                segmentation = [coord for point in obj["polygon"] for coord in (point['x'], point['y'])]
                x_coords = [point["x"] for point in obj["polygon"]]
                y_coords = [point["y"] for point in obj["polygon"]]
                bbox = [min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)]
            elif "line" in obj:
               
                print(f"Warning: Line found for category {category_name}, converting to closed polygon")
                line_points = obj["line"]
                segmentation = [coord for point in line_points for coord in (point["x"], point["y"])]
                segmentation += [line_points[0]["x"], line_points[0]["y"]]  # Close the line by adding the start point
                x_coords = [point["x"] for point in line_points]
                y_coords = [point["y"] for point in line_points]
                bbox = [min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)]
            else: 
                continue

            annotations.append({
                "id": annotation_id,
                "image_id": image_info[external_id]["id"],
                "category_id": category_id_mapping[category_name],
                "segmentation": [segmentation],
                "area": bbox[2] * bbox[3],
                "bbox": bbox,
                "iscrowd": 0
            })
            annotation_id += 1
    
    coco_data["annotations"] = annotations
    coco_data["categories"] = categories
    output_dir = os.path.join(output_path, "Annotations")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, os.path.basename(image_dir) + ".json")
    with open(output_file, "w") as json_file:
        json.dump(coco_data, json_file, indent=4)
    
    print(f"COCO format JSON saved to {output_file}")

if __name__ == "__main__":
    dir = os.getcwd()
    parser = argparse.ArgumentParser(description="Convert CSV annotations to COCO format")
    parser.add_argument('--csv_file', required=True, help="Path to the CSV file with annotations")
    parser.add_argument('--image_dir', required=True, help="Directory with images")
    args = vars(parser.parse_args())
    csv_to_coco(args["csv_file"], os.path.join(dir, args["image_dir"]), dir)
