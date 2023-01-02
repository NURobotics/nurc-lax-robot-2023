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
	for box in bboxes:
		x, y, w, h = box[1]
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
	return img
