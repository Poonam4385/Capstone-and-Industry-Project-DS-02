# 🚀 Nationwide Demand Forecasting & Inventory Optimization

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/ML-LightGBM-success)](https://lightgbm.readthedocs.io/)
[![PyTorch](https://img.shields.io/badge/Deep%20Learning-PyTorch-red?logo=pytorch)](https://pytorch.org/)
[![OR-Tools](https://img.shields.io/badge/Optimization-OR--Tools-orange)](https://developers.google.com/optimization)
[![Dash](https://img.shields.io/badge/Dashboard-Plotly%20Dash-purple)](https://dash.plotly.com/)

## 📌 Project Overview

End-to-end retail AI project using the Walmart M5 dataset to forecast demand, quantify uncertainty, reconcile hierarchical forecasts, and optimize inventory ordering decisions.

## 🌐 Live Dashboard

🚀 **Live dashboard link will be added after Render deployment.**

## 📊 Final Results

| Metric | Result |
|---|---:|
| Rolling-28 Validation WAPE | 46.11% |
| LightGBM Validation WAPE | **40.69%** |
| Rolling-28 Test WAPE | 44.43% |
| LightGBM Test WAPE | **39.27%** |
| LightGBM Test RMSSE | **0.8011** |
| Improvement vs Baseline | **11.63%** |
| TFT WAPE | **31.33%** |
| National Reconciled WAPE | **3.61%** |
| Items Optimized | **450** |
| Items Ordered | **364** |
| Recommended Units | **18,664** |
| Procurement Value | **$26,356.90** |
| High-Risk Items | **133** |

## 🏗️ Pipeline

```text
M5 Dataset
   ↓
EDA
   ↓
Feature Engineering
   ↓
Baseline / Prophet / LightGBM / TFT
   ↓
Prediction Intervals
   ↓
Hierarchical Reconciliation
   ↓
Safety Stock + Reorder Point
   ↓
OR-Tools Inventory Optimization
   ↓
Plotly Dash Dashboard
```

## 🧠 Models

- Naive and rolling baselines
- Prophet
- LightGBM
- Temporal Fusion Transformer

## 📈 Forecast Uncertainty

| Model | Nominal Coverage | Actual Coverage |
|---|---:|---:|
| LightGBM | 90% | 89.29% |
| TFT | 80% | 76.74% |
| TFT | 90% | 86.18% |
| Prophet | 90% | 88.69% |

## 🌎 Hierarchy

```text
Item
 ↓
Store
 ↓
State
 ↓
National
```

All hierarchy consistency tests passed.

## 📦 Inventory Optimization

Inventory recommendations are generated from forecast demand, lead-time demand, safety stock and reorder points using Google OR-Tools.

Important: the M5 dataset does not contain actual current inventory, procurement costs, supplier lead times or stockout penalties. These values are simulated for the prototype.

## 🖥️ Dashboard

The Plotly Dash application provides:

- store filtering
- KPI cards
- actual vs forecast demand
- 90% prediction intervals
- model performance comparison
- stockout-risk analysis
- recommended order quantities
- searchable and sortable inventory recommendations

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Data | Pandas, NumPy |
| EDA | Matplotlib, Seaborn |
| Statistical Forecasting | Prophet |
| Machine Learning | LightGBM |
| Deep Learning | PyTorch |
| Deep Forecasting | Temporal Fusion Transformer |
| Optimization | Google OR-Tools |
| Visualization | Plotly |
| Dashboard | Dash |
| Development | Google Colab |
| Version Control | GitHub |
| Deployment | Render |

## ▶️ Run Locally

```bash
git clone https://github.com/Poonam4385/Capstone-and-Industry-Project-DS-02.git
cd Capstone-and-Industry-Project-DS-02
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:8050
```

## ☁️ Render Deployment

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:server --bind 0.0.0.0:$PORT
```

## 🔐 Security

Never commit Kaggle tokens, GitHub tokens, kaggle.json, or .env files.

## 🔗 Repository

https://github.com/Poonam4385/Capstone-and-Industry-Project-DS-02

## 🔭 Future Improvements

- Train on full M5 hierarchy
- MinT reconciliation
- GPU TFT training
- Real ERP inventory integration
- Supplier lead-time uncertainty
- MOQ and case-pack constraints
- Warehouse capacity constraints
- Automated retraining
- Docker deployment

## ⭐ Project

If you find the project useful, consider giving the repository a star.