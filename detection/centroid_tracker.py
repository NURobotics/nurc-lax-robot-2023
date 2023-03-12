from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

# TODO: read article that centroid tracker code is based on:
#  https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
#  Also read about opencv inbuilt trackers - https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/

class CentroidTracker:
    def __init__(self, maxDisappeared=50):
        # initialize unique object ID
        self.nextObjectID = 0

        # TODO: Might be worth just creating an object class
        #  with an objectID and objectTracker field to clarify the code
        #  reread this comment once you're more familiar with code
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        # TODO: check whether we actually need self.bbox,
        #  I'm pretty sure tracker object has bounding box attribute
        self.bbox = OrderedDict()

        # store the number of frames an object can be marked "disappeared" before it is deregistered
        self.maxDisappeared = maxDisappeared

    # registering a new object using next available ID to store its centroid
    # TODO: dont need centroid as input variable
    def register(self, centroid, bbox):
        self.nextObjectID += 1
        # TODO: Instantiate tracker object at the bbox
        # TODO: Set self.objects[self.nextObjectID] = tracker object
        self.objects[self.nextObjectID] = centroid  # remove once using opencv tracker
        self.disappeared[self.nextObjectID] = 0
        self.bbox[self.nextObjectID] = bbox

    # de-registering an object by deleting object ID from both dictionaries
    def deregister(self, objectID):
        # TODO: Check if this is the right way to remove a tracker object
        del self.objects[objectID]
        del self.disappeared[objectID]
        del self.bbox[objectID]

    # update state every frame
    def update(self, frame, boxes):
        # TODO: for tracker in dictionary of trackers
        #  update tracker
        # if no current bounding boxes, de-register any object past limit and return early
        if len(boxes) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1

                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)

            return self.bbox

        # calculate centroid of each bounding box and organize in a numpy array
        inputCentroids = np.zeros((len(boxes), 2), dtype="int")
        inputRects = []
        for(i, (x, y, w, h)) in enumerate(boxes):
            cX = int(x + (w * 0.5))
            cY = int(y + (h * 0.5))
            inputCentroids[i] = (cX, cY)
            inputRects.append(boxes[i])

        # if currently not tracking any objects, register the centroids
        # TODO: dont need centroid as input variable
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i], inputRects[i])

        # otherwise, objects are being tracked so need to update centroids
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            # compute distance between each pair of object centroids and input centroids
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            # TODO: Not immediate concern, but maybe bipartite matching instead of this?
            #  Not important, do this last

            # find smallest value in each row, sort row indexes by minimum values
            rows = D.min(axis=1).argsort()

            # find smallest value in each column and sort based on ordered rows
            cols = D.argmin(axis=1)[rows]

            # keep track of rows and columns already examined
            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue

                # update centroid and disappeared counter
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.bbox[objectID] = inputRects[col]
                self.disappeared[objectID] = 0

                usedRows.add(row)
                usedCols.add(col)

            # compute unexamined rows and columns
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # in the event that there are more object centroids than input centroids
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)

            # in the event that there are more input centroids than object centroids
            else:
                # TODO: dont need centroid as input variable
                for col in unusedCols:
                    self.register(inputCentroids[col], inputRects[col])

        return self.bbox
