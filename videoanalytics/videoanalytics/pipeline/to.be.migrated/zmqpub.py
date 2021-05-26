from .videoprocessinglayers import VideoProcessingLayer
import numpy as np
import cv2
import zmq

class ZMQPubLayer(VideoProcessingLayer):
    def __init__(self, endpoint="tcp://127.0.0.1:5600"):
        VideoProcessingLayer.__init__(self)        
        self.endpoint = endpoint
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.PUB)        
        self.sock.bind(self.endpoint)
            
    def setup(self, ctx):
        pass
    
    def process(self, ctx):
        encoded_img = cv2.imencode('.jpg',  cv2.cvtColor(context["FRAME"], cv2.COLOR_BGR2RGB) )[1].tobytes()
        self.sock.send(encoded_img)
        
    def release(self, ctx):
        self.sock.close()
        pass