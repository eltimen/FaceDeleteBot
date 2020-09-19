import sys
import cv2
import dlib
import numpy as np
from imutils import face_utils

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")


def detect_faces(image):
    face_hulls = []
    subjects = detect(image, 0)
    for subject in subjects:
        shape = predict(image, subject)
        shape = face_utils.shape_to_np(shape)
        hull = cv2.convexHull(shape)
        face_hulls.append(hull)
    return face_hulls


def blur_convex_hulls(image, hulls):
    blurred_image = cv2.GaussianBlur(image, (93, 93), 20)
    mask = np.zeros(image.shape, np.uint8)

    for hull in hulls:
        roi_corners = np.reshape(np.array(hull, dtype=np.int32), (1, 1, -1, 2))
        cv2.fillPoly(mask, roi_corners, (255,) * image.shape[2])
    mask_inverse = np.ones(mask.shape).astype(np.uint8) * 255 - mask
    return cv2.bitwise_and(blurred_image, mask) + cv2.bitwise_and(image, mask_inverse)


def process_image(path):
    image = cv2.imread(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    image = blur_convex_hulls(image, faces)

    try:
        out_image_path = path[:path.rindex('.')] + '_out' + path[path.rindex('.'):]
    except ValueError:
        out_image_path = path + '.png'
    cv2.imwrite(out_image_path, image)
    return out_image_path


if __name__ == '__main__':
    image_path = sys.argv[1]
    out_image_path = process_image(image_path)
    cv2.imshow("image", cv2.imread(out_image_path))
    cv2.waitKey(0)
