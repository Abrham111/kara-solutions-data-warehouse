### Overview
Build a data warehouse to store data on Ethiopian medical businesses scraped from Telegram channels. Integrate object detection using YOLO for enhanced data analysis.

1. **Data Scraping and Collection Pipeline**
  - Utilize Telegram API or custom scripts to extract data from public Telegram channels.
  - Collect images for object detection.
  - Store raw data temporarily before processing.

2. **Data Cleaning and Transformation**
  - Remove duplicates, handle missing values, standardize formats, and validate data.
  - Use DBT for data transformation and load into the data warehouse.

3. **Object Detection Using YOLO**
  - Set up the environment and download the YOLO model.
  - Detect objects in collected images and store detection data.

4. **Expose Data Using FastAPI**
  - Set up FastAPI and create endpoints for data access.
