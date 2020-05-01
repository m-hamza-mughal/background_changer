import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg as get_detectron_cfg


class Segmenter:
    def __init__(self, cfg):
        self.det_cfg = get_detectron_cfg()

        self.det_cfg.merge_from_file(model_zoo.get_config_file(cfg.DETECTRON.CONFIG_FILE))
        self.det_cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = cfg.DETECTRON.SCORE_THRESH
        self.det_cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = cfg.DETECTRON.NMS_THRESH
        self.det_cfg.MODEL.DEVICE = cfg.DETECTRON.DEVICE
        self.det_cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(cfg.DETECTRON.CONFIG_FILE)
        self.predictor = DefaultPredictor(self.det_cfg)

    def predict(self, image):
        """
        Returns mask of first person in image
        :param image:
        :return:
        """
        outputs = self.predictor(image)
        mask = outputs.get('instances').get('pred_masks')
        person_indices = outputs.get('instances').get('pred_classes') == 0

        person_mask = mask[person_indices]
        person_mask = person_mask.sum(axis=0)
        return person_mask.cpu().numpy()
