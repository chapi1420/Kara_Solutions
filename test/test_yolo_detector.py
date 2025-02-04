import unittest
from unittest.mock import patch, MagicMock
import os
from ..scripts.yolo import YOLOObjectDetector  
class TestYOLOObjectDetector(unittest.TestCase):
    
    @patch("torch.hub.load")
    @patch("os.listdir")
    def setUp(self, mock_listdir, mock_torch_hub_load):
        # Mock the YOLO 
        self.mock_model = MagicMock()
        mock_torch_hub_load.return_value = self.mock_model
        
        # Mock listdir to simulate image files
        mock_listdir.return_value = ["image1.jpg", "image2.jpg"]
        
        # Create a test instance of YOLOObjectDetector
        self.image_dir = "test_images"
        self.db_config = {
            'dbname': 'test_db',
            'user': 'test_user',
            'password': 'test_pass',
            'host': 'localhost',
            'port': '5432'
        }
        self.detector = YOLOObjectDetector(self.image_dir, self.db_config)

    @patch("torch.hub.load")
    def test_model_loading(self, mock_torch_hub_load):
        # Check if the model is loaded correctly
        mock_torch_hub_load.assert_called_with('ultralytics/yolov5', 'yolov5s')

    @patch("torch.hub.load")
    @patch("os.path.join", side_effect=lambda a, b: f"{a}/{b}")
    def test_detect_objects(self, mock_path_join, mock_torch_hub_load):
        # Mock detection results
        mock_results = MagicMock()
        mock_results.xyxy = [
            MagicMock(numpy=lambda: [[10, 20, 30, 40, 0.9, 1]])
        ]
        self.detector.model.return_value = mock_results

        # Run detection
        self.detector.detect_objects()
        
        # Verify results are stored
        self.assertEqual(len(self.detector.detection_results), 1)
        self.assertEqual(self.detector.detection_results[0]['confidence'], 0.9)

    @patch("psycopg2.connect")
    def test_store_results_in_db(self, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Sample detection results
        self.detector.detection_results = [{
            'image_name': 'image1.jpg',
            'x1': 10, 'y1': 20, 'x2': 30, 'y2': 40,
            'confidence': 0.9, 'class': 1
        }]

        # Run the store_results_in_db method
        self.detector.store_results_in_db()

        # Check if the INSERT statement was executed
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()