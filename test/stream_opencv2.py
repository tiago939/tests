import numpy as np
import cv2 as cv

camera0 = 'http://187.19.166.182/mjpg/video.mjpg'
camera1 = 'http://187.19.166.182/mjpg/video.mjpg'
camera2 = 'http://73.182.17.160:8081/mjpg/video.mjpg'
camera3 = 'http://47.181.86.62:8082/mjpg/video.mjpg'

video_capture_0 = cv.VideoCapture(camera0)
video_capture_1 = cv.VideoCapture(camera1)
video_capture_2 = cv.VideoCapture(camera2)
video_capture_3 = cv.VideoCapture(camera3)

video_capture_0.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
video_capture_1.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
video_capture_2.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
video_capture_3.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))

video_capture_0.set(cv.CAP_PROP_BUFFERSIZE, 20)
video_capture_1.set(cv.CAP_PROP_BUFFERSIZE, 20)
video_capture_2.set(cv.CAP_PROP_BUFFERSIZE, 20)
video_capture_3.set(cv.CAP_PROP_BUFFERSIZE, 20)

def rescale_frame(frame, percent=50):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)

def hconcat_resize_min(im_list, interpolation=cv.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv.hconcat(im_list_resize)

def vconcat_resize_min(im_list, interpolation=cv.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv.vconcat(im_list_resize)

def concat_tile_resize(im_list_2d, interpolation=cv.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv.INTER_CUBIC)

while True:
        ret0, frame0 = video_capture_0.read()
        ret1, frame1 = video_capture_1.read()
        ret2, frame2 = video_capture_2.read()
        ret3, frame3 = video_capture_3.read()

        frame0 = rescale_frame(frame0)
        frame1 = rescale_frame(frame1)
        frame2 = rescale_frame(frame2)
        fame3 = rescale_frame(frame3)
        frame = concat_tile_resize([[frame0, frame1],[frame2, frame3]])
        cv.imshow('cams', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

video_capture_0.release()
video_capture_1.release()
video_capture_2.release()
video_capture_3.release()
cv.destroyAllWindows()

