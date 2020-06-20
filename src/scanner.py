#!python
# coding: utf-8

# Imports
import numpy as np 
import cv2
import time
import audio
from multiprocessing import Process


def run():

    print("pkg_SCANNER - Scanning Page")
    start = time.time()
    
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('temp/feed.mp4')
    #cap.set(10,160)
    #imgw = 600
    #imgl = 800
    vidw = 640
    vidl = 480
    cont = True
    consistent = 0

    while cont:
        # Use live video feed
        ret, frame = cap.read()

        # Use image 
        #image = cv2.imread("images/1.jpg", 1)

        # Resize the image into a processable size 
        #image = cv2.resize(image,(imgw,imgl)) # Image
        image = cv2.resize(frame,(vidw,vidl)) # Video

        # Apply grayscale processing to the image
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use Gaussian Blurr to smooth the image 
        blurr = cv2.GaussianBlur(grey, (5,5),0)

        # Use Canny to identifiy edges within the image
        edge = cv2.Canny(blurr, 0, 50)   
        # Use Adaptive Threshold to identifiy edges within the image
        threshold = cv2.adaptiveThreshold(blurr,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2) 

        # Find all the contours and keep them in a list
        contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Sort the contours sort by decreasing area
        contours = sorted(contours, key=cv2.contourArea, reverse= True)

        # Using the largest 4 contours we now estimate the shape of the page as a polygon
        for i in contours:
            elip =  cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i,0.08*elip, True)

            if len(approx) == 4 : 
                page = approx 
                break

        # Draw the contour on the image
        cv2.drawContours(image, [page], -1, (0, 255, 0), 2)

        # Restructure the matrix to a 2x2
        page = page.reshape((4,2))

        # Identify the corners of the page and assign them to dedicated variables
        det_page = np.zeros((4,2), dtype="float32")

        sum_ = page.sum(axis = 1)
        det_page[0] = page[np.argmin(sum_)]
        det_page[2] = page[np.argmax(sum_)]

        diff_ = np.diff(page, axis=1)
        det_page[1] = page[np.argmin(diff_)]
        det_page[3] = page[np.argmax(diff_)]

        (tl,tr,br,bl) = det_page

        # Using the distance we can find the lengths
        dist1 = np.linalg.norm(br-bl)
        dist2 = np.linalg.norm(tr-tl)
        maxLen = max(int(dist1),int(dist2))

        dist3 = np.linalg.norm(tr-br)
        dist4 = np.linalg.norm(tl-bl)
        maxHeight = max(int(dist3), int(dist4))

        distance = np.array([[0,0],[maxLen-1, 0],[maxLen-1, maxHeight-1], [0, maxHeight-1]], dtype="float32")

        # Using the distances we can now transform the image
        pt = cv2.getPerspectiveTransform(det_page, distance)
        wp = cv2.warpPerspective(image, pt, (maxLen, maxHeight))

        # Conver to black and white and resize
        identified_page = cv2.cvtColor(wp, cv2.COLOR_BGR2GRAY)
        (thresh, baw) = cv2.threshold(identified_page, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #identified_page = cv2.resize(identified_page,(imgw,imgl))
        identified_page = cv2.resize(identified_page,(vidw,vidl))

        # Display processed stages of image
        show(frame, edge, threshold, image, identified_page, baw)

        # Calculate current area and target area
        # A 60% threshold is used here
        page_area = maxHeight * maxLen
        #perc_aim = (imgw * imgl) * 0.6
        perc_aim = int((vidw * vidl) * 0.6)

        # Save the images that need to be used further based on area percentage
        # Give feedback if the page has been found, too far away, or if it cannot be found
        if page_area >= perc_aim:
            print(consistent)
            consistent = consistent + 1
            time.sleep(0.01)
            if consistent == 100:
                print("")
                p = Process(target = audio.go, args = ("key", "scanner_001"))
                p.daemon = True
                p.start()
            elif consistent >= 300:
                # Document scanned and stored
                cv2.imwrite("temp/scanned.jpg", identified_page)
                cv2.destroyAllWindows()
                audio.go("key", "scanner_002")
                cont = False
        elif page_area <= perc_aim:
            # Document is too small 
            consistent = 0
            p = Process(target = audio.go, args = ("key", "scanner_003"))
            p.daemon = True
            p.start()
        else:   
            # Document cannot be found
            consistent = 0
            p = Process(target = audio.go, args = ("key", "scanner_004"))
            p.daemon = True
            p.start()


        # Close all windows with any keyboard press
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            cap.release()
            print("False")
            return False
        
        # Timeout closure
        if time.time() - start >= 30:
            audio.go("key", "scanner_005")
            print(time.time() - start)
            cap.release()
            print("False")
            return False
        
    cap.release()
    print("True")
    return True


def show(frame, edge, threshold, image, identified_page, baw):

    #cv2.imshow("Feed",frame)
    #cv2.imshow("Canny",edge)
    #cv2.imshow("Threshold",threshold)
    #cv2.imshow("Black and White", baw)
    cv2.imshow("Contour Overlay", image)
    cv2.imshow("FINAL", identified_page)

    return


if __name__ == '__main__':

    run()

    while True:
        pass

