import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def load_cv2_image(path):
    return cv2.imread(path)


def resize_cv2_image(image, ratio):
    h, w = image.shape[:2]
    src = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]], np.float32)
    dest = src * ratio
    affine = cv2.getAffineTransform(src, dest)
    img3 = cv2.warpAffine(
        image, affine, (int(float(w)*ratio), int(float(h)*ratio)), cv2.INTER_LANCZOS4)
    return img3


def cv2_to_pil_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    new_image = image.copy()
    return Image.fromarray(new_image)


image = load_cv2_image("1周目/cat.jpg")
image = resize_cv2_image(image, 0.1)
image = cv2_to_pil_image(image)
image.show()
