### conversion_yolo_obj_detection

After converting the annotations from csv format to COCO format. Now we need the annotations for object detection based on YOLO format. So to convert the annotations from COCO to YOLO format **coco_to_yolo.py** script is used.

To run the file, run the following command:

    python coco_to_yolo.py --coco_ann_file [path/to/coco-annotation-file] --image_dir [path/to/image-directory] --output_dir [path/to/output-directory]
    
