# 🛡️ CyberSentinel AI - Memory Forensics Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**An AI-powered memory forensics analyzer with a stunning cyberpunk dashboard for detecting malware in memory dumps.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Models](#-models) • [Screenshots](#-screenshots)

</div>

---

## 📋 Overview

CyberSentinel AI is a cutting-edge memory forensics tool that leverages Machine Learning and Deep Learning to analyze memory dumps and detect malicious activity. It provides:

- **99.99% Detection Accuracy** using ensemble learning
- **Real-time Threat Classification** (Benign, Ransomware, Spyware, Trojan)
- **Zero-Day Detection** via Isolation Forest anomaly detection
- **Interactive 3D Visualizations** for memory clustering analysis
- **Cyberpunk-Themed Dashboard** with glitch effects and neon aesthetics

---

## ✨ Features

### 🔍 Threat Detection
- **Binary Classification**: Instantly classify samples as Benign or Malware
- **Multi-class Classification**: Identify specific malware families
- **Anomaly Detection**: Flag unusual patterns that may indicate zero-day threats
- **Confidence Scoring**: Get probabilistic assessments for each prediction

### 🧠 AI Models
- **Ensemble Super Learner**: Combines Random Forest, Logistic Regression, and MLP
- **Optimized MLP**: Neural network with hyperparameter tuning
- **Isolation Forest**: Unsupervised anomaly detection for novel threats

### 📊 Visualization
- **3D PCA Clustering**: Interactive 3D scatter plots of memory space
- **Feature Importance Analysis**: Understand what drives detections
- **Class Distribution Charts**: Visual overview of threat landscape

### 📄 Reporting
- **Comprehensive HTML Reports**: Downloadable forensic analysis reports
- **Scan History**: Track all previous analyses with filtering
- **CSV Export**: Export results for further analysis

### 🎨 Cyberpunk UI
- **Void Black Theme**: Deep dark background with hexagon grid overlay
- **Neon Colors**: Electric Cyan, Hot Pink, Acid Green accents
- **Glitch Animations**: Twitching headers, pulsing indicators
- **Terminal Aesthetics**: Command-line style elements

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cybersentinel-ai.git
cd cybersentinel-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit pandas numpy scikit-learn plotly joblib shap lime
```

3. **Run the application**
```bash
cd src
streamlit run app.py
```

4. **Open in browser**
Navigate to `http://localhost:8501`

---

## 📖 Usage

### 1. Dashboard
The main dashboard provides an overview of the dataset statistics, 3D memory clustering visualization, class distribution, and feature importance analysis.

### 2. Scan Dump
Upload a CSV file containing memory dump features for analysis:
1. Click "Upload CSV" and select your file
2. Preview the data in the table
3. Click "EXECUTE_SCAN" to run the analysis
4. View detailed results for each sample
5. Download the forensic report

### 3. Train Models
Train the AI models on your dataset:
- **Ensemble**: Combined classifier for best accuracy
- **Neural Network**: Deep learning model with optimization
- **Anomaly Detector**: For zero-day threat detection

### 4. History
View and export previous scan results with filtering options.

---

## 🏗️ Architecture

```
cybersentinel-ai/
├── malmem.csv                 # Training dataset (CIC-MalMem-2022)
├── test_sample.csv            # Sample test file
├── models/                    # Saved trained models
│   ├── ensemble.pkl
│   ├── mlp_multiclass.pkl
│   ├── mlp_optimized.pkl
│   ├── anomaly_detector.pkl
│   └── RandomForest.pkl
├── src/
│   ├── app.py                 # Main Streamlit dashboard
│   ├── data_preprocessing.py  # Data loading and preprocessing
│   ├── base_models.py         # Baseline model training
│   ├── advanced_models.py     # Ensemble, MLP, Anomaly training
│   ├── search_algo.py         # Feature selection (RFE)
│   └── report_generator.py    # HTML report generation
├── Project_Report.md          # Detailed project documentation
├── SRS.md                     # Software Requirements Specification
└── README.md                  # This file
```

---

## 🤖 Models

### Performance Metrics

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | 99.88% | 99.9% | 99.8% | 99.8% |
| Decision Tree | 99.98% | 100% | 99.9% | 99.9% |
| Random Forest | 99.99% | 100% | 100% | 100% |
| Optimized MLP | 99.99% | 100% | 100% | 100% |
| **Ensemble Voting** | **99.99%** | **100%** | **100%** | **100%** |

### Model Descriptions

- **Ensemble Super Learner**: Soft voting classifier combining RF, LR, and MLP for robust predictions
- **MLP Classifier**: 3-layer neural network optimized via RandomizedSearchCV
- **Isolation Forest**: Unsupervised learning for detecting anomalous memory patterns

---

## 📊 Dataset

**Source**: CIC-MalMem-2022 (Obfuscated Memory Dataset)

| Attribute | Value |
|-----------|-------|
| Total Samples | 58,596 |
| Features | 55 (Volatility-extracted) |
| Classes | Benign (50%), Malware (50%) |
| Malware Families | Ransomware, Spyware, Trojan |

### Key Features
- `pslist.*`: Process listing metrics
- `dlllist.*`: DLL loading characteristics
- `handles.*`: Handle count and types
- `ldrmodules.*`: Hidden module indicators
- `malfind.*`: Code injection indicators
- `svcscan.*`: Service information

---

## 🖼️ Screenshots

### Dashboard
The main threat intelligence dashboard with 3D memory clustering, metrics, and feature analysis.

### Scan Results
Detailed analysis results with confidence scores, malware family identification, and anomaly detection.

### Report Generation
Downloadable HTML forensic reports with executive summaries and recommendations.

---

## 🛠️ Configuration

### Dataset Path
By default, the application looks for `malmem.csv` in the parent directory. You can specify a custom path in the sidebar.

### Model Training
Train models from the "Train Models" tab. Models are saved to the `models/` directory and persist between sessions.

---

## 📝 API Reference

### DataPreprocessor
```python
from data_preprocessing import DataPreprocessor

dp = DataPreprocessor("malmem.csv")
df = dp.load_data()
df = dp.clean_and_encode()
X_train, X_test, y_train, y_test, y_mal_train, y_mal_test = dp.split_data()
```

### AdvancedModelTrainer
```python
from advanced_models import AdvancedModelTrainer

trainer = AdvancedModelTrainer(X_train, y_train, X_test, y_test, y_mal_train, y_mal_test)
trainer.train_ensemble_model()
trainer.train_malware_type_model()
trainer.train_anomaly_detector()
trainer.save_models()
```

### ForensicsReportGenerator
```python
from report_generator import ForensicsReportGenerator

generator = ForensicsReportGenerator()
html_content, report_id = generator.generate_report(scan_results)
download_link = generator.get_download_link(html_content, "report.html")
```

---

## 🔮 Future Enhancements

- [ ] Live memory acquisition via C++ bindings
- [ ] Docker containerization for deployment
- [ ] LLM-powered natural language report summaries
- [ ] YARA rule integration
- [ ] API endpoints for external integration
- [ ] Real-time memory monitoring daemon

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CIC-MalMem-2022** dataset by the Canadian Institute for Cybersecurity
- **Volatility Framework** for memory forensics feature extraction
- **Streamlit** for the amazing dashboard framework
- **Scikit-Learn** for machine learning capabilities

---

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.

---

<div align="center">

**Built with 💚 for Cybersecurity Professionals**

</div>
