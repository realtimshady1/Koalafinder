import cv2
import os
import sys

def extract_frames(video_file, folder):
    cap = cv2.VideoCapture(video_file)

    frame_list = [int(os.path.splitext(frame)[0]) for frame in os.listdir(folder)]
    count = 0
    while True:
        if count in frame_list:
            #cap.set(2,int(frame))
            is_read, img = cap.read()
            if not is_read:
                break
            cv2.imwrite(os.path.join(folder,str(count).zfill(8))+'.jpg', img)
            count += 1
        else:
            count += 1

if __name__=='__main__':
    if len(sys.argv) > 2:
        video_file = sys.argv[1]
        folder = sys.argv[2]
    else:
        raise ValueError('Please specify the correct number of inputs')

    extract_frames(video_file, folder)
