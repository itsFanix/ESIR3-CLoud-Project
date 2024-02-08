import torch
import cv2
from retry import retry
import pika
import logging


logging.basicConfig(level=logging.INFO)


@retry(delay=5, backoff=2, max_delay=60,logger=None)
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    return connection


def detect_animals(video_path):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    cap = cv2.VideoCapture(video_path)
    animalsClasse = ["bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]
    animalsInVideo = []
    realAnimals = []
    while True:
        frame = cap.read()[1]
        if frame is None:
            break
        result = model(frame)
        df = result.pandas().xyxy[0]
        for ind in df.index:
            x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
            x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
            label = df['name'][ind]
            confidence = df['confidence'][ind]
            text = f'{label} {confidence:.2f}'
            if label in animalsClasse:
                objet = {"label": label, "confidence": confidence.round(2)}
                animalsInVideo.append(objet)
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        #     cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.9, (36, 255, 12), 2)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(10)
    cap.release()
    cv2.destroyAllWindows()
    for animal in animalsInVideo:
        if animal["label"] not in [animal["label"] for animal in realAnimals]:
            realAnimals.append(animal)
        else:
            for realAnimal in realAnimals:
                if realAnimal["label"] == animal["label"]:
                    if realAnimal["confidence"] < animal["confidence"]:
                        realAnimal["confidence"] = animal["confidence"]
    return realAnimals


def main():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='metadataFileQueue')
    logging.info('Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        logging.info("########################################################")
        logging.info(f" Received   {body} ")
        metadatafile = body.decode('utf-8')
        logging.info(f"Processing {metadatafile}")
        # logging.info(f"Processed {body.decode('utf-8')}")
    
    channel.basic_consume(queue='metadataFileQueue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    # video_path = 'data/cat.mp4'
    # print(detect_animals(video_path))


if __name__ == "__main__":
    main()

