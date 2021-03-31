import argparse
import cv2
import time
import os
from glob import glob
from pathlib import Path

class YOLODetector:
    CONFIDENCE_THRESHOLD = 0.6
    NMS_THRESHOLD = 0.6
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

    def __init__(self,weights_filename,cfg_filename,classes_filename):
        self.net = cv2.dnn.readNet( weights_filename, cfg_filename )
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

            
        self.class_names = []
        with open(classes_filename, "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

    def detect(self,img):
        classes, scores, boxes = self.model.detect(img, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        return classes, scores, boxes

    def draw_bounding_boxes(self,img, classes, scores, boxes):
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s : %f" % (self.class_names[classid[0]], score)
            cv2.rectangle(img, box, color, 2)
            cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def get_bounding_boxes_str(self,classes, scores, boxes):
        tmp = ""
        for (classid, score, box) in zip(classes, scores, boxes):
            tmp += "%d %.3f %.3f %.3f %.3f %.3f\n" % (
                classid[0], boxes[0], boxes[1], boxes[2], boxes[3], score
            )
        return tmp

def process_image(filename,detector,args):
    print("Processing image %s" % filename)

    # Open image
    img = cv2.imread(filename)

    # Detect
    classes, scores, boxes = detector.detect(img)
    detector.draw_bounding_boxes(img,classes, scores, boxes)

    print("Total detections: %d" % len(classes))

    # Save image with detections
    img_base_name = os.path.splitext(os.path.basename(args.input))[0]
    img_pred_filename = args.output+"/"+img_base_name+"-pred.jpg"
    cv2.imwrite(img_pred_filename, img)
    print("Saved image with predictions to %s" % img_pred_filename)

    # Save txt with bounding-boxes    
    txt_pred_filename = args.output+"/"+img_base_name+"-pred.txt"
    with open(txt_pred_filename,"wt") as fp:
        txt = detector.get_bounding_boxes_str(classes, scores, boxes)        
        fp.write(txt)
    print("Saved txt with predictions to %s" % txt_pred_filename)        
    return

def process_batch(filename,detector,args):    
    # Get file list
    # FIXME
    files = []

    # Process each input
    for x in files:        
        input_ext = os.path.splitext(x)[1]
        input_type = get_input_type(input_ext)
        if "unsupported" != input_type:
            process_input(input_type, x,detector,args)
        else:
            print("Unsupported input type.")
            exit()

    return

def process_video(filename,detector,args):

    # Open input video
    cap = cv2.VideoCapture(filename)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    input_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))
    input_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    print("Reading %s. Total frames: %d" % (filename, total_frames))

    start_frame = 0
    if args.start_frame != None:
        start_frame = args.start_frame
    current_frame = args.start_frame        
    
    max_frames = total_frames
    if args.max_frames != None:
        max_frames = args.max_frames
        
    # Create videowriter
    video_base_name = os.path.splitext(os.path.basename(args.input))[0]
    video_pred_filename = video_base_name+"-pred.mp4"

    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    out = cv2.VideoWriter(
            video_pred_filename, 
            cv2.CAP_FFMPEG, 
            fourcc, 
            input_fps, 
            (input_w,input_h)
        )
        
    if False == out.isOpened():
        raise ValueError("Could not open WriterLayer output")

    # For each frame
    (grabbed, frame) = cap.read()
    while grabbed and (current_frame < max_frames):
        print("Frame %d/%d" % (current_frame,max_frames))
        #start = time.time()
        classes, scores, boxes = detector.detect(frame)
        detector.draw_bounding_boxes(frame,classes, scores, boxes)
        #end = time.time()

        out.write(frame)

        (grabbed, frame) = cap.read()
        current_frame+=1    

    # Release input,output
    cap.release()
    out.release()
    print("Saved video to %s" % video_pred_filename)
    return    

def get_input_type(file_extension):
    supported_img_extensions = [".jpg",".jpeg"]
    supported_video_extensions = [".mp4",".webm",".avi"]
    supported_batch_extensions = [".txt"]

    if file_extension in supported_img_extensions:
        return "image"
    elif file_extension in supported_video_extensions:
        return "video"
    elif file_extension in supported_batch_extensions:
        return "batch"
    else:
        return "unsupported"


def process_input(input_type, filename,detector,args):
    processors = {
        "image": process_image,
        "video": process_video,
        "batch": process_batch
    }
    return processors[input_type](filename,detector,args)

def scan_for_model_files(model_path):
    print("Looking for model files in %s" % model_path)
    candidates = glob("%s/*.txt" % args.model)
    classes_txt = candidates[0] if len(candidates) >= 1 else None
    print("Classes: %s" % classes_txt)

    candidates = glob("%s/*.weights" % model_path)
    model_weights = candidates[0] if len(candidates) >= 1 else None
    print("Weights: %s" % model_weights)

    candidates = glob("%s/*.cfg" % model_path)
    model_cfg = candidates[0] if len(candidates) >= 1 else None
    print("Config: %s" % model_cfg)

    assert(classes_txt and model_weights and model_cfg)
    return model_weights,model_cfg,classes_txt

def test(args):
    print("Test")    
    exit()
    
if __name__=="__main__":     
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', type=str, help='Single image, image batch, or video batch')
    parser.add_argument('--output', type=str, help='Output path',default="output")
    parser.add_argument('--model', type=str, help='Darknet model path',default=None)
    parser.add_argument('--model-weights', type=str, help='Darknet model weights')
    parser.add_argument('--model-cfg', type=str, help='Darknet model configuration')
    parser.add_argument('--classes-txt', type=str, help='Darknet txt file with class names')
    parser.add_argument('--start-frame', type=int, help='Starting frame (for video input)',default=0)
    parser.add_argument('--max-frames', type=int, help='Max frames (for video input)',default=None)
    args = parser.parse_args()

    #test(args)

    if not args.input:
        print("No input was specified.")
        exit()

    # Instance detector
    if args.model is not None:
        model_weights,model_cfg,model_classes_txt = scan_for_model_files(args.model )
    else:
        model_weights,model_cfg,model_classes_txt = args.model_weights,args.model_cfg,args.classes_txt

    detector = YOLODetector(model_weights,model_cfg,model_classes_txt)
    if not detector:
        print("Could not instance detector.")
        exit()    
    
    # Output path
    if not os.path.exists(args.output):
        output_path = Path(args.output)
        output_path.mkdir(parents=True)

    # Process input
    input_ext = os.path.splitext(args.input)[1]
    input_type = get_input_type(input_ext)
    if "unsupported" != input_type:
        process_input(input_type, args.input,detector,args)
    else:
        print("Unsupported input type.")
        exit()