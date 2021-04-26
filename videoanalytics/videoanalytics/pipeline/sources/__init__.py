import cv2
import numpy as np
from tqdm.notebook import tqdm

from videoanalytics.pipeline import Source

class VideoReader(Source):
    def __init__(self, context,video_path,start_frame=0,max_frames=None):        
        super().__init__(context)
        self.processed_frames = 0
        self.cap = cv2.VideoCapture(video_path)
        
        video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.start_frame = start_frame
        self.max_frames = max_frames
        if self.max_frames is None:
            self.total_frames = video_frame_count-self.start_frame 
        else:
            self.total_frames = self.max_frames

        if self.total_frames>(video_frame_count-self.start_frame):
            self.total_frames=video_frame_count-self.start_frame
            
        self.context["INPUT_FPS"] = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.context["INPUT_WIDTH"] = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.context["INPUT_HEIGHT"] = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.context["START_FRAME"] =  self.start_frame
        self.context["TOTAL_FRAMES"] = self.total_frames
        print("Start frame:", self.start_frame)
        print("Total frames frame:", self.total_frames)
        self.progress_bar = tqdm(total=self.total_frames)
   
    def setup(self):
        #print("Setting up VideoReader")
        pass
    
    def read(self):
        if self.processed_frames < self.total_frames:
            #print("Reading frame %d/%d" % (self.processed_frames+1,self.max_frames) )
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.context['FRAME'] = frame
            self.processed_frames+=1
            self.progress_bar.update(1)
        else:
            ret = False
        return ret
    
    def shutdown(self):
        #print("Shutting down VideoReader")
        self.cap.release()