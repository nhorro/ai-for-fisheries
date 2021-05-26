from .videoprocessinglayers import VideoProcessingLayer
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

class ElasticSearchObjectDetectionIndexer(VideoProcessingLayer):
    def __init__(self):
        VideoProcessingLayer.__init__(self)
        self.es = Elasticsearch()
    
    def setup(self, ctx):
        pass
    
    def process(self, ctx):
        doc = {
            'frame': ctx["INPUT_CURR_FRAME"],
            'detectedobjs': ctx["OBJECT_DETECTION_LABELED_OUTPUT_ES"],
            'timestamp': datetime.utcnow()
        }
                
        res = self.es.index(index="detected-objects2", doc_type='object-detections2', body=doc)

    def release(self, ctx):
        pass