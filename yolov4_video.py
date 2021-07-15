import cv2
import argparse
import darknet as dn
from time import time


def yolov4_video(args):
    # Video output Frame per second
    FPS = 30.0 
    
    # load in our YOLOv4 architecture network
    network, class_names, class_colors = dn.load_network(args.config,
                                                         args.data,
                                                         args.weights)

    # load the width and height of the network
    width = dn.network_width(network)
    height = dn.network_height(network)

    # Uncomment to use Webcam
    # cap = cv2.VideoCapture(0)

    # Local Stored video detection - Set input video
    cap = cv2.VideoCapture(args.input)

    # returns the width and height of capture video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # set out for video writer
    out = cv2.VideoWriter(
        args.output, cv2.VideoWriter_fourcc(*"MJPG"), FPS,
        (frame_width, frame_height))

    # Calculate ratio to convert from frame to yolo input window
    width_ratio = frame_width / width
    height_ratio = frame_height / height

    # create an image we reuse for each detect
    image = dn.make_image(width, height, 3)

    # start the timer
    start = time()
    print("Starting the YOLO loop...")

    # load the input frame and write output frame.
    while True:
        prev_time = time()

        # capture frame and return true if frame present
        ret, frame = cap.read()

        # check if frame present otherwise break the while loop
        if not ret:
            break

        # convert frame into RGB from BGR and resize accordingly
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(frame, (width, height),
                             interpolation=cv2.INTER_LINEAR).tobytes()

        # copy that frame bytes to darknet_image
        dn.copy_image_from_bytes(image, resized)

        # detection occurs at this line and return detections
        detections = dn.detect_image(network, class_names, image)

        # cycle through the positive detections
        for label, confidence, bbox in detections:
            left, top, right, bottom = dn.bbox2points(bbox)
            left = int(left * width_ratio)
            top = int(top * height_ratio)
            right = int(right * width_ratio)
            bottom = int(bottom * height_ratio)

            # apply bounding boxes to the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (255,255,255), 2)

            # apply text box to the image
            cv2.putText(frame, "{} [{:.2f}]".format(label, float(confidence)),
                        (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255,255,255), 2)

        # Write that frame into output video
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        # print fps
        print(1 / (time() - prev_time))

        # # display Image window
        # cv2.imshow('Demo', image)
        # cv2.waitKey(3)

    # release cap and out.
    cap.release()
    out.release()
    print(f"Time elapsed: {time()-start}")
    print("Video Write Completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="Yolov4 .cfg file path",
                        type=str)
    parser.add_argument('data', help="Yolov4 .data file path",
                        type=str)
    parser.add_argument('weights', help="Yolov4 .weights file path",
                        type=str)
    parser.add_argument('input', help="Input test video path",
                        type=str)
    parser.add_argument('-output', help="Output file name",
                        type=str, default="output.avi")
    args = parser.parse_args()

    yolov4_video(args)
