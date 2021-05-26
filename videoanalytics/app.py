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
from videoanalytics.pipeline.sinks.obj_detector import DetectionsAnnotator, DetectionsCSVWriter, \
                                                       ObjectDetectorCSV
from videoanalytics.pipeline.sinks.roi import ROIView, ROIObjTest
from videoanalytics.pipeline.sinks.trackers.sort import SORT


from videoanalytics.pipeline.sinks.zmqpub import ZMQPub
from videoanalytics.pipeline.sinks.resizer import Resizer
from videoanalytics.pipeline.sinks.influxdb import InfluxDBWriter

from videoanalytics.pipeline.sinks.background import BackgroundExtractor1, BackgroundExtractor2



# Configuration
# -----------------------------------------------------------------------------

# Input
INPUT_VIDEO = "../data/media/barco.mp4"
#START_FRAME = 0

START_FRAME = 9000 # Redes
#START_FRAME = 10000 # Redes

MAX_FRAMES = None

# Detector
CSV_DETECTIONS_FILENAME = "../data/other/detections.csv"

# Detections Annotator
DETECTOR_CLASSES_FILENAME = "../data/models/coco/classes.txt"

# Output
OUTPUT_VIDEO = "../data/media/prueba-rois.mp4"

# ROIS
ROIS_FILENAME = "../data/other/rois.json"

# Components under development
# -----------------------------------------------------------------------------


# Pipeline definition
# -----------------------------------------------------------------------------

# 1. Crear el contexto en el que los bloques comparten información
g_context = {}



def create_pipeline1(context):
    # 2. Instanciar la pipeline (grafo dirigido)
    pipeline = nx.DiGraph()

    # 3. Agregar bloques
    pipeline.add_nodes_from([
        ( "input", {
          "component": VideoReader(context,
                                     video_path=INPUT_VIDEO,
                                     start_frame=START_FRAME,
                                     max_frames=MAX_FRAMES)
        }),
        
        ( "detector", {
          "component": ObjectDetectorCSV(context,CSV_DETECTIONS_FILENAME)
        }),

    ])

    # 4. Definir conexiones
    pipeline.add_edges_from([
        ("input", "detector")
    ])

    # 5. Eliminar bloques aislados
    pipeline.remove_nodes_from(list(nx.isolates(pipeline)))
    return pipeline

def create_pipeline2(context):
    # 2. Instanciar la pipeline (grafo dirigido)
    pipeline = nx.DiGraph()

    # 3. Agregar bloques
    pipeline.add_nodes_from([
        ( "input", {
          "component": VideoReader(context,
                                     video_path=INPUT_VIDEO,
                                     start_frame=START_FRAME,
                                     max_frames=MAX_FRAMES)
        }),

        ( "mog", {
          "component": BackgroundExtractor1(context)
        }),

        
        ( "detector", {
          "component": ObjectDetectorCSV(context,CSV_DETECTIONS_FILENAME)
        }),

        ( "tracker", {
            "component": SORT(context, max_age=200, min_hits=3, iou_threshold=0.3)
        }),
        
        ( "detector-annot", {
          "component": DetectionsAnnotator(context,class_names_filename=DETECTOR_CLASSES_FILENAME)
        }),    


        ( "roi-annot", {
          "component": ROIView(context,filename=ROIS_FILENAME)
        }),   

        ( "roi-test", {
          "component": ROIObjTest(context,filename=ROIS_FILENAME)
        }),   
        
        #( "writer", {
        #  "component": VideoWriter(context,filename=OUTPUT_VIDEO)
        #})

        ( "influxdb", {
            "component": InfluxDBWriter(context,variables_to_publish=[
                "q_izquierda_sup",
                "q_izquierda_inf",
                "q_derecha_sup",
                "q_derecha_inf",
                "q_timon",
                "q_total",
                "activity"
            ])
        } ),

        ( "zmqpub", {
          "component": ZMQPub(context,endpoint="tcp://127.0.0.1:5600")
        })
    ])

    # 4. Definir conexiones
    pipeline.add_edges_from([
        ("input", "mog"), 
        ("mog", "detector"), 
        #("detector", "detector-annot"),
        ("detector", "tracker"),
        ("detector", "roi-annot"),
        ("roi-annot", "roi-test"),
        #("detector-annot", "resizer"),
        ("roi-test", "influxdb"),
        #("resizer", "zmqpub")
        #("detector-annot", "writer")
    ])

    # 5. Eliminar bloques aislados
    pipeline.remove_nodes_from(list(nx.isolates(pipeline)))
    return pipeline


