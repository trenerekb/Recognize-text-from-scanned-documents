import align
import cv2


def filter_img(crop_img):
    # Преобразуем преобразованный результат в значение серого
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # cv2.imwrite('blur.jpg', blur)
    scanDenois = cv2.fastNlMeansDenoising(blur, None, 10, 1, 21)
    # cv2.imwrite('Denoising.jpg', scanDenois)
    # thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    scanThresh = cv2.bitwise_not(scanDenois)
    # cv2.imwrite(f'scanThresh.jpg', scanThresh)
    return scanThresh

    # scanGray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('gray.jpg', scanGray)
    # scanDenois = cv2.fastNlMeansDenoising(scanGray, None, 30, 3, 21)
    # cv2.imwrite('Denoising.jpg', scanGray)
    # # scanBilater = cv2.bilateralFilter(scanDenois, 20, 35, 35)
    # # cv2.imwrite(f'bilater.jpg', scanBilater)
    # return scanDenois


def processing_scan_img(count_pages):
    finished_img = []

    for i in range(count_pages):
        image = cv2.imread(f'page{i+1}.jpg')
        align_img = align.deskew(image)
        crop_img = align_img[0:1070, 300:5650]
        # cv2.imwrite(f'crop_img{i}.jpg', crop_img)
        finish_img = filter_img(crop_img)
        # cv2.imwrite(f'finish_img{i+1}.jpg', finish_img)
        finished_img.append(finish_img)

    return finished_img


def filter_img_hand(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    scanDenois = cv2.fastNlMeansDenoising(blur, None, 30, 1, 30)
    # cv2.imwrite('HandDenoising.jpg', scanDenois)
    # thresh = cv2.adaptiveThreshold(scanDenois, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    scanThresh = cv2.bitwise_not(scanDenois)
    # cv2.imwrite(f'thresh.jpg', thresh)
    return scanThresh