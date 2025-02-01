import torch
import cv2
import logging
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine

class YOLOObjectDetection:
    def __init__(self, model_name='yolov5s', database_url=None):
        """Initialize YOLO model and database connection."""
        self.model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
        self.database_url = database_url
        if database_url:
            self.engine = create_engine(database_url)
        
        logging.basicConfig(filename="yolo_detection.log", level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("YOLO model initialized.")

    def detect_objects(self, image_path):
        """Run YOLO object detection on an image."""
        logging.info(f"Detecting objects in {image_path}")
        results = self.model(image_path)
        return results

    def process_results(self, results):
        """Extract relevant data from detection results."""
        detections = results.pandas().xyxy[0]  # Get detection details
        logging.info(f"Processed results: {len(detections)} objects detected.")
        return detections

    def save_results_to_db(self, detections, table_name='object_detections'):
        """Save detection results to a database."""
        if self.database_url:
            detections.to_sql(table_name, con=self.engine, if_exists='append', index=False)
            logging.info("Detection results saved to database.")
        else:
            logging.warning("Database URL not provided. Skipping database storage.")

    def show_results(self, results):
        """Display detection results on the image."""
        logging.info("Displaying results.")
        results.show()

    def detect_and_store(self, image_path):
        """Perform end-to-end detection and store results in the database."""
        logging.info(f"Starting detection pipeline for {image_path}")
        results = self.detect_objects(image_path)
        detections = self.process_results(results)
        self.show_results(results)
        self.save_results_to_db(detections)
        logging.info("Detection pipeline completed successfully.")
        return detections
