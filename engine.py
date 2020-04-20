import sys
import cv2
import dlib
from imutils import face_utils
   
def detect_faces(image):
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
 
    face_hulls = []
    subjects = detect(image, 0)
    for subject in subjects:
        shape = predict(image, subject)
        shape = face_utils.shape_to_np(shape)#converting to NumPy Array
        hull = cv2.convexHull(shape)
        face_hulls.append(hull)
    return face_hulls; 

def process_image(path):
    image = cv2.imread(path) 
    #print('image size: {}'.format(image.shape))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    
    for face in faces:
        cv2.drawContours(image, [face], -1, (0, 0, 0), cv2.FILLED)
    
    #save_path = path[:path.rindex('.')] + '_out' + path[path.rindex('.'):]
    save_path = path + '_out.jpg'
    cv2.imwrite(save_path, image)
    return save_path

if __name__ == '__main__':
    image_path = sys.argv[1]
    modified_path = process_image(image_path)
    cv2.imshow("image", cv2.imread(modified_path))
    cv2.waitKey(0)