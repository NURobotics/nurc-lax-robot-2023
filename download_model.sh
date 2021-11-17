#!/bin/bash -e

mkdir -p yolo-coco
curl https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names -o yolo-coco/coco.names
curl https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg -o yolo-coco/yolov3.cfg
curl https://pjreddie.com/media/files/yolov3.weights -o yolo-coco/yolov3.weights
