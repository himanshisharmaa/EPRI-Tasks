import json
import os
import argparse


dir=os.getcwd()
ap=argparse.ArgumentParser()
ap.add_argument("--coco_ann_file",required=True,help="Path to the COCO annotation file")
ap.add_argument("--output_dir",default=os.path.join(dir,"yolo_labels"),help="Path to output directory")
ap.add_argument("--image_dir",required=True,help="Path to image directory")
args=vars(ap.parse_args())

output_dir=args["output_dir"]
coco_ann_file=os.path.join(dir,args["coco_ann_file"])
image_dir=os.path.join(dir,args["image_dir"])
if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def convert_bbox_coco_to_yolo(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x_min, y_min, w, h = box
    x_center = x_min + w / 2.0
    y_center = y_min + h / 2.0
    x_center *= dw
    w *= dw
    y_center *= dh
    h *= dh
    return (x_center, y_center, w, h)

with open(coco_ann_file) as f:
    coco_data = json.load(f)

category_id_to_name = {category["id"]: category["name"] for category in coco_data["categories"]}
category_name_to_id = {name: i for i, name in enumerate(category_id_to_name.values())}

with open(os.path.join(output_dir, "classes.txt"), "w") as f:
    for category_name in category_name_to_id:
        f.write(f"{category_name}\n")



for image in coco_data["images"]:
    image_id = image["id"]
    file_name = os.path.splitext(image["file_name"])[0]  # Image filename without extension
    image_width = image["width"]
    image_height = image["height"]


    
    
    label_file_path = os.path.join(output_dir, f"{file_name}.txt")
    with open(label_file_path, "w") as label_file:
        
        for annotation in coco_data["annotations"]:
            if annotation["image_id"] == image_id:
                category_id = annotation["category_id"]
                yolo_class_id = category_name_to_id[category_id_to_name[category_id]]
                
                
                yolo_bbox = convert_bbox_coco_to_yolo(
                    (image_width, image_height),
                    annotation["bbox"]
                )
                label_file.write(f"{yolo_class_id} " + " ".join(map(str, yolo_bbox)) + "\n")

print("Conversion completed. YOLO annotations are saved in:", output_dir)