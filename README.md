# Automated Facial Recognition Door Access System

This project implements an **automated door access control system using facial recognition**.  
The system identifies authorized users through a camera and grants access by communicating with an Arduino-controlled door lock mechanism.

The project combines **computer vision, Python, and hardware control** to simulate a smart security system.

---

# Project Overview

The system captures an image using a camera and compares the detected face with a database of authorized users.  
If the face is recognized, the system sends a signal to an Arduino board that unlocks the door.

If the face is not recognized, access is denied.

This type of system can be used in:

- smart homes
- secure offices
- laboratories
- restricted access areas
- smart security systems

---

# System Architecture

The workflow of the system is the following:

Camera → Python Face Recognition → Serial Communication → Arduino → Door Unlock

1. The camera captures an image of the user.
2. Python detects and encodes the face.
3. The system compares the detected face with stored known faces.
4. If a match is found, a signal is sent to the Arduino.
5. Arduino activates the door lock mechanism.

---

# Features

## Face Detection
The system detects human faces using the camera and computer vision algorithms.

## Face Recognition
Detected faces are compared with the images stored in the **knownFaces** folder.

## Access Control
Authorized users are granted access while unknown users are denied.

## Serial Communication
Python communicates with the Arduino board through serial communication.

## Image Logging
Captured images are stored in the **testedFaces** folder for debugging and monitoring.

---

# Technologies Used

- Python
- OpenCV
- Face Recognition Library
- Arduino
- Serial Communication
- NumPy

---

# Project Structure
```
facial-recognition-door-access
│
├── README.md
├── capturePhoto.py
├── faceRec.py
├── main.py
├── serialCommunication.py
│
├── arduino
│ └── cod.ino
│
├── knownFaces
│ └── images of authorized users
│
├── testedFaces
│ └── captured images during testing
│
└── requirements.txt

```


# How the System Works

### Step 1 – Capture Image
The system captures an image from the camera.

### Step 2 – Face Encoding
Facial features are extracted using the face recognition algorithm.

### Step 3 – Face Comparison
The encoded face is compared against the images in the **knownFaces** folder.

### Step 4 – Access Decision

If the face matches an authorized user:

Access Granted → Arduino unlocks the door


If the face is unknown:

Access Denied


---

# Installation

### 1 Install Required Libraries


pip install -r requirements.txt


---

### 2 Connect Arduino

Upload the Arduino code located in:


arduino/cod.ino


This code controls the door unlocking mechanism.

---

### 3 Run the System

Run the main Python script:


python main.py


The camera will start and the system will begin detecting faces.

---

# Requirements

The required Python libraries are listed in `requirements.txt`.

Example:


opencv-python
face-recognition
pyserial
numpy


---

# Future Improvements

Possible improvements for the system:

- real-time video recognition
- database integration for user management
- improved recognition accuracy
- access logs and security monitoring
- mobile notifications for unauthorized access attempts

---

# Authors

Brătian Melisa-Adriana 


---

# Academic Context

This project was developed as part of an academic project
