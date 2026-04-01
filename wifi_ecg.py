import socket
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch, savgol_filter
import neurokit2 as nk
import pandas as pd
import joblib

HOST = ''
PORT = 80



# LOAD MODEL

model = joblib.load("svm_model_2dataset.pkl")
scaler = joblib.load("scaler.pkl")



# READ ECG

def read_ecg(duration=10, fs=250):
    s = socket.socket()
    s.connect((HOST, PORT))

    buffer = ""
    data = []
    samples = duration * fs

    while len(data) < samples:
        chunk = s.recv(1024).decode()

        if not chunk:
            break

        buffer += chunk
        lines = buffer.split("\n")
        buffer = lines[-1]

        for line in lines[:-1]:
            try:
                val = int(line.strip())
                data.append(val)
            except:
                continue

    s.close()
    print("Collected samples:", len(data))
    return np.array(data)



# FILTERS

def bandpass(signal, fs=250):
    b, a = butter(3, [0.5/(fs/2), 40/(fs/2)], btype='band')
    return filtfilt(b, a, signal)

def notch_filter(signal, fs=250):
    b, a = iirnotch(50, 30, fs)
    return filtfilt(b, a, signal)



# NORMALIZE

def normalize(ecg):
    ecg = ecg - np.median(ecg)
    std = np.std(ecg)
    return ecg if std == 0 else ecg / std



# PEAK DETECTION

def get_rpeaks(ecg, fs=250):
    try:
        _, info = nk.ecg_peaks(ecg, sampling_rate=fs)
        return info["ECG_R_Peaks"]
    except:
        return []



# BPM
def calculate_bpm(rpeaks, fs=250):
    if len(rpeaks) < 2:
        return 0
    rr = np.diff(rpeaks) / fs
    return 60 / np.mean(rr)



# HRV FEATURES

def extract_hrv(rpeaks, fs=250):
    if len(rpeaks) < 5:
        return None

    try:
        hrv = nk.hrv_time(rpeaks, sampling_rate=fs)
        hrv_freq = nk.hrv_frequency(rpeaks, sampling_rate=fs)

        lf = hrv_freq["HRV_LF"].values[0]
        hf = hrv_freq["HRV_HF"].values[0]
        total = lf + hf if (lf + hf) != 0 else 1

        return {
            "Gender": 1,
            "Mean HR (bpm)": 60000 / hrv["HRV_MeanNN"].values[0],
            "AVNN (ms)": hrv["HRV_MeanNN"].values[0],
            "SDNN (ms)": hrv["HRV_SDNN"].values[0],
            "RMSSD (ms)": hrv["HRV_RMSSD"].values[0],
            "pNN50 (%)": hrv["HRV_pNN50"].values[0],
            "LF (ms2)": lf,
            "HF (ms2)": hf,
            "LF/HF Ratio": hrv_freq["HRV_LFHF"].values[0],
            "LF Norm (n.u.)": (lf / total) * 100,
            "HF Norm (n.u.)": (hf / total) * 100
        }

    except:
        return None



# SIGNAL QUALITY CHECK

def check_signal_quality(ecg):
    if np.max(ecg) > 4000 or np.min(ecg) < 10:
        return False
    if np.std(ecg) < 20:
        return False
    return True



# STRESS PREDICTION

def predict_stress(features, rpeaks):

    bpm = calculate_bpm(rpeaks)
    print(f"BPM: {bpm:.1f}")

    if features is None:
        return "Bad Signal"

    try:
        df = pd.DataFrame([features])
        df = df.reindex(columns=scaler.feature_names_in_, fill_value=0)
        df = df.fillna(0)

        scaled = scaler.transform(df)
        pred = model.predict(scaled)[0]

        if pred == 1 and bpm > 90:
            return "Stress detected"
        elif pred == 1:
            return "Mild stress"
        else:
            return "Relaxed"

    except:
        return "Prediction Error"



# ARRHYTHMIA

def detect_arrhythmia(rpeaks, fs=250):

    if len(rpeaks) < 5:
        return "Not enough data"

    rr = np.diff(rpeaks) / fs
    rr_ms = rr * 1000
    bpm = 60 / np.mean(rr)

    print(f"\nArrhythmia BPM: {bpm:.1f}")
    print("RR variability (ms):", np.std(rr_ms))

    if bpm > 110:
        return "Tachycardia (High HR)"
    elif bpm < 50:
        return "Bradycardia (Low HR)"
    elif np.std(rr_ms) > 80:
        return "Possible Arrhythmia"
    else:
        return "Normal Rhythm"



# MAIN

ecg = read_ecg()

# RAW
plt.plot(ecg[:1000])
plt.title("Raw ECG")
plt.show()

# QUALITY CHECK
if not check_signal_quality(ecg):
    print("Bad signal detected.")
    exit()

# PROCESS
filtered = bandpass(ecg)
filtered = notch_filter(filtered)
filtered = filtered - np.mean(filtered)

# RPEAKS BEFORE SMOOTHING
rpeaks = get_rpeaks(filtered)

# SMOOTH FOR DISPLAY ONLY
display_signal = normalize(filtered)
display_signal = savgol_filter(display_signal, 9, 2)
display_signal = display_signal[250:]

# PLOT FILTERED
plt.plot(display_signal[:800])
plt.title("Filtered ECG")
plt.show()

print("Detected peaks:", len(rpeaks))

# FEATURES
features = extract_hrv(rpeaks)

# RESULTS
prediction = predict_stress(features, rpeaks)
arrhythmia = detect_arrhythmia(rpeaks)

print("\n========== RESULTS ==========")
print("Stress:", prediction)
print("Arrhythmia:", arrhythmia)
print("============================")