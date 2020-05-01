import cv2


class VideoReader(object):

    def __init__(self, cfg, file, bck_idx):
        self.source = file
        self.video_out_name = cfg.OUTPUT.DIR + file.split('/')[-1][:-4] + "_BCK{}.".format(bck_idx) + cfg.OUTPUT.FORMAT

    def __iter__(self):
        self.cap = cv2.VideoCapture(self.source)

        self.output_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.output_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        self.video_out = cv2.VideoWriter(
            self.video_out_name,
            fourcc,
            15,
            (self.output_width, self.output_height))

        if not self.cap.isOpened():
            raise IOError('Video {} cannot be opened'.format(self.source))
        return self

    def __next__(self):
        was_read, frame = self.cap.read()
        if not was_read:
            frame = None

        return was_read, frame

    def write_frame(self, frame):
        self.video_out.write(frame)

    def clean(self):
        self.cap.release()
        self.video_out.release()
        cv2.destroyAllWindows()



