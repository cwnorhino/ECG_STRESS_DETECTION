import socket
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
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



# FILTER
def bandpass(signal, fs=250):
    if len(signal) < fs:
        return signal

    b, a = butter(3, [0.5/(fs/2), 40/(fs/2)], btype='band')
    return filtfilt(b, a, signal)


#NORMALIZE
def normalize(ecg):
    ecg = ecg - np.mean(ecg)
    std = np.std(ecg)

    if std == 0:
        print("Flat signal")
        return ecg

    return ecg / std


# PEAK DETECTION

def get_rpeaks(ecg, fs=250):
    try:
        _, info = nk.ecg_peaks(ecg, sampling_rate=fs)
        return info["ECG_R_Peaks"]
    except:
        return []



# HRV FEATURE EXTRACTION

def extract_hrv(rpeaks, fs=250):
    if len(rpeaks) < 5:
        return None

    try:
        hrv = nk.hrv_time(rpeaks, sampling_rate=fs)
        hrv_freq = nk.hrv_frequency(rpeaks, sampling_rate=fs)

        mean_hr = 60000 / hrv["HRV_MeanNN"].values[0]
        nn50 = (hrv["HRV_pNN50"].values[0] / 100) * len(rpeaks)

        lf = hrv_freq["HRV_LF"].values[0]
        hf = hrv_freq["HRV_HF"].values[0]
        total = lf + hf if (lf + hf) != 0 else 1

        return {
            "Gender": 1,
            "Mean HR (bpm)": mean_hr,
            "AVNN (ms)": hrv["HRV_MeanNN"].values[0],
            "SDNN (ms)": hrv["HRV_SDNN"].values[0],
            "NN50 (beats)": nn50,
            "pNN50 (%)": hrv["HRV_pNN50"].values[0],
            "RMSSD (ms)": hrv["HRV_RMSSD"].values[0],
            "LF (ms2)": lf,
            "LF Norm (n.u.)": (lf / total) * 100,
            "HF (ms2)": hf,
            "HF Norm (n.u.)": (hf / total) * 100,
            "LF/HF Ratio": hrv_freq["HRV_LFHF"].values[0]
        }

    except:
        return None



# PREDICTION 

def predict_stress(features, rpeaks):

    bpm = max((len(rpeaks) / 10) * 60, 60)
    print(f"BPM: {bpm:.1f}")

    # HARD SAFETY (prevents wrong ML output)
    if bpm < 85:
        return "Relaxed"

    # BAD SIGNAL
    if features is None:
        return "Stress detected" if bpm > 100 else "Mild stress"

    try:
        df = pd.DataFrame([features])

        expected_cols = scaler.feature_names_in_
        df = df.reindex(columns=expected_cols, fill_value=0)

        # FIX NaN
        df = df.fillna(0)

        print("\nFeatures:\n", df)

        scaled = scaler.transform(df)
        pred = model.predict(scaled)[0]

        # FINAL DECISION LOGIC
        if bpm > 105:
            return "Stress detected"
        elif pred == 1:
            return "Mild stress"
        else:
            return "Relaxed"

    except Exception as e:
        print("ML failed → fallback:", e)

        if bpm > 100:
            return "Stress detected"
        elif bpm > 85:
            return "Mild stress"
        else:
            return "Relaxed"



# MAIN

ecg = read_ecg(duration=10)

# RAW
plt.plot(ecg[:1000])
plt.title("Raw ECG")
plt.show()

# PROCESS
ecg = normalize(ecg)
filtered = bandpass(ecg)

# remove drift
filtered = filtered - np.mean(filtered)

# FILTERED
plt.plot(filtered[:1000])
plt.title("Filtered ECG")
plt.show()

# PEAKS
rpeaks = get_rpeaks(filtered)
print("Detected peaks:", len(rpeaks))

# FEATURES
features = extract_hrv(rpeaks)

# PREDICTION
prediction = predict_stress(features, rpeaks)

print("\nResult:", prediction)