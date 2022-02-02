import cv2
import os
import sys
from tqdm import tqdm
from time import time
from threading import Thread
from queue import Queue

def read_frames(frame_list, video_file, frames_queue):
    cap = cv2.VideoCapture(video_file)
    count = 0
    for frame in frame_list:
        if frame != count:
            cap.set(1, frame)
            count = frame
        img = cap.read()[1]
        count += 1
        frames_queue.put(img)

def write_frames(frame_list, folder, frames_queue):
    for frame in tqdm(frame_list):
        img = frames_queue.get(timeout=1)
        cv2.imwrite(os.path.join(folder,str(frame).zfill(8))+'.jpg', img)


def extract_frames(video_file, folder):
    start_time = time()
    frames_queue = Queue(maxsize=1)

    frame_list = sorted([int(os.path.splitext(frame)[0]) for frame in os.listdir(folder)])[:100]

    Thread(target=read_frames, args=(frame_list, video_file, frames_queue)).start()
    Thread(target=write_frames, args=(frame_list, folder, frames_queue)).start()

    #print('Elapsed time: ', time()-start_time)

if __name__=='__main__':
    if len(sys.argv) > 2:
        video_file = sys.argv[1]
        folder = sys.argv[2]
    else:
        raise ValueError('Please specify the correct number of inputs')

    extract_frames(video_file, folder)
