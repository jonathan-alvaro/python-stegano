import cv2 as cv

source = cv.VideoCapture('videos/video.avi')
fourcc = cv.VideoWriter_fourcc(*'XVID')

out = cv.VideoWriter('v.avi', fourcc, 20.0, (int(source.get(3)), int(source.get(4))))

for i in range(1000):
    _, frame = source.read()
    out.write(frame)

source.release()
out.release()