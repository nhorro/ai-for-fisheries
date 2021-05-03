import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
import cv2
import os


import networkx as nx
from videoanalytics.pipeline import Source, Sink
from videoanalytics.pipeline.sources import VideoReader
from videoanalytics.pipeline.sinks import VideoWriter
from videoanalytics.pipeline.sinks.yolo4_detector import YOLOv4Detector
from videoanalytics.pipeline.sinks.obj_detector import DetectionsAnnotator, DetectionsCSVWriter, ObjectDetectorCSV


import json



def load_rois(filename):





class ROIView(Sink):        
    def __init__(self, context,filename):
        super().__init__(context)

		with open(filename) as f:
  			self.rois = json.load(f)

  		self.rois = self.rois["regions"]

  		for r in self.rois:
  			r["polygon"] = np.int32(r["polygon"])
   
    def setup(self):        
        self.frame_counter = self.context["START_FRAME"]
            
    def process(self):       
		overlay = context["FRAME"].copy()

        # BEGIN GUI CODE
        if len(g_roi) > 2:
            converted_roi = np.int32([g_roi])            
            

        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle over the image
        context["FRAME"] = cv2.addWeighted(overlay, alpha, context["FRAME"], 1 - alpha, 0)
		for r in self.rois:
  			cv2.fillPoly(overlay, pts = r["polygon"] , color =r["color"])
            cv2.polylines(overlay, r["polygon"] , 5, r["color"])
        self.frame_counter+=1
    
    def shutdown(self):
        pass     	
