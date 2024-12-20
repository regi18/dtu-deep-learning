from typing import Literal
import torch
from models.yolo.utils.intersection_over_union import intersection_over_union


def non_max_suppression(bboxes: list, iou_threshold: float, threshold: float, box_format: Literal['midpoint', 'corners'] = 'corners'):
    """
    Does Non-Max Suppression (NMS) to given bboxes.
    NMS is a method to filter overlapping bounding boxes that represent the same object. 
    It keeps the box with the highest confidence score for an object and removes overlapping boxes (using IoU).

    Parameters:
        bboxes (list): list of lists containing all bboxes with each bboxes specified as [class_pred, prob_score, x1, y1, x2, y2]
        iou_threshold (float): threshold where predicted bboxes is correct
        threshold (float): threshold to remove predicted bboxes (independent of IoU) 
        box_format (str): "midpoint" or "corners" used to specify bboxes

    Returns:
        list: bboxes after performing NMS given a specific IoU threshold
    """

    assert type(bboxes) == list

    # Filter bboxes based based on prob_score/confidence score, 
    # then sort them by confidence score (bboxes[0] will have the heighest prob_score)
    bboxes = [box for box in bboxes if box[1] > threshold]
    bboxes = sorted(bboxes, key=lambda x: x[1], reverse=True)
    bboxes_after_nms = []

    while bboxes:
        chosen_box = bboxes.pop(0)

        # Put "chosen_box" back into bboxes if the IoU between that and another bbox is less than iou_threshold: i.e. keep low overlap bboxes.
        # Boxes with high overlap (IoU >= iou_threshold) are suppressed (removed).
        bboxes = [
            box
            for box in bboxes
            if box[0] != chosen_box[0]
            or intersection_over_union(
                torch.tensor(chosen_box[2:]),
                torch.tensor(box[2:]),
                box_format=box_format,
            )
            < iou_threshold
        ]

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms
