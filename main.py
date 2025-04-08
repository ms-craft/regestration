import cv2
import os
def find_features(img1):
    correct_matches_dct = {}
    directory = 'E:\maxim\cv2'
    for image in os.listdir(directory):
        img2 = cv2.imread(directory+image, 0)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        correct_matches = []
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                correct_matches.append([m])
                correct_matches_dct[image.split('.')[0]] = len(correct_matches)
    correct_matches_dct = dict(sorted(correct_matches_dct.items(),
             key=lambda item: item[1], reverse=True))
    return list(correct_matches_dct.keys())[0]


def find_contours_of_cards(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    T, thresh_img = cv2.threshold(blurred, 215, 255, 
                                  cv2.THRESH_BINARY)
    (_, cnts, _) = cv2.findContours(thresh_img, 
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    return cnts






def find_coordinates_of_cards(cnts, image):
    cards_coordinates = {}
    for i in range(0, len(cnts)):
        x, y, w, h = cv2.boundingRect(cnts[i])
        if w > 20 and h > 30:
            img_crop = image[y - 15:y + h + 15,
                             x - 15:x + w + 15]
            cards_name = find_features(img_crop)
            cards_coordinates[cards_name] = (x - 15, 
                     y - 15, x + w + 15, y + h + 15)
    return cards_coordinates
img = cv2.imread('main.png', cv2.IMREAD_GRAYSCALE)
print(find_features(img))

cv2.imshow('main', img)
cv2.waitKey(0)