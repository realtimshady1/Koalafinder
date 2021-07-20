import numpy as np

EPSILON = 1e-15
INF = 9e15


def get_iou(box1, box2):
    # get the coordinates of bounding boxes
    b1_x1, b1_y1, b1_x2, b1_y2 = box1[:, 0], box1[:, 1], box1[:, 2], box1[:, 3]
    b2_x1, b2_y1, b2_x2, b2_y2 = box2[:, 0], box2[:, 1], box2[:, 2], box2[:, 3]

    # get the corrdinates of the intersection rectangle
    inter_rect_x1 = np.max(b1_x1, b2_x1)
    inter_rect_y1 = np.max(b1_y1, b2_y1)
    inter_rect_x2 = np.min(b1_x2, b2_x2)
    inter_rect_y2 = np.min(b1_y2, b2_y2)

    # intersection area
    inter_area = np.clip(inter_rect_x2 - inter_rect_x1 + 1) * \
        np.clip(inter_rect_y2 - inter_rect_y1 + 1, min=0)

    # union Area
    b1_area = (b1_x2 - b1_x1 + 1) * (b1_y2 - b1_y1 + 1)
    b2_area = (b2_x2 - b2_x1 + 1) * (b2_y2 - b2_y1 + 1)

    iou = inter_area / (b1_area + b2_area - inter_area)

    return iou


def pair_distance(bbox_A, bbox_B):
    # intersection over union score
    iou = get_iou(bbox_A['bbox'][:], bbox_B['bbox'][:])

    # confidence score
    score = np.dot(bbox_A['scores'], bbox_B['scores'])

    # distance is the inverse of similarity
    # epsilon value prevents a divide by 0
    distance = 1 / (iou * score + EPSILON)

    return distance


def pair_positives(distances, maximization_problem):
    # initialize pair list
    pairs = []

    # continue while there are still unmatched axes
    while distances.min() != INF:
        # find the smallest distance
        inds = np.where(distances == distances.min())

        # check if either axis is 1
        a, b = inds if len(inds[0]) == 1 else (inds[0][0], inds[1][0])

        # record the results
        a, b = int(a), int(b)
        pairs.append((a, b))

        # remove all other records in the same row and column
        distances[a, :] = INF
        distances[:, b] = INF

    return pairs


def rescore_bbox(cur_score, prev_score, count):
    # calculate new historical vector score
    cur_score = cur_score / (count + 1) + prev_score * count / (count + 1)

    # increase consecutive frame count by one
    count += 1

    return cur_score, count


def post_process(detections, prev_detections):
    # extract information
    scores, bboxs = detections
    prev_scores, prev_bboxs = prev_detections

    # initialise the distance matrix
    distances = np.zeros((np.len(bboxs), np.len(prev_bboxs)))

    # cycle each combination of bboxs
    for bbox, i in enumerate(bboxs, 0):
        for prev_bbox, j in enumerate(prev_bboxs, 0):
            # record the distance between each pair
            distances[i, j] = pair_distance(bbox,
                                            prev_bbox)

    # find positive bbox pairs from the matrix
    pairs = pair_positives(distances)

    # make new list of bboxs
    new_bboxs = [bboxs[i] for i in pairs[:, 0]]

    # calculate new scores
    new_scores = [rescore_bbox(scores[idx], prev_scores[prev_idx]) for idx, prev_idx in pairs]

    return zip(new_scores, new_bboxs)
