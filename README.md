# 🎯 Bachelor Project: Geolocation of Detected Objects in Aerial Imagery

## 🔍 Problem Statement

**Main Question:**  
How can the geographical coordinates of objects detected within aerial images be determined?

**Sub-questions:**  
- What data is required to accurately determine an object’s geographic location from an image?  
- How can image metadata be transformed into precise coordinates?  
- How can objects of interest be reliably detected in aerial images?


## 📦 Project Structure

├── .github/workflows # CI pipelines and test automation

├── backend # Coordinate transformation logic and data services

├── frontend # Interface for visualizing detections and locations

├── notebooks # (Jupyter)

├── docker-compose.yaml # Container orchestration

├── .gitignore 

## 📅 Timeline Highlights

- **Jan:** Tool onboarding, data familiarization  
- **Feb:** Geospatial transformations (pixel → coordinate)  
- **Mar:** PoC for geolocation, begin object detection  
- **Apr:** Object detection refinement, draft methodology  
- **May:** Final testing, results, and thesis writing

## 🧩 Interesting Components

### 🔧 `backend/src/georeferencing`

This module handles the core transformation from **2D image pixel positions to 3D geographic coordinates**.

Techniques such as **Homography estimation** and **camera projection geometry** are applied to align real-world coordinates with the image plane.

---

### 🧠 `backend/src/logic/object_detection_logic.py`

Implements logic for detecting **cars in oblique aerial photos** and processing predictions.

---

### 📓 `notebooks`

- **Model Training**

- **Geolocation Error Analysis**

---
