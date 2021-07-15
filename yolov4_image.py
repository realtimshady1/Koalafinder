import darknet as dn
import cv2
import argparse


def darknet_helper(img, width, height, network, class_names):
    darknet_image = dn.make_image(width, height, 3)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb,
                             (width, height),
                             interpolation=cv2.INTER_LINEAR)

    # get image ratios to convert bounding boxes to proper size
    img_height, img_width, _ = img.shape
    width_ratio = img_width / width
    height_ratio = img_height / height

    # run model on darknet style image to get detections
    dn.copy_image_from_bytes(darknet_image, img_resized.tobytes())
    detections = dn.detect_image(network, class_names, darknet_image)
    dn.free_image(darknet_image)

    return detections, width_ratio, height_ratio


def yolov4_inference(args):
    # load in our YOLOv4 architecture network
    network, class_names, class_colors = dn.load_network(args.config,
                                                         args.data,
                                                         args.weights)

    # load the width and height of the network
    width = dn.network_width(network)
    height = dn.network_height(network)

    # run test on person.jpg image that comes with repository
    image = cv2.imread(args.input)
    detections, width_ratio, height_ratio = darknet_helper(image,
                                                           width,
                                                           height,
                                                           network,
                                                           class_names)

    # cycle through the positive detections
    for label, confidence, bbox in detections:
        left, top, right, bottom = dn.bbox2points(bbox)
        left = int(left * width_ratio)
        top = int(top * height_ratio)
        right = int(right * width_ratio)
        bottom = int(bottom * height_ratio)

        # apply bounding boxes to the image
        cv2.rectangle(image, (left, top), (right, bottom),
                      class_colors[label], 2)

        # apply text box to the image
        cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                    (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    class_colors[label], 2)

    # save the final image
    print(f'Image saved to {args.output}')
    cv2.imwrite(args.output, image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="Yolov4 .cfg file path",
                        type=str)
    parser.add_argument('data', help="Yolov4 .data file path",
                        type=str)
    parser.add_argument('weights', help="Yolov4 .weights file path",
                        type=str)
    parser.add_argument('input', help="Input test image path",
                        type=str)
    parser.add_argument('-output', help="Output file name",
                        type=str, default="predictions.jpg")
    args = parser.parse_args()

    # enter main function
    yolov4_inference(args)
