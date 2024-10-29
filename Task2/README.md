## - conversion_yolo_obj_detection

After converting the annotations from csv format to COCO format in Task1. Now we need the annotations for object detection based on YOLO format. So to convert the annotations from COCO to YOLO format **coco_to_yolo.py** script is used.

To run the file, run the following command:

    python coco_to_yolo.py --coco_ann_file [path/to/coco-annotation-file] --image_dir [path/to/image-directory] --output_dir [path/to/output-directory]


## - conversion_yolo_instance_seg

IF we need to convert the annotations from COCO annotation format to YOLO format for instance segmentation, **annotation_conversion.py** script is used.

To run the file, run the following command:

        python annotation_conversion.py --image_dir [path/to/image-directory] --input_path [path/to/annotation-file-or-directory] --target_format YOLO --task instance_segmentation --output_dir [path/to/output-directory]


## FiftyOneVisualization

After converting the annotations to desired format, visualization for each annotation type is done with FiftyOne. **FiftyOne_Circuit.ipynb** file contains visualization code for COCO and YOLO(object-detection and instance-segmentation) format on EPRI dataset.


