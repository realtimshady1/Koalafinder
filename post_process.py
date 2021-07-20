import numpy as np

EPSILON = 1e-15
INF = 9e15


def get_iou(box1, box2):
    # get the corrdinates of the intersection rectangle
    rect_x1 = np.maximum(box1[0], box2[0])
    rect_y1 = np.maximum(box1[1], box2[1])
    rect_x2 = np.minimum(box1[2], box2[2])
    rect_y2 = np.minimum(box1[3], box2[3])

    # intersection area
    inter_area = np.maximum((rect_x2 - rect_x1 + 1), 0) * \
        np.maximum((rect_y2 - rect_y1 + 1), 0)

    # union Area
    b1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    b2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # calculate iou
    iou = inter_area / (b1_area + b2_area - inter_area)

    return iou


def pair_distance(bboxA, scoreA, bboxB, scoreB):
    # intersection over union score
    iou = get_iou(bboxA, bboxB)

    # confidence score
    score = np.dot(scoreA, scoreB)

    # distance is the inverse of similarity
    # epsilon value prevents a divide by 0
    distance = 1 / (iou * score + EPSILON)

    return distance


def pair_positives(distances):
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


def rescore_bbox(score, prev_score, count):
    # calculate new historical vector score
    score = float(score) / (count + 1) + \
        float(prev_score) * count / (count + 1)

    # increase consecutive frame count by one
    count += 1

    return score, count


def redetect(dets, prev_dets, idx, prev_idx):
    # check if the first item is a string
    if isinstance(prev_dets[idx][0], str):
        count = 0
    else:
        count = prev_dets[idx][0]

    # copy the previous bbox
    new_bbox = dets[idx][2]
    new_score, new_count = rescore_bbox(dets[idx][1],
                                        prev_dets[prev_idx][1],
                                        count)

    return (new_count, new_score, new_bbox)


def post_process(dets, prev_dets):
    # initialise the distance matrix
    distances = np.zeros((len(dets), len(prev_dets)))

    # cycle each combination of bboxs
    for i, (_, score, bbox) in enumerate(dets, 0):
        for j, (_, prev_score, prev_bbox) in enumerate(prev_dets, 0):
            # record the distance between each pair
            distances[i, j] = pair_distance(bbox,
                                            float(score),
                                            prev_bbox,
                                            float(prev_score))

    # find positive bbox pairs from the matrix
    pairs = pair_positives(distances)

    # create new dets
    new_dets = [redetect(dets, prev_dets, idx, prev_idx)
                for idx, prev_idx in pairs]

    return new_dets
