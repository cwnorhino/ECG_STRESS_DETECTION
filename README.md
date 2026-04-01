# ECG Stress and Abnormality Detection System

A real-time **ECG-based health monitoring system** built using
**ESP32**, **AD8232 sensor**, and **Machine Learning** to detect stress
levels and heart irregularities.

------------------------------------------------------------------------

## Overview

This project focuses on acquiring ECG signals, processing them, and
analyzing heart activity to detect:

-   Heart Rate (BPM)
-   Heart Rate Variability (HRV)
-   Stress Levels (via ML model)
-   Arrhythmia (irregular heart rhythms)

------------------------------------------------------------------------

## Features

-   Real-time ECG acquisition using ESP32\
-   Wireless data transmission via WiFi\
-   Machine Learning-based stress detection (SVM)\
-   Signal filtering and processing\
-   HRV feature extraction

------------------------------------------------------------------------

## Hardware Components

-   ESP32\
-   AD8232 ECG Sensor\
-   Electrodes\
-   Breadboard & Wires\
-   Batteries\
-   Buck Converter

------------------------------------------------------------------------

## Software

-   Python\
-   NumPy, SciPy\
-   Machine Learning (SVM)

------------------------------------------------------------------------

## Working Principle

1.  ECG captured via electrodes\
2.  Processed via AD8232\
3.  ESP32 samples and sends data\
4.  Python processes signal\
5.  ML model predicts stress

------------------------------------------------------------------------

## Results

-   \~75% accuracy\
-   Real-time ECG monitoring\
-   Detects stress & irregularities

------------------------------------------------------------------------

## Limitations

-   Sensitive to noise\
-   Limited dataset\
-   Not medical-grade

------------------------------------------------------------------------

## Future Scope

-   Deep learning models\
-   Better sensors\
-   Mobile app\
-   Wearable system


