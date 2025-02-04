# Ethiopian Medical Business Data Warehouse with Object Detection

A scalable data pipeline to collect, process, and analyze Ethiopian medical business data from Telegram channels, enhanced with YOLO-based object detection.

---

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Key Components](#key-components)
  - [1. Data Scraping and Collection Pipeline](#1-data-scraping-and-collection-pipeline)
  - [2. Data Cleaning and Transformation](#2-data-cleaning-and-transformation)
  - [3. Object Detection Using YOLO](#3-object-detection-using-yolo)
  - [4. Data Exposure via FastAPI](#4-data-exposure-via-fastapi)
- [Data Warehouse Design](#data-warehouse-design)
- [Installation & Setup](#installation--setup)

---

## Key Components

### 1. Data Scraping and Collection Pipeline

#### Tools
- **Telegram API Libraries**: `telethon` or `python-telegram-bot`
- **Scraping Framework**: Scrapy or custom async Python scripts
- **Storage**: Temporary AWS S3/MinIO bucket or local `./data/raw`

#### Steps
1. **Channel Discovery**: Identify public Telegram channels focused on Ethiopian medical businesses.
2. **Data Extraction**:
   - Text: Business names, contact info, addresses, services.
   - Images: Store in `raw_images/` with timestamps.
3. **Temporary Storage**: Save raw data as:
   - JSON files for text data.
   - JPG/PNG for images.
   - Compressed into daily batches (e.g., `2023-10-01_raw.zip`).

---

### 2. Data Cleaning and Transformation

#### Tools
- **DBT (Data Build Tool)**: For modular SQL transformations.
- **Pandas**: Python scripts for initial cleaning.

#### Process
1. **Cleaning**:
   - Remove duplicate records.
   - Filter urls.
   - Filter emojis.
2. **DBT Workflow**:
   - **Staging**: Raw data → Structured tables.
   - **Intermediate**: Join business data with geolocations.
   - **Mart Layer**: Aggregate tables for analytics.
     
     ---
### 3. Object Detection Using YOLO
●	Setting Up the Environment:
○	Ensure you have the necessary dependencies installed, including YOLO and its required libraries (e.g., OpenCV, TensorFlow, or PyTorch depending on the YOLO implementation).
pip install opencv-python
pip install torch torchvision  # for PyTorch-based YOLO
pip install tensorflow  # for TensorFlow-based YOLO

●	Downloading the YOLO Model
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
●	Preparing the Data
○	 Collect images from the Chemed Telegram Channel, https://t.me/lobelia4cosmetics
●	Use the pre-trained YOLO model to detect objects in the images.
●	Processing the Detection Results
○	Extract relevant data from the detection results, such as bounding box coordinates, confidence scores, and class labels.
●	Storing detection data to a database table.

---
### 4. Expose the collected data using Fast API
●	Setting Up the Environment:
○	Install FastAPI and Uvicorn
pip install fastapi uvicorn
●	Create a FastAPI Application
○	Set up a basic project structure for your FastAPI application.
expose_api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├──crud.py
●	Database Configuration
○	In the database.py configure the database connection using SQLAlchemy.
●	Creating Data Models
○	In the models.py define SQLAlchemy models for the database tables.
●	Creating Pydantic Schemas
○	In the schemas.py define Pydantic schemas for data validation and serialization.
●	CRUD Operations
○	In the crud.py implement CRUD (Create, Read, Update, Delete) operations for the database.
●	Creating API Endpoints
○	In the main.py define the API endpoints using FastAPI.

---
git clone https://github.com/Abrham111/kara-solutions-data-warehouse.git
pip install -r requirements.txt
