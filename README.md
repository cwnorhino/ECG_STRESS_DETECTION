# ECG Stress and Abnormality Detection System
I was reading a paper on stress detection using different sensors
using ECG signals one day and decided that I should try making 
a real-time **ECG-based health monitoring system** using
**ESP32**(I always have an ESP32), **AD8232 sensor** ( these things were kinda expensive), and **Machine Learning** ( I read a bit of hands on machine learning using scikit learn book and called it a day) to detect stress levels and heart irregularities. (NOTE: the paper that I was reading is mentioned in the references section)

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

-   Real-time ECG acquisition using ESP32
-   Wireless data transmission via WiFi
-   Machine Learning-based stress detection (SVM)
-   Signal filtering and processing
-   HRV feature extraction

------------------------------------------------------------------------

## Hardware Components

-   ESP32
-   AD8232 ECG Sensor
-   Electrodes
-   Breadboard & Wires
-   Batteries
-   Buck Converter

------------------------------------------------------------------------

## Software

-   Python
-   NumPy, SciPy
-   Machine Learning (SVM): The model was trained on this dataset: https://www.kaggle.com/datasets/apithm/ecg-and-eeg-stress-features

------------------------------------------------------------------------

## Working Principle

1.  ECG captured via electrodes
2.  Processed via AD8232
3.  ESP32 samples and sends data
4.  Python processes signal
5.  ML model predicts stress
6.  If because of noise and stuff signals are bad and it is difficult to detect HRV features then I also got a code running to detect using BPM which lowkey defeats the ML purpose but GOD I HATE NOISE

------------------------------------------------------------------------

## Results

-   75% accuracy on the ML dataset 
-   Real-time ECG monitoring
-   Detects stress & irregularities

------------------------------------------------------------------------

## Limitations

-   Sensitive to noise ( I HATE NOISE)
-   Limited dataset
-   Not medical-grade
-   I NEED A LARGER DATASET AND BETTER ELECTRODES

------------------------------------------------------------------------

## some photos 

![image alt](https://github.com/cwnorhino/ECG_STRESS_DETECTION/blob/0181ef793b309926a523a7323d597489c633cc4d/assets/training%20vs%20validation%20accuracy.jpeg)
training V/s Validation accuracy learning curva

![image alt](https://github.com/cwnorhino/ECG_STRESS_DETECTION/blob/0181ef793b309926a523a7323d597489c633cc4d/assets/AAAAAAAAAAAAAAAAAAAAAAAAAA.jpeg)
ESP32 Circuit with AD8232

![image alt](https://github.com/cwnorhino/ECG_STRESS_DETECTION/blob/0181ef793b309926a523a7323d597489c633cc4d/assets/raw%20ECG.jpeg)
Raw ECG signal before filtering

![image alt](https://github.com/cwnorhino/ECG_STRESS_DETECTION/blob/0181ef793b309926a523a7323d597489c633cc4d/assets/filtered%20ecg.jpeg)
Filtered ECG Signal

--------------------------------------------------------------------------

## Future Scope

-   Deep learning models (please someone send me a larger dataset)
-   Better sensors
-   Using PPG sensors to make it portable but then HRV wont be able to get extracted though
-   Mobile app (I dont know App dev)
-   Wearable system (inshallah)

-------------------------------------------------------------------------

## References
- https://ieeexplore.ieee.org/abstract/document/10946259
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6085204/


