# 🛡️ Insurance Fraud Detection System

An end-to-end Machine Learning project that detects potentially fraudulent insurance claims using data preprocessing, feature engineering, rule-based validation, and predictive modeling.

## 📌 Project Overview

Insurance fraud leads to significant financial losses for insurance companies every year. This project uses Machine Learning techniques to identify suspicious claims and classify them as fraudulent or legitimate.

The solution includes:

- Data preprocessing and feature engineering
- Fraud detection model training
- Rule-based fraud validation engine
- Prediction service for new claims
- Flask-based application interface
- Automated testing

---

## 🚀 Features

✅ Data cleaning and preprocessing
✅ Feature engineering pipeline
✅ Machine Learning fraud prediction model
✅ Rule-based fraud detection engine
✅ REST/API prediction service
✅ Model persistence and loading
✅ Unit testing support
✅ Deployable Flask application

---

## 📂 Project Structure

```
43
insurance-fraud-detection/
│
├── app.py # Main application entry point
├── train_model.py # Model training script
├── feature_engineering.py # Feature creation and transformation
├── prediction_service.py # Prediction logic
├── rule_engine.py # Business rule validation
├── requirements.txt # Dependencies
│
├── data/ # Dataset files
├── models/ # Trained model files
├── notebooks/ # Jupyter notebooks
├── tests/ # Unit tests
│
└── README.md
```

---

## 🛠️ Tech Stack

- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- Flask
- Joblib
- PyTest
- Jupyter Notebook

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/insurance-fraud-detection.git

cd insurance-fraud-detection

```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/Mac

```bash

source .venv/bin/activate

```

### Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 📊 Train the Model

Run the training script to build and save the fraud detection model:
```bash
python train_model.py
```

Trained models will be stored inside the `models/` directory.

---

## 🔮 Run Predictions

Use the prediction module:

```bash
python prediction_service.py
```

Example output:

```json
{
"prediction": "Fraudulent",
"confidence_score": 0.94
}
```
---
## 🌐 Run Application

Start the Flask application:

```bash
python app.py
```

Application will be available at:

```
http://localhost:5000
```
---
## 🧪 Run Tests

Execute unit tests using pytest:

```bash
pytest tests/
```
---

## 📈 Machine Learning Workflow

1. Load Insurance Claims Data
2. Data Cleaning
3. Feature Engineering
4. Train/Test Split
5. Model Training
6. Fraud Prediction
7. Rule-Based Verification
8. Final Fraud Classification
---
## 🎯 Fraud Detection Rules
The Rule Engine helps identify suspicious claims using business logic such as:
- Unusually high claim amounts
- Multiple claims submitted in a short period
- Inconsistent customer information
- High-risk claim patterns

These rules work alongside the Machine Learning model to improve fraud detection accuracy.
---

## 📋 Future Enhancements
- Real-time fraud monitoring dashboard
- Explainable AI (SHAP/LIME)
- Docker deployment
- CI/CD pipeline
- Cloud deployment (Azure/AWS)
- Advanced anomaly detection

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request
---

---
## 👩‍💻 Author

**Shruti Balgude**
Software Engineer
Interested in Machine Learning, Data Analytics, and AI Solutions.
---
⭐ If you find this project useful, please give it a star on GitHub.
