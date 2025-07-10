class Model:
    def __init__(self):
        pass

    def train_model(self):
        pass

    def load_weights(self):
        pass

    def infer(self, img=""):
        pass

    def test_model(self, img_dir, ann_dir, output_dir, debug_flag=False, data_stats=False):
        """
        Description: This will generate a csv file with below-mentioned columns:
        Channel Name, total_annotated_boxes, total_predicted_boxes, correct_preds, iou < 80, extra_preds
        if debug_flag is true write images to the output dir and save with discussed convention name.

        Args:
            img_dir:
            ann_dir:
            output_dir:

        Returns: mAP
        """

        pass