# Edición de ROIs (proviosorio)
# -----------------------------------------------------------------------------

g_roi = []


#define the events for the
# mouse_click.
def mouse_click(event, x, y, 
                flags, param):
    global g_context
    global g_roi
      
    # to check if left mouse 
    # button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
          
        # font for left click event
        font = cv2.FONT_HERSHEY_TRIPLEX
        LB = 'Left Button down'
          
        # display that left button 
        # was clicked.
        #cv2.putText(g_context["FRAME"], LB, (x, y), 
        #            font, 1, 
        #            (255, 255, 0), 
        #            2) 
        #cv2.imshow('Video', g_context["FRAME"])
        

    elif event == cv2.EVENT_LBUTTONUP:
        # font for left click event
        font = cv2.FONT_HERSHEY_TRIPLEX
        LB = 'Left Button up'
          
        # display that left button 
        # was clicked.
        #cv2.putText(g_context["FRAME"], LB, (x, y), 
        #            font, 1, 
        #            (255, 255, 0), 
        #            2) 
        g_roi.append([x,y])


def process_pipeline_ui(p,context):
    global g_roi

    seq = [p.nodes[x]['component'] for x in list(nx.topological_sort(p))]
    sources = [x for x in filter(lambda x: issubclass(type(x),Source),seq)]
    sinks = [x for x in filter(lambda x: issubclass(type(x),Sink),seq)]
    
    # Init
    print("Initializing pipeline")
    print("Sequence:", list(nx.topological_sort(p)))
    for x in seq:    
        x.setup()
    
    # Process
    print("Processing pipeline")
    eof_not_reached = False
    for x in sources:
        eof_not_reached |= x.read()


    # GUI CALLBACKS
    cv2.namedWindow('Principal', cv2.WINDOW_NORMAL)   
    #cv2.namedWindow('Análisis', cv2.WINDOW_NORMAL)   
    cv2.setMouseCallback("Principal", mouse_click)
    
    while eof_not_reached:
        for x in sinks:
            x.process()    

        #
        overlay = context["FRAME"].copy()

        # BEGIN GUI CODE
        if len(g_roi) > 2:
            converted_roi = np.int32([g_roi])            
            cv2.fillPoly(overlay, pts = converted_roi, color =(0,155,0))
            cv2.polylines(overlay, converted_roi, 5, (0,255,0))

            alpha = 0.4  # Transparency factor.
            # Following line overlays transparent rectangle over the image
            context["FRAME"] = cv2.addWeighted(overlay, alpha, context["FRAME"], 1 - alpha, 0)


        cv2.imshow("Principal", cv2.cvtColor(context["FRAME"], cv2.COLOR_BGR2RGB) )
        #cv2.imshow("Análisis", cv2.cvtColor(context["FRAME_TMP"], cv2.COLOR_BGR2RGB) )
        # END GUI CODE
            
        # Read next frame
        eof_not_reached = False
        for x in sources:
            eof_not_reached |= x.read()
        
        # Process input
        key_pressed = cv2.waitKey(1) & 0xFF    
        if key_pressed == 27:
            eof_not_reached = False
        # New ROI
        elif key_pressed == ord('n'):
            g_roi = []
        # Save ROI
        elif key_pressed == ord('s'):
            #converted_roi = np.int32([g_roi])       
            print(g_roi)
            #print(type(g_roi))
            #print(g_roi.shape)
        elif key_pressed == ord('1'):
            print("User command 1")
            nx.get_node_attributes(pipeline, 'component')['roi-annot'].toggle_display_enable()
        elif key_pressed == ord('2'):
            print("User command 2")
            nx.get_node_attributes(pipeline, 'component')['mog'].toggle_display_enable()
        elif key_pressed == ord('3'):
            print("User command 3")
            nx.get_node_attributes(pipeline, 'component')['tracker'].toggle_display_enable()
        elif key_pressed == ord('4'):
            print("User command 4")
        elif key_pressed == ord('5'):
            print("User command 5")
            
    # Shutdown    
    print("Shutting down pipeline")
    for x in seq:
        x.shutdown()    

    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    print("Pipeline processor")

    pipeline = create_pipeline2(g_context)

    # Process pipeline
    process_pipeline_ui(pipeline,g_context)

