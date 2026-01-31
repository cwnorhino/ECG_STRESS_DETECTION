import joblib

model = joblib.load("svm_model_2dataset.pkl")
scaler = joblib.load("scaler.pkl")
new_sample = [[
    1, 85.8474, 698.9147, 45.8957, 46, 10.7477, 29.6913,
    412.1663, 46.8523, 467.3008, 53.1197, 0.882
]]
new_sample_scaled = scaler.transform(new_sample)
prediction = model.predict(new_sample_scaled)
print(prediction)

