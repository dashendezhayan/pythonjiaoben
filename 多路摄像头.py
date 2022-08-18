# -*- coding: utf-8 -*-
""" 
@Time    : 2021/10/25 18:04
@Author  : xuhaotian
@FileName: 多路摄像头.py
@SoftWare: PyCharm
"""
import cv2
import time
import multiprocessing as mp
def image_put(q, user, pwd, ip, channel=1):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s//Streaming/Channels/%d" % (user, pwd, ip, channel))
    if cap.isOpened():
        print('HIKVISION')
    else:
        cap = cv2.VideoCapture("rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (user, pwd, ip, channel))
        print('DaHua')

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)


def image_get(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

def run_single_camera():
    user_name, user_pwd, camera_ip = "admin", "a12345678", "192.168.3.111"

    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)),
                 mp.Process(target=image_get, args=(queue, camera_ip))]

    [process.start() for process in processes]
    [process.join() for process in processes]

def run_multi_camera():
    # user_name, user_pwd = "admin", "password"
    user_name, user_pwd = "admin", "a12345678"
    camera_ip_l = [
        "192.168.3.111",  # ipv4
        "192.168.3.111",
        "192.168.3.111",  # ipv4
        "192.168.3.111",  # ipv4
        "192.168.3.111",  # ipv4
        "192.168.3.111",  # ipv4# ipv6
        "192.168.3.111",  # ipv4# ipv6

    ]

    mp.set_start_method(method='spawn')  # init
    queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]

    processes = []
    for queue, camera_ip in zip(queues, camera_ip_l):
        processes.append(mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)))
        processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))

    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    # run_single_camera()
    run_multi_camera()
    pass
