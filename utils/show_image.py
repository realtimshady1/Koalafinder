import cv2
import argparse

def draw_bbox(frame, classId, left, top, right, bottom):
    # Draw a bounding box.
    frame_gt = frame
    cv2.rectangle(frame_gt, (left, top), (right, bottom), (255, 178, 50), 3)
    label = '%s' % (classId)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    frame_gt = cv2.rectangle(frame_gt,
                             (left,
                              int(top - round(1.5 * labelSize[1]))),
                             (left + int(round(1.5 * labelSize[0])),
                              top + baseLine),
                             (255, 255, 255),
                             cv2.FILLED)
    frame_gt = cv2.putText(frame_gt, label, (left, top),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    return frame_gt


def show_image(name):
    gt_base = "./"
    textfilename = name + ".txt"
    img_path = name + ".jpg"
    frame_orig = cv2.imread(img_path)
    gt_path = gt_base + textfilename
    img_height, img_width = frame_orig.shape[:2]
    with open(gt_path, "r") as f_gt:
        content_gt = f_gt.readlines()
    content_gt = [x.strip() for x in content_gt]
    for line in content_gt:
        obj_id, left, top, width, height = map(int, line.split())
        print(line)
        image_gt = draw_bbox(
            frame_orig,
            obj_id,
            left,
            top,
            left + width,
            top + height)
    cv2.imshow('Groundtruth', image_gt)
    cv2.waitKey(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="name of the image to display",
                        type=str)
    args = parser.parse_args()

    show_image(args.name)
