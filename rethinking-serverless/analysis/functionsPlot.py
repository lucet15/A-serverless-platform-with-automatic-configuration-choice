import pandas as pd
import matplotlib.pyplot as plt

data_ocr = pd.read_csv('./data/metrics/openfaas-ocr/openfaas-ocr_tesseract_512Mi_1000m_t3.large_BASIC.csv')
data_face_detector = pd.read_csv('./data/metrics/pigo-face-detector_BASIC/pigo-face-detector_faces2_512Mi_1000m_t3.large_BASIC.csv')

cost_ocr=20
cost_face_detector=15

plt.figure(figsize=(10,6))
plt.bar(cost_ocr, data_ocr['Response-delay'].mean())
plt.bar(cost_face_detector, data_face_detector['Response-delay'].mean())

plt.text(cost_ocr, data_ocr['Response-delay'].mean(), "OCR", ha='center', va='bottom')
plt.text(cost_face_detector, data_face_detector['Response-delay'].mean(), "Face Detector", ha='center', va='bottom')

plt.xlabel('Cost')
plt.ylabel('Performance')
plt.title('Cost Performance Bar Plot')
plt.show()

plt.savefig("BASIC.png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)
    