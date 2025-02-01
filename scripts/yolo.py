import os
import torch
import cv2
import psycopg2
import logging
from yolov5 import detect
from dotenv import load_dotenv

class YOLOObjectDetector:
    def __init__(self, image_dir):
        """
        Initialize the YOLO Object Detector.

        :param image_dir: Path to the directory containing images for object detection.
        :param db_config: Dictionary containing database connection details.

        """

        load_dotenv()
        db_config = {
            'dbname': 'DB_NAME_yolo',
            'user': 'DB_USER_yolo',
            'password': 'DB_PASS_yolo',
            'host': 'DB_HOST_yolo',
            'port': 'DB_PORT_yolo'
        }

        self.image_dir = image_dir
        self.db_config = db_config
        self.detection_results = []
        
        # Configure logging
        logging.basicConfig(filename='object_detection.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Load the YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or 'yolov5m', 'yolov5l', 'yolov5x'

    def detect_objects(self):
        """
        Perform object detection on images in the specified directory.
        """
        try:
            self.logger.info("Starting object detection process.")
            
            # Loop through each image in the directory
            for image_name in os.listdir(self.image_dir):
                image_path = os.path.join(self.image_dir, image_name)
                
                # Perform object detection
                results = self.model(image_path)
                
                # Extract detection results
                detections = results.xyxy[0].numpy()  # detections are in the format [x1, y1, x2, y2, confidence, class]
                
                # Store the results
                for detection in detections:
                    self.detection_results.append({
                        'image_name': image_name,
                        'x1': detection[0],
                        'y1': detection[1],
                        'x2': detection[2],
                        'y2': detection[3],
                        'confidence': detection[4],
                        'class': detection[5]
                    })

            self.logger.info("Object detection completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during object detection: {e}")
            raise

    def store_results_in_db(self):
        """
        Store the detection results in a PostgreSQL database.
        """
        try:
            self.logger.info("Connecting to the database to store detection results.")
            
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )

            # Create a cursor object
            cur = conn.cursor()

            # Create a table to store detection results (if it doesn't exist)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id SERIAL PRIMARY KEY,
                image_name TEXT,
                x1 FLOAT,
                y1 FLOAT,
                x2 FLOAT,
                y2 FLOAT,
                confidence FLOAT,
                class INT
            )
            """)

            # Insert detection results into the database
            for result in self.detection_results:
                cur.execute("""
                INSERT INTO detections (image_name, x1, y1, x2, y2, confidence, class)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (result['image_name'], result['x1'], result['y1'], result['x2'], result['y2'], result['confidence'], result['class']))

            # Commit the transaction
            conn.commit()
            self.logger.info("Detection results stored in the database successfully.")

        except Exception as e:
            self.logger.error(f"An error occurred while storing results in the database: {e}")
            raise
        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()
            self.logger.info("Database connection closed.")

    def run(self):
        """
        Run the entire process: object detection and storing results in the database.
        """
        try:
            self.detect_objects()
            self.store_results_in_db()
        except Exception as e:
            self.logger.error(f"An error occurred in the run process: {e}")
            raise


if __name__ == "__main__":
    # Configuration for the database
    load_dotenv()
    db_config = {
        'dbname': 'DB_NAME',
        'user': 'DB_USER',
        'password': 'DB_PASS',
        'host': 'DB_HOST',
        'port': 'DB_PORT'
    }

    # Path to the directory containing images
    image_dir = '/home/nahomnadew/Desktop/10x/week7/Kara_Solutions/data/photos'

    # Create an instance of the YOLOObjectDetector class
    detector = YOLOObjectDetector(image_dir=image_dir, db_config=db_config)

    # Run the object detection and database storage process
    detector.run()