import cv2
import os


def get_new_image_counter(path):
    files = 0
    for _, _, filenames in os.walk(path):
        files += len(filenames)
    return files + 1


def supported_resolutions():
    camera_1 = cv2.VideoCapture(0)
    resolutions = []
    for width in range(640, 2048, 128):
        for height in range(640, 2048, 128):
            camera_1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            camera_1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            res = [camera_1.get(cv2.CAP_PROP_FRAME_WIDTH), camera_1.get(cv2.CAP_PROP_FRAME_HEIGHT)]
            resolutions.append(res)


def get_cameras_ids(cameras=10):
    cam_id = []
    '''Search 10 ports for cameras and store camera id if exists'''
    for i in range(cameras):
        camera = cv2.VideoCapture(i)

        found, frame = camera.read()
        if found:
            cam_id.append(i)
            camera.release()
        i += 1
    return cam_id


if __name__ == '__main__':
    width = 960 # 1920
    height = 720 # 1080
    camera_index = 0

    cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
    print 'Welcome to Webcam Capture - Developed by J. Atanbori'
    print 'Initialising Camera ', camera_index, '. Please wait ...'
    capture = cv2.VideoCapture(camera_index)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, 30)

    while True:
        found, frame = capture.read()
        if not found:
            print 'No cameras detected. Please ensure the cameras are turned on...'
            cv2.waitKey(5000)
            break
        frame = cv2.putText(frame, "Source: Camera-" + str(camera_index), (50, 50), cv2.FONT_ITALIC, 1, 255)
        cv2.imshow('Camera', frame)
        c = cv2.waitKey(10)
        if c == ord('n'):  # in "n" key is pressed while the popup window is in focus
            '''release the previous camera'''
            capture.release()
            print 'Initialising Camera ', camera_index, '. Please wait ...'
            camera_index += 1  # try the next camera index
            capture = cv2.VideoCapture(camera_index)
            found_again, frame = capture.read()
            frame = cv2.putText(frame, "Source: Camera-" + str(camera_index), (50, 50), cv2.FONT_ITALIC, 1, 255)
            if not found_again:  # if the next camera index didn't work, reset to 0.
                camera_index = 0
                print 'Initialising Camera ', camera_index, '. Please wait ...'
                capture = cv2.VideoCapture(camera_index)
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                capture.set(cv2.CAP_PROP_FPS, 30)

        elif c == 27:  # esc to exit
            break
        elif c == ord('s'):  # save images
            cameras = get_cameras_ids(cameras=10)
            capture.release()
            '''create a folder with name camera index if not exist'''
            img_path = 'captured_images/camera' + str(camera_index)
            '''Get the unique id to save the file'''
            img_counter = get_new_image_counter(img_path)

            '''************Save images from all the cameras****************'''
            for cam in cameras:
                '''create a folder with name camera index if not exist'''
                img_path = 'captured_images/camera' + str(cam)
                if not os.path.exists(img_path):
                    os.makedirs(img_path)

                '''Open the camera to capture the image'''
                capture = cv2.VideoCapture(cam)
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                capture.set(cv2.CAP_PROP_FPS, 30)
                _, frame = capture.read()

                filename = str(img_counter) + '.png'
                print 'Saving Camera ', str(cam), ' to: ', os.path.join(img_path, filename)
                cv2.imwrite(os.path.join(img_path, filename), frame)

            print 'images have been successfully saved'