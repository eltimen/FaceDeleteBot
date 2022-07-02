import sys
import cv2
import numpy as np

model_path = "models/opencv_face_detector.caffemodel"
config_path = "models/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(config_path, model_path)
net_input_shape = 300, 300


def detect_faces(img):
    """Detect faces on the image and return bounding rectangles"""
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, net_input_shape), 1.0, net_input_shape, (104.0, 117.0, 123.0))

    net.setInput(blob)
    output = net.forward()
    face_rectangles = []
    for i in range(output.shape[2]):
        confidence = output[0, 0, i, 2]
        if confidence > 0.45:
            box = output[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x, y, x1, y1) = box.astype('int')
            face_rectangles.append(((x, y), (x1, y1)))

    return face_rectangles


def blur_convex_hulls(image, hulls):
    """Blur the specified convex hulls in the image"""
    blurred_image = cv2.GaussianBlur(image, (93, 93), 20)
    mask = np.zeros(image.shape, np.uint8)

    for hull in hulls:
        roi_corners = np.reshape(np.array(hull, dtype=np.int32), (1, 1, -1, 2))
        cv2.fillPoly(mask, roi_corners, (255,) * image.shape[2])
    mask_inverse = np.ones(mask.shape).astype(np.uint8) * 255 - mask
    return cv2.bitwise_and(blurred_image, mask) + cv2.bitwise_and(image, mask_inverse)


def blur_rects(image, rects):
    """Blur the specified rectangles in the image"""
    output_image = image.copy()
    for rect in rects:
        x, y = rect[0]
        x1, y1 = rect[1]
        output_image[y:y1, x:x1] = cv2.GaussianBlur(image[y:y1, x:x1], (93, 93), 20)
    return output_image


def process_image(path):
    image = cv2.imread(path)
    if image is None:
        return None

    face_rectangles = detect_faces(image)
    out_image = blur_rects(image, face_rectangles)

    try:
        out_image_path = path[:path.rindex('.')] + '_out' + path[path.rindex('.'):]
    except ValueError:
        # if no extension in filename
        out_image_path = path + '_out.png'
    cv2.imwrite(out_image_path, out_image)
    return out_image_path


if __name__ == '__main__':
    image_path = sys.argv[1]
    out_image_path = process_image(image_path)
    cv2.imshow("image", cv2.imread(out_image_path))
    cv2.waitKey(0)
