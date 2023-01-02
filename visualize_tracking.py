import cv2
import numpy as np
import argparse
import os
import imutils
import time
import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
from centroid_tracker import CentroidTracker
import matplotlib.pyplot as plt


def visualize(frame, bboxes):
	img = frame.copy()

	for id, box in bboxes:
		x, y, w, h = box
		text = "ID: {}".format(id)
		cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
	return img
