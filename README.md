# 🛡️ Insurance Fraud Detection System
2
 
3
An end-to-end Machine Learning project that detects potentially fraudulent insurance claims using data preprocessing, feature engineering, rule-based validation, and predictive modeling.
4
 
5
## 📌 Project Overview
6
 
7
Insurance fraud leads to significant financial losses for insurance companies every year. This project uses Machine Learning techniques to identify suspicious claims and classify them as fraudulent or legitimate.
8
 
9
The solution includes:
10
 
11
- Data preprocessing and feature engineering
12
- Fraud detection model training
13
- Rule-based fraud validation engine
14
- Prediction service for new claims
15
- Flask-based application interface
16
- Automated testing
17
 
18
---
19
 
20
## 🚀 Features
21
 
22
✅ Data cleaning and preprocessing
23
 
24
✅ Feature engineering pipeline
25
 
26
✅ Machine Learning fraud prediction model
27
 
28
✅ Rule-based fraud detection engine
29
 
30
✅ REST/API prediction service
31
 
32
✅ Model persistence and loading
33
 
34
✅ Unit testing support
35
 
36
✅ Deployable Flask application
37
 
38
---
39
 
40
## 📂 Project Structure
41
 
42
```
43
insurance-fraud-detection/
44
│
45
├── app.py # Main application entry point
46
├── train_model.py # Model training script
47
├── feature_engineering.py # Feature creation and transformation
48
├── prediction_service.py # Prediction logic
49
├── rule_engine.py # Business rule validation
50
├── requirements.txt # Dependencies
51
│
52
├── data/ # Dataset files
53
├── models/ # Trained model files
54
├── notebooks/ # Jupyter notebooks
55
├── tests/ # Unit tests
56
│
57
└── README.md
58
```
59
 
60
---
61
 
62
## 🛠️ Tech Stack
63
 
64
- Python 3.x
65
- Pandas
66
- NumPy
67
- Scikit-learn
68
- Flask
69
- Joblib
70
- PyTest
71
- Jupyter Notebook
72
 
73
---
74
 
75
## ⚙️ Installation
76
 
77
### Clone the repository
78
 
79
```bash
80
git clone https://github.com/yourusername/insurance-fraud-detection.git
81
 
82
cd insurance-fraud-detection
83
```
84
 
85
### Create Virtual Environment
86
 
87
```bash
88
python -m venv .venv
89
```
90
 
91
### Activate Virtual Environment
92
 
93
#### Windows
94
 
95
```bash
96
.venv\Scripts\activate
97
```
98
 
99
#### Linux/Mac
100
 
101
```bash
102
source .venv/bin/activate
103
```
104
 
105
### Install Dependencies
106
 
107
```bash
108
pip install -r requirements.txt
109
```
110
 
111
---
112
 
113
## 📊 Train the Model
114
 
115
Run the training script to build and save the fraud detection model:
116
 
117
```bash
118
python train_model.py
119
```
120
 
121
Trained models will be stored inside the `models/` directory.
122
 
123
---
124
 
125
## 🔮 Run Predictions
126
 
127
Use the prediction module:
128
 
129
```bash
130
python prediction_service.py
131
```
132
 
133
Example output:
134
 
135
```json
136
{
137
"prediction": "Fraudulent",
138
"confidence_score": 0.94
139
}
140
```
141
 
142
---
143
 
144
## 🌐 Run Application
145
 
146
Start the Flask application:
147
 
148
```bash
149
python app.py
150
```
151
 
152
Application will be available at:
153
 
154
```
155
http://localhost:5000
156
```
157
 
158
---
159
 
160
## 🧪 Run Tests
161
 
162
Execute unit tests using pytest:
163
 
164
```bash
165
pytest tests/
166
```
167
 
168
---
169
 
170
## 📈 Machine Learning Workflow
171
 
172
1. Load Insurance Claims Data
173
2. Data Cleaning
174
3. Feature Engineering
175
4. Train/Test Split
176
5. Model Training
177
6. Fraud Prediction
178
7. Rule-Based Verification
179
8. Final Fraud Classification
180
 
181
---
182
 
183
## 🎯 Fraud Detection Rules
184
 
185
The Rule Engine helps identify suspicious claims using business logic such as:
186
 
187
- Unusually high claim amounts
188
- Multiple claims submitted in a short period
189
- Inconsistent customer information
190
- High-risk claim patterns
191
 
192
These rules work alongside the Machine Learning model to improve fraud detection accuracy.
193
 
194
---
195
 
196
## 📋 Future Enhancements
197
 
198
- Real-time fraud monitoring dashboard
199
- Explainable AI (SHAP/LIME)
200
- Docker deployment
201
- CI/CD pipeline
202
- Cloud deployment (Azure/AWS)
203
- Advanced anomaly detection
204
 
205
---
206
 
207
## 🤝 Contributing
208
 
209
Contributions are welcome.
210
 
211
1. Fork the repository
212
2. Create a feature branch
213
3. Commit your changes
214
4. Push to your branch
215
5. Open a Pull Request
216
 
217
---
218
 

 
223
---
224
 
225
## 👩‍💻 Author
226
 
227
**Shruti Balgude**
228
 
229
Software Engineer
230
 
231
Interested in Machine Learning, Data Analytics, and AI Solutions.
232
 
233
---
234
⭐ If you find this project useful, please give it a star on GitHub.
