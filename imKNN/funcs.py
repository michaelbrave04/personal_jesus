import os
import pickle
from PIL import Image
import cv2
import numpy as np
from imutils import paths

loaded_model = pickle.load(open('model.sav', 'rb'))


def image_to_feature_vector(image, size=(32, 32)):
    # resize the image to a fixed size, then flatten the image into
    # a list of raw pixel intensities
    return cv2.resize(image, size).flatten()

def cut_frame(frame):
    y, x = frame.shape[:2]
    hx, hy = x // 2, y // 2
    ims = [frame[0:hy, 0:hx],
           frame[0:hy, hx:x],
           frame[hy:y, 0:hx],
           frame[hy:y, hx:x]]
    return ims

def classify(ims):
    global j
    pred = []
    for im in ims:
        pred.append(loaded_model.predict(image_to_feature_vector(im).reshape((1, -1))))
        # cv2.imwrite('D:/imKNN/imgs/ones/' + str(j) + '.jpeg', im)
        j += 1
        # cv2.imshow(*pred[-1], im)
    return pred



# пример запуска

imagePaths = list(paths.list_images('D:/imKNN/imgs/fours'))
# initialize the raw pixel intensities matrix, the features matrix,
# and labels list
rawImages = []

# loop over the input images
for (i, imagePath) in enumerate(imagePaths):
    # load the image and extract the class label (assuming that our
    # path as the format: /path/to/dataset/{class}.{image_num}.jpg
    image = cv2.imread(imagePath)
    rawImages.append(image)
    # show an update every 1,000 images
    if i > 0 and i % 1000 == 0:
        print("[INFO] processed {}/{}".format(i, len(imagePaths)))

# show some information on the memory consumed by the raw images
# matrix and features matrix
rawImages = np.array(rawImages)
for i in rawImages:
    print(*classify(i))
    cv2.imshow('all', i)
    cv2.waitKey(0)
