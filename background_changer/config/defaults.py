#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

"""Configs."""
from fvcore.common.config import CfgNode

# -----------------------------------------------------------------------------
# Config definition
# -----------------------------------------------------------------------------
_C = CfgNode()

# ---------------------------------------------------------------------------- #
# Background options
# ---------------------------------------------------------------------------- #
_C.BACKGROUND = CfgNode()

_C.BACKGROUND.NUM_VARIATIONS = -1

_C.BACKGROUND.DIR = "./data/backgrounds/"


# -----------------------------------------------------------------------------
# Data options
# -----------------------------------------------------------------------------
_C.DATA = CfgNode()

# either can be video or image
_C.DATA.FORMAT = "video"


# -----------------------------------------------------------------------------
# Detectron options
# -----------------------------------------------------------------------------

_C.DETECTRON = CfgNode()

# cpu or cuda
_C.DETECTRON.DEVICE = "cuda"

_C.DETECTRON.SCORE_THRESH = 0.5

_C.DETECTRON.NMS_THRESH = 0.5

_C.DETECTRON.CONFIG_FILE = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"


# -----------------------------------------------------------------------------
# Output options
# -----------------------------------------------------------------------------

_C.OUTPUT = CfgNode()

_C.OUTPUT.DIR = "./data/output/video/" if _C.DATA.FORMAT == "video" else "./data/output/images/"

_C.OUTPUT.FORMAT = "avi" if _C.DATA.FORMAT == "video" else "jpg"


# -----------------------------------------------------------------------------
# Input options
# -----------------------------------------------------------------------------

_C.INPUT = CfgNode()

_C.INPUT.DIR = "./data/test_data/"

_C.INPUT.FORMAT = "avi" if _C.DATA.FORMAT == "video" else "jpg"


def _assert_and_infer_cfg(cfg):
    # Background assertions.
    assert cfg.BACKGROUND.NUM_VARIATIONS != 0
    # TRAIN assertions.
    assert cfg.DATA.FORMAT in ["video", "image"]
    assert cfg.DETECTRON.DEVICE in ["cpu", "cuda"]

    assert cfg.DETECTRON.SCORE_THRESH > 0
    return cfg


def get_cfg():
    """
    Get a copy of the default config.
    """
    return _assert_and_infer_cfg(_C.clone())
