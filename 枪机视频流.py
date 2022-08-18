import av
import cv2

# video = av.open('rtsp://admin:admin@192.168.0.98/stream1', 'r')
# #video = av.open('http://10.11.20.104:8554/48/64', 'r')
# print("format:" + video.dumps_format())
# print('after open')
# index = 0
# try:
#     for frame in video.decode():
#         # Do something with `frame`
#         index += 1
#         print("frame:{}".format(index))
#
#         img = frame.to_nd_array(format='bgr24')
#         #cv2.imshow("Test", img)
#         cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
#         cv2.imshow("frame", img)
#         cv2.imwrite("Test{}.jpg".format(index), img)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# except Exception as e:
#     print('fate erro:{}'.format(e))
#
# cv2.destroyAllWindows()


import ffmpeg
host = '192.168.0.98/stream1'

# 子进程
(
    ffmpeg.input('rtsp://' + 'admin:admin@' + host, allowed_media_types='video',  rtsp_transport='tcp')['a']  # allowed_media_types='audio' 只读取音频流
        .filter('volume', 1)  # 音量大小控制
        .overwrite_output()
        .run(capture_stdout=True)
)