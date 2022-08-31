import cv2


def getSkewAngle(cvImage) -> float:
    """
    Calculate skew angle of an image.
    Input: image
    Output: angle
    """

    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    # thresh = cv2.bilateralFilter(blur, 15, 25, 35)
    thresh = cv2.Canny(blur, 10, 300)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours , cv2.RETR_LIST RETR_TREE RETR_EXTERNAL
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Uncomment next 2 lines to display largest contour used to determine skew angle
    cv2.drawContours(newImage, [largestContour], 0, (0,255,0), 3)
    # Image.fromarray(newImage).show()

    # Determine the angle.
    angle = minAreaRect[-1]

    if angle > 45:
        angle = angle - 90

    return angle


# Rotate image using the angle from the above function
def rotateImage(cvImage, angle: float):
    """
    Rotates image
    Input: image, angle to rotate
    Output: rotated image
    """

    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return newImage


def flip90(raw_img):
    height, width, channels = raw_img.shape  # (5000, 1133, 3)
    center = (width/2, width/2)
    angle = 90
    M = cv2.getRotationMatrix2D(center, angle, 1)
    img_rotated_90 = cv2.warpAffine(raw_img, M, (height, width))

    return img_rotated_90


# Deskew image using the above functions
def deskew(cvImage):
    """
    Straightens (de-skews) an image
    Input: image
    Output: straigntened image
    """
    img_rotated_90 = flip90(cvImage)
    crop_img = img_rotated_90[0:1070, 0:5600]
    angle = getSkewAngle(crop_img)

    return rotateImage(crop_img, angle)
