from time import time
import glob
import random
import cv2
from tqdm import tqdm

from .detectron_helper import Segmenter
from .video_helper import VideoReader


def process_video(cfg, file, bck_path, bck_idx, predictor):
    start = time()
    frame_iterator = VideoReader(cfg, file, bck_idx)
    background_im = cv2.imread(bck_path)

    for ret, frame in frame_iterator:
        if not ret and frame is None:
            break

        background = background_im.copy()
        mask = predictor.predict(frame)
        clone = frame.copy()

        # Inflate the mask
        # kernel = np.ones((3,3), np.uint8)
        # dilated_mask = cv2.dilate(mask.astype(np.uint8), kernel, iterations = 1)

        clone[mask == 0] = 0
        background = cv2.resize(background, (clone.shape[1], clone.shape[0]))

        background[mask != 0] = 0
        combined_image = background + clone

        frame_iterator.write_frame(combined_image)

    frame_iterator.clean()
    if cfg.VERBOSITY == 1:
        print("Completed:", frame_iterator.video_out_name.split('/')[-1], "Time:", time()-start)


def process_image(cfg, file, bck_path, bck_idx, predictor):
    start = time()
    image = cv2.imread(file)
    out_image = cfg.OUTPUT.DIR + file.split('/')[-1][:-4] + "_BCK{}.".format(bck_idx) + cfg.OUTPUT.FORMAT
    background = cv2.imread(bck_path)

    mask = predictor.predict(image)
    clone = image.copy()

    # Inflate the mask
    # kernel = np.ones((3,3), np.uint8)
    # dilated_mask = cv2.dilate(mask.astype(np.uint8), kernel, iterations = 1)

    clone[mask == 0] = 0
    background = cv2.resize(background, (clone.shape[1], clone.shape[0]))

    background[mask != 0] = 0
    combined_image = background + clone

    cv2.imwrite(out_image, combined_image)
    if cfg.VERBOSITY == 1:
        print("Completed:", out_image.split('/')[-1], "Time:", time()-start)


def process_data(cfg):
    assert len(glob.glob(cfg.BACKGROUND.DIR + "*.jpg")) > 0,\
        "No background images available.\nMake sure images are in .jpg format"

    num_backgrounds = cfg.BACKGROUND.NUM_VARIATIONS
    if num_backgrounds > 0:
        list_of_backgrounds = random.sample(glob.glob(cfg.BACKGROUND.DIR + "*.jpg"), num_backgrounds)
    else:
        list_of_backgrounds = glob.glob(cfg.BACKGROUND.DIR + "*.jpg")

    list_of_files = glob.glob(cfg.INPUT.DIR + "*." + cfg.INPUT.FORMAT)
    assert len(list_of_files) > 0, "No input files found"

    segmentation_predictor = Segmenter(cfg)

    for file_path in tqdm(list_of_files):
        for bck_idx, bck_path in enumerate(list_of_backgrounds):
            if cfg.DATA.FORMAT == "video":
                process_video(cfg, file_path, bck_path, bck_idx, segmentation_predictor)
            else:
                process_image(cfg, file_path, bck_path, bck_idx, segmentation_predictor)

    print("Data Converted. \nFiles available at: ", cfg.OUTPUT.DIR)
