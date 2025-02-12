from PIL import Image
import tempfile
import cv2
import numpy as np

# set dpi
def set_dpi(img_path):
    im = Image.open(img_path)
    factor = min(1.0, 1024.0 / im.size[0])
    factor = min(factor, 1024.0 / im.size[1])
    width = int(im.size[0] * factor)
    height = int(im.size[1] * factor)
    im_resized = im.resize((width, height), Image.Resampling.LANCZOS)
    tpimg = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    im_resized.save(tpimg.name, dpi=(300, 300))
    return tpimg.name

# Normalization
def normalize(img):
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    return img

# remove noise
def remove_noise(img, h=10, hForColor=10):
    img = cv2.fastNlMeansDenoisingColored(img, None, h, hForColor, 7, 21)
    return img

# skeletonize
def skeletonize(img):
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    return img

# grayscale
def grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# thresholding
def adaptivethresholding(img):
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img

def thresholding(img, threshold=127):
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return img

# deskew objects
def correct_skew(img):
    gray = img
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 280)
    if lines is None:
        print("No lines detected. Using default angle.")
        return img
    angles = []
    for line in lines:
        _, theta = line[0]
        angle = theta * 180 / np.pi
        angles.append(angle)
    median_angle = np.median(angles) - 90
    rotated = rotate_image(img, median_angle)
    return rotated


def rotate_image(img, angle):
    height, width = img.shape[:2]
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

if __name__ == "__main__":
    img_path = set_dpi('pics/6.jpg')
    img = cv2.imread(img_path)
    img = normalize(img)
    img = remove_noise(img)
    img = skeletonize(img)
    img = grayscale(img)
    img = adaptivethresholding(img)
    img = correct_skew(img)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()