import cv2
import argparse
import darknet as dn
import os
import csv
from threading import Thread
from queue import Queue

from utils import read_srt
from post_process import post_process


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="Yolov4 .cfg file path",
                        type=str)
    parser.add_argument('data', help="Yolov4 .data file path",
                        type=str)
    parser.add_argument('weights', help="Yolov4 .weights file path",
                        type=str)
    parser.add_argument('input', help="Input test video path",
                        type=str)
    parser.add_argument('-post_process', help='Apply post processing or not',
                        type=bool, default=True)
    parser.add_argument('-output', help="Output file name",
                        type=str, default="output.avi")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    parser.add_argument("--show", type=bool, default=False,
                        help="window inference display. For headless systems")
    return parser.parse_args()


def check_args(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config):
        raise(ValueError("Invalid config path {}".format(
            os.path.abspath(args.config))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(
            os.path.abspath(args.weights))))
    if not os.path.exists(args.data):
        raise(ValueError("Invalid data file path {}".format(
            os.path.abspath(args.data))))
    if not os.path.exists(args.input):
        raise(ValueError("Invalid video path {}".format(
            os.path.abspath(args.input))))


def str2int(video_path):
    try:
        return int(video_path)
    except ValueError:
        return video_path


def convert_points(bbox):
    left, top, right, bottom = dn.bbox2points(bbox)
    left = int(left * width_ratio)
    top = int(top * height_ratio)
    right = int(right * width_ratio)
    bottom = int(bottom * height_ratio)

    return (left, top), (right, bottom)


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        # read frame from the video source
        ret, frame = cap.read()
        if not ret:
            break

        # convert frame to useable format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame,
                                   (width, height),
                                   interpolation=cv2.INTER_LINEAR)

        # add frame to output queue
        frame_queue.put(frame)

        # convert for detection
        img_for_detect = dn.make_image(width, height, 3)
        dn.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())

        # add frame to detect queue
        darknet_image_queue.put(img_for_detect)

    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        # read from queue
        try:
            darknet_image = darknet_image_queue.get(timeout=1)
        except:
            break

        # perform detection
        detections = dn.detect_image(network,
                                     class_names,
                                     darknet_image,
                                     thresh=args.thresh)

        # save detections to output queue
        try:
            detections_queue.put(detections, timeout=1)
        except:
            break
        
        # clean up
        dn.free_image(darknet_image)

    cap.release()


def drawing(frame_queue, detections_queue):
    # set out for video writer
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(args.output,
                            cv2.VideoWriter_fourcc(*"MJPG"),
                            fps,
                            (frame_width, frame_height))

    # initialize the loop for the first frame
    prev_detections = []
    
    # initialize timestamps
    tstamp = 0
    
    # initialize csv log
    f = open(os.path.splitext(os.path.basename(input_path))[0] + '.csv', 'w')
    contents = read_srt(os.path.splitext(input_path)[0] + '.SRT')
    writer = csv.writer(f)
    header = ['Video Time', 'Label', 'Confidence', 'Bounding-box'] + contents[0].keys()
    writer.writerow(header)
    
    # start inference loop
    print("Inference started...")
    while cap.isOpened():
        # read from queue
        frame = frame_queue.get()
        detections = detections_queue.get()
        tstamp += 1


        if frame is not None:
            # post process the detections to find new detections
            if args.post_process and len(detections) and len(prev_detections):
                detections = post_process(detections, prev_detections)
    
            # record the results to use for the next frame
            prev_detections = detections
            
            # print positive detections
            if len(detections):
                print('{}s '.format(int(tstamp/30)))
                for label, confidence, bbox in detections:
                    print("\t{}: {}%".format('Koala', confidence))
                    writer.writerow([tstamp/fps, 'Koala', confidence, bbox] + contents[tstamp].values())
            
            for _, confidence, bbox in detections:
                xy1, xy2 = convert_points(bbox)

                # apply bounding boxes to the image
                cv2.rectangle(frame, xy1, xy2, (255, 255, 255), 2)

                # apply text box to the image
                text = "{} [{:.2f}]".format("Koala", float(confidence))
                cv2.putText(frame, text, (xy1[0], xy1[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255),
                            2)
                

            # show output window
            if args.show:
                cv2.imshow('Inference', frame)

            # write to output
            if args.output is not None:
                video.write(frame)

    f.close()
    cap.release()
    video.release()
    cv2.destroyAllWindows()
       
    print("Video Write Completed")


if __name__ == "__main__":
    # create queue for processing
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    # load input arguments
    args = parser()
    check_args(args)

    # load in our YOLOv4 architecture network
    network, class_names, class_colors = dn.load_network(args.config,
                                                         args.data,
                                                         args.weights)

    # load the width and height of the network
    width = dn.network_width(network)
    height = dn.network_height(network)

    # Local Stored video detection - Set input video
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)

    # calculate ratio to convert from frame to yolo input window
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width_ratio = frame_width / width
    height_ratio = frame_height / height

    # start multithreading processes
    Thread(target=video_capture, args=(frame_queue,
                                       darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue,
                                   detections_queue,
                                   fps_queue)).start()
    Thread(target=drawing, args=(frame_queue,
                                 detections_queue)).start()
