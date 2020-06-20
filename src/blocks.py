import cv2
import numpy as np
from PIL import Image, ImageDraw

path = 'temp/scanned'

def get_graph(item):

    # Take a copy of the image to extract the item later
    image = cv2.imread(path + '.jpg')
    original = image.copy()
    cut = original[:]
    count = 0

    # Dilate the image to remove the text
    dilated_img = cv2.dilate(image, np.ones((7,7), np.uint8))
    #cv2.imwrite("temp/dilate.jpg", dilated_img)

    # In order to further remove any text on the page we apply smoothing
    bg_img = cv2.medianBlur(dilated_img, 21) 
    #cv2.imwrite("temp/blurs.jpg", bg_img)

    # Form an image that is difference between the orignal and the blurred
    diff_img = 255 - cv2.absdiff(image, bg_img)
    norm_img = diff_img.copy()
    #cv2.imwrite("temp/diff.jpg", norm_img)

    # Normalise and truncate to bring back the dynamic range of the image and remove gray pixels
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 255, 0, cv2.THRESH_TRUNC)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    #cv2.imwrite("temp/remove.jpg", norm_img)

    # Apply a grayscale and OTSU threshold
    gray = cv2.cvtColor(thr_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #cv2.imwrite("temp/otsu.jpg", thresh)

    # Dilate with a morphological transformation
    if item == "graphs":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (23,10))
        dilate = cv2.dilate(thresh, kernel, iterations=1)
    elif item == "images":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (45,15))
        dilate = cv2.dilate(thresh, kernel, iterations=2)
        #cv2.imwrite("temp/morph.jpg", dilate)
    else:
        print("ERR - Invalid call")

    # Find contours and remove those that seem to represent objects that are not items
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        cv2.rectangle(image, (x,y), (x + w,y + h), (36,255,12), 3)

        if cv2.contourArea(c) >= 10000:
            cut = original[y:y+h, x:x+w]
            cv2.imwrite("temp/blocks/"  + str(count) + '.jpg', cut)
            count = count + 1

        if w/h > 2 and area < 10000:
            cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

    #cv2.imwrite("temp/contour.jpg", image)

    # Find all the contours remaining that represent the items
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x,y), (x + w,y + h), (36,255,12), 3)

    #ordered_cnts = max(cnts, key=cv2.contourArea)
    sort_cnts = sorted(cnts, key=lambda x: cv2.contourArea(x))
    count = 0

    # Capture the item from the page and remove it from the original
    for sc in sort_cnts:
        #if cv2.contourArea(sc) >= 100000 and cv2.contourArea(sc) <= 7000000:
        if cv2.contourArea(sc) >= 200000 and cv2.contourArea(sc) <= 250000:
            x,y,w,h = cv2.boundingRect(sc)
            points = []
            points.append(x)
            points.append(y)
            points.append(x + w)
            points.append(y + h)
            cut = original[y:y+h, x:x+w]
            cv2.imwrite("temp/blocks/" + item + "/"  + str(count) + '.jpg', cut)
            remove(points, item, count)
            count = count + 1

    return 


def remove(points, item, count):
    
    # Remove graph or image from page
    t = Image.open(path + '.jpg').convert("RGB")
    draw = ImageDraw.Draw(t)
    draw.rectangle(((points[0],points[1]), (points[2],points[3])), fill="white")
    t.save(path + '.jpg', "JPEG")

    return

def get():

    print("pkg_ITEMS - Extracting graphs and images")

    get_graph("images")
    #get_graph("graph")

    return


if __name__ == '__main__':

    get_graph("images")

    #cv2.imshow('remove', image)
    #cv2.imshow('thresh', thresh)
    #cv2.imshow('dilate', dilate)
    #cv2.imshow('ROI', ROI)
    
    #cv2.imwrite('temp/overlay.jpg', image)
    #cv2.imwrite('temp/dill.jpg', dilate)
    #cv2.imwrite('temp/cut.jpg', cut)
    
    #cv2.waitKey()
