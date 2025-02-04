# AI-Powered Data Warehouse for Ethiopian Medical Businesses

## Overview
This project aims to build a data warehouse to store and analyze Ethiopian medical business data scraped from Telegram channels. The data warehouse will support object detection using YOLO and integrate ETL/ELT frameworks to ensure efficient data transformation and analysis. 

The project is structured into multiple tasks, including data scraping, cleaning, transformation, object detection, database management, and API development. Each task plays a crucial role in ensuring the completeness and usability of the data.

---

## Features
- **Data Scraping & Collection**: Extracts relevant data from Telegram channels using the `telethon` library.
- **Data Cleaning & Transformation**: Implements robust ETL/ELT processes using DBT to ensure data quality.
- **Object Detection**: Utilizes YOLOv5 to detect and classify objects within images scraped from Telegram.
- **Data Warehousing**: Stores structured data in a PostgreSQL database for efficient querying and analysis.
- **API Development**: Builds a FastAPI-based interface to expose the collected and processed data.

---

## Tech Stack
- **Web Scraping**: `telethon`, `BeautifulSoup`, `Scrapy`, `Selenium`
- **Database**: PostgreSQL, SQLAlchemy
- **Data Processing**: Pandas, DBT
- **Object Detection**: YOLOv5, OpenCV, PyTorch
- **API Development**: FastAPI, Pydantic, Uvicorn

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/chapi1420/Kara_Solutions
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Task Breakdown

### Task 1 - Data Scraping & Collection
Data is collected from various Ethiopian medical Telegram channels. The process involves:
- **Utilizing Telethon**: A Python client library for Telegram API to extract messages, media, and metadata.
- **Scraping Images**: Gathering images from channels for object detection.
- **Handling Rate Limits**: Implementing delays and error handling to avoid API bans.
- **Storing Raw Data**: Temporarily storing extracted data in JSON/CSV format before transformation.
- **Logging & Monitoring**: Capturing logs to track progress and errors.

Run the scraper using:
```bash
python scrape_telegram.py
```

---

### Task 2 - Data Cleaning & Transformation
Raw data collected from Telegram often contains inconsistencies. This step includes:
- **Removing Duplicates**: Ensuring no redundant records.
- **Handling Missing Values**: Filling or dropping missing fields.
- **Standardizing Formats**: Converting date formats, text normalization, and type corrections.
- **Implementing DBT Models**: Running transformations on raw data and loading it into the warehouse.

To transform data using DBT:
```bash
dbt run
```

---

### Task 3 - Object Detection with YOLO
YOLO (You Only Look Once) is used to analyze images for relevant medical-related objects. The process involves:
- **Downloading Pre-trained YOLOv5 Model**
- **Preprocessing Images**: Resizing and normalizing image formats.
- **Running Object Detection**: Detecting and classifying objects in medical-related images.
- **Extracting Metadata**: Storing bounding boxes, labels, and confidence scores in the database.

To run object detection:
```bash
python detect_objects.py --source data/images
```

---

### Task 4 - Data Warehousing
The cleaned and processed data is stored in PostgreSQL. The steps include:
- **Schema Design**: Creating relational tables optimized for queries.
- **Loading Data**: Using SQLAlchemy to insert data into tables.
- **Indexing & Optimization**: Ensuring efficient querying with indexes.
- **Data Validation**: Verifying integrity and consistency of stored data.

---

### Task 5 - API Development
FastAPI is used to expose the collected and processed data through a RESTful API. The API includes:
- **Database Connection**: Using SQLAlchemy for interaction with PostgreSQL.
- **Creating Pydantic Schemas**: Defining models for validation and serialization.
- **CRUD Operations**: Implementing create, read, update, and delete functionalities.
- **API Endpoints**: Allowing users to fetch relevant data.

To start the API server:
```bash
uvicorn main:app --reload
```

---

## Project Structure
```
project/
├── data/-->dvc controlled
├── dbt_for_elt/
├── API/
   ├──main.py
   ├──schema.py
   ├──database.py
   ├──model.py
   ├──crud.py
├──notebooks/
   ├──cleaning.ipynb
   ├──database.ipynb
   ├──yolo.ipynb
├──logs/
├── yolov5.pt
├── scripts/
│   ├── scrape_telegram.py
│   ├── yolo.py.py
    ├──database.py
├──target/---> dvc controlled
├──yolov5/---> dvc controlled
      ├──results/----->dvc
├── requirements.txt
├── README.md
└── schema.sql
```

---

## Deliverables
- **GitHub Repository**: Contains code and implementation.
- **Final Report**: Blog post or PDF documenting the project.
- **API Endpoints**: Exposes the processed data for external access.

---

## References
- [YOLOv5 Documentation](https://github.com/ultralytics/yolov5)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [DBT Guide](https://docs.getdbt.com/docs/introduction)

---

## Contributors
- **Mahlet** (Mentor)
- **Elias** (Mentor)
- **Rediet** (Mentor)
- **Kerod** (Mentor)
- **Emitinan** (Mentor)
- **Rehmet** (Mentor)

---

