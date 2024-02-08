import cv2
import numpy as np
from retry import retry
import pika
import logging

logging.basicConfig(level=logging.INFO)


@retry(delay=5, backoff=2, max_delay=60,logger=None)
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    return connection





def load_yolo():
    net = cv2.dnn.readNet("yolo_files/yolov3.cfg", "yolo_files/yolov3.weights")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    classes = []
    with open("yolo_files/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers


def detect_objects(img, net, outputLayers):	
        

    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(416, 416), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    outputs = np.vstack(outputs) # combine the 3 output groups into 1 (10647, 85)
    return outputs

def get_box_dimensions(outputs, height, width):
    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        scores = output[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.8:
            center_x = int(output[0] * width)
            center_y = int(output[1] * height)
            w = int(output[2] * width)
            h = int(output[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confs.append(float(confidence))
            class_ids.append(class_id)
    return boxes, confs, class_ids

#    for output in outputs:
#         scores = output[5:]
#         classID = np.argmax(scores)
#         confidence = scores[classID]
#         if confidence > conf:
#             x, y, w, h = output[:4] * np.array([W, H, W, H])
#             p0 = int(x - w//2), int(y - h//2)
#             p1 = int(x + w//2), int(y + h//2)
#             boxes.append([*p0, int(w), int(h)])
#             confidences.append(float(confidence))
#             classIDs.append(classID)

    # for output in outputs:
    #     for detect in output:
    #         scores = detect[5:]
    #         class_id = np.argmax(scores)
    #         confidence = scores[class_id]
    #         if confidence > 0.5:
    #             center_x = int(detect[0] * width)
    #             center_y = int(detect[1] * height)
    #             w = int(detect[2] * width)
    #             h = int(detect[3] * height)
    #             x = int(center_x - w / 2)
    #             y = int(center_y - h / 2)
    #             boxes.append([x, y, w, h])
    #             confs.append(float(confidence))
    #             class_ids.append(class_id)
    # return boxes, confs, class_ids

def draw_labels(boxes, confs, class_ids, classes, img, colors):
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(indexes)> 0:
        for i in indexes.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            label = str(classes[class_ids[i]])
            font_scale = 1  
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h),color, 2)
            cv2.putText(img, label, (x, y - 10), font, font_scale, color, 2)

    # for i in range(len(boxes)):
    #     if i in indexes:
    #         x, y, w, h = boxes[i]
    #         label = str(classes[class_ids[i]])
    #         # label_color = (255, 0, 0)  # 
    #         font_scale = 1  
    #         color = colors[class_ids[i]]
    #         cv2.rectangle(img, (x, y), (x + w, y + h),color, 2)
    #         cv2.putText(img, label, (x, y - 10), font, font_scale, color, 2)
    return img


def image_detection(video_path, net, classes, output_layers, colors):
    animalInVideo =  []
    batch_size =5

    cap = cv2.VideoCapture(video_path)

   
   
    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape
        outputs = detect_objects(frame, net, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        frame = draw_labels(boxes, confs, class_ids, classes, frame, colors)  # Updated line
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == 27:  # Press ESC to exit
            break
    cap.release()
    cv2.destroyAllWindows()
    
    # _, frame = cap.read()
    # height, width, channels = frame.shape
    # outputs = detect_objects(frame, net, output_layers)
    # boxes, confs, class_ids = get_box_dimensions(outputs, height, width)

    # animalsInVideo = [classes[i] for i in class_ids if classes[i] in animalsClasse]
    #     # frame = draw_labels(boxes, confs, class_ids, classes, frame)  # Updated line
    #     # cv2.imshow("Video", frame)
    #     # key = cv2.waitKey(1)
    #     # if key == 27:  # Press ESC to exit
    #     #     break
    # print(animalsInVideo)
    # cap.release()
    # cv2.destroyAllWindows()

def run(video_name):
    # video_path = f"data/{video_name}"

    net, classes, output_layers = load_yolo()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    image_detection(video_name, net, classes, output_layers, colors)
    logging.info(f"Processed {video_name}")

def main():
    logging.info("###############################")
    run("video2.mp4")
    # connection = connect_to_rabbitmq()
    # channel = connection.channel()
    # channel.queue_declare(queue='metadataFileQueue')
    # logging.info('Waiting for messages. To exit press CTRL+C')

    # def callback(ch, method, properties, body):
    #     logging.info("########################################################")
    #     logging.info(f" Received   {body} ")
    #     run(body.decode('utf-8'))
    #     logging.info(f"Processed {body.decode('utf-8')}")
    
    # channel.basic_consume(queue='metadataFileQueue', on_message_callback=callback, auto_ack=True)
    # channel.start_consuming()


if __name__ == '__main__':
    main()
