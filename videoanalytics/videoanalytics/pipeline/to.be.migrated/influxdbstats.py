# !pip3 install influxdb
from .videoprocessinglayers import VideoProcessingLayer
from influxdb import InfluxDBClient
from datetime import datetime, timedelta

def get_current_timestamp_as_str():
    return datetime.utcnow().strftime("%Y%m%d%H%M")


class InfluxDBStatisticsLayer(VideoProcessingLayer):
    def __init__(self, host='localhost', port=8086, database="my_application"):
        VideoProcessingLayer.__init__(self)
        self.client = InfluxDBClient(host=host, port=port, database=database)
        pass
    
    def setup(self, ctx):
        json_body = []

        now_str = get_current_timestamp_as_str()
        
        interesting_variables = [
                    "INPUT_FILENAME",
                    "INPUT_MAX_FRAMES",
                    "INPUT_LENGTH"
        ]
        
        for v in interesting_variables:
            json_body.append(
                {
                    "measurement": v,
                    "time": now_str,
                    "fields": {
                        "value": ctx[v]
                    }
                }
            )        

        """
        json_body.append(
            {
                "measurement": "TestMeasuremntFromOutsideDockerToTestTimestamp",
                "time": datetime.utcnow(),
                "fields": {
                    "value": str(datetime.now())
                }
            }
        )        
        """
        self.client.write_points(json_body)
    
    def process(self, ctx):
        json_body = []

        now_str = get_current_timestamp_as_str()
        
        json_body.append(
            {
                "measurement": "INPUT_CURR_FRAME",
                "time":  now_str,
                "fields": {
                    "value": ctx["INPUT_CURR_FRAME"]
                }
            }
        )        
        
        for k,v in ctx["OBJECT_DETECTION_LABELED_OUTPUT_SCORES"].items():
            json_body.append(
                {
                    "measurement": k.upper()+"_COUNT",
                    "time":  now_str,
                    "fields": {
                        "value": len(v)
                    }
                }
        )        
        
        self.client.write_points(json_body)
    
    def release(self, ctx):
        self.client.close()