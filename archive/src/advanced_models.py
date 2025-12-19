from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
import shap
import lime
import lime.lime_tabular
import numpy as np
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

class AdvancedModelTrainer:
    def __init__(self, X_train, y_train, X_test, y_test, y_mal_train=None, y_mal_test=None):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.y_mal_train = y_mal_train
        self.y_mal_test = y_mal_test
        
        self.best_model = None
        self.malware_model = None
        self.ensemble_model = None
        self.anomaly_model = None
        
    def build_and_optimize_mlp(self):
        """Builds an MLP and optimizes hyperparameters for Binary Classification."""
        print("Initializing MLP (Binary) and starting optimization...")
        mlp = MLPClassifier(random_state=42, max_iter=500)
        
        param_dist = {
            'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
            'activation': ['tanh', 'relu'],
            'solver': ['adam'],
            'alpha': [0.0001, 0.001, 0.01],
            'learning_rate': ['constant', 'adaptive']
        }
        
        random_search = RandomizedSearchCV(mlp, param_distributions=param_dist, n_iter=5, cv=3, random_state=42, n_jobs=-1, verbose=1)
        random_search.fit(self.X_train, self.y_train)
        
        self.best_model = random_search.best_estimator_
        print(f"Best Parameters (Binary): {random_search.best_params_}")
        
        if self.X_test is not None and self.y_test is not None:
            y_pred = self.best_model.predict(self.X_test)
            acc = accuracy_score(self.y_test, y_pred)
            print(f"Optimized MLP Accuracy (Binary): {acc:.4f}")
        return self.best_model

    def train_malware_type_model(self):
        """Trains a multiclass classifier for Malware Type."""
        if self.y_mal_train is None:
            print("No malware type labels provided.")
            return None
            
        print("Training Malware Type Classifier (Multiclass)...")
        # Using a standard MLP for multiclass
        self.malware_model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        self.malware_model.fit(self.X_train, self.y_mal_train)
        
        y_pred = self.malware_model.predict(self.X_test)
        acc = accuracy_score(self.y_mal_test, y_pred)
        print(f"Malware Type Model Accuracy: {acc:.4f}")
        return self.malware_model

    def train_ensemble_model(self):
        """Trains a Voting Ensemble (RF + MLP + LogReg)."""
        print("Training Ensemble Super Learner...")
        clf1 = LogisticRegression(random_state=1, max_iter=1000)
        clf2 = RandomForestClassifier(n_estimators=50, random_state=1)
        clf3 = MLPClassifier(hidden_layer_sizes=(50,50), max_iter=500, random_state=1)
        
        self.ensemble_model = VotingClassifier(estimators=[
            ('lr', clf1), ('rf', clf2), ('mlp', clf3)], voting='soft')
        
        self.ensemble_model.fit(self.X_train, self.y_train)
        if self.X_test is not None and self.y_test is not None:
            y_pred = self.ensemble_model.predict(self.X_test)
            acc = accuracy_score(self.y_test, y_pred)
            print(f"Ensemble Model Accuracy: {acc:.4f}")
        else:
            print("Ensemble Model Trained (No test set provided).")
        return self.ensemble_model

    def train_anomaly_detector(self):
        """Trains an Isolation Forest for Anomaly Detection (Unsupervised)."""
        print("Training Anomaly Detector (Isolation Forest)...")
        # Contamination can be estimated by the ratio of malware, or set low for strictly 'outliers'
        # Since we have balanced data, 'outlier' is tricky. 
        # But for 'Anomaly' in forensics, we might train ONLY on Benign data to detect Malware as anomalies, 
        # OR train on all to find weird styles. 
        # Let's train on EVERYTHING and let it score 'weirdness'.
        self.anomaly_model = IsolationForest(random_state=42, contamination=0.1)
        self.anomaly_model.fit(self.X_train)
        print("Anomaly Detector Trained.")
        return self.anomaly_model

    def explain_with_shap(self, sample_idx=0):
        if not self.best_model:
            return None, None
        
        background = shap.kmeans(self.X_train, 10) 
        explainer = shap.KernelExplainer(self.best_model.predict_proba, background)
        
        sample_data = self.X_test.iloc[sample_idx]
        shap_values = explainer.shap_values(sample_data)
        return explainer, shap_values

    def explain_with_lime(self, sample_idx=0):
        if not self.best_model:
            return None
        explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=np.array(self.X_train),
            feature_names=self.X_train.columns.tolist(),
            class_names=['Benign', 'Malware'],
            mode='classification'
        )
        exp = explainer.explain_instance(
            data_row=self.X_test.iloc[sample_idx], 
            predict_fn=self.best_model.predict_proba
        )
        return exp

    def save_models(self):
        if not os.path.exists('models'):
            os.makedirs('models')
        
        # Save models if they exist
        if self.best_model: joblib.dump(self.best_model, 'models/mlp_optimized.pkl')
        if self.malware_model: joblib.dump(self.malware_model, 'models/mlp_multiclass.pkl')
        if self.ensemble_model: joblib.dump(self.ensemble_model, 'models/ensemble.pkl')
        if self.anomaly_model: joblib.dump(self.anomaly_model, 'models/anomaly_detector.pkl')
        
        print("Models saved.")

if __name__ == "__main__":
    from data_preprocessing import DataPreprocessor
    dp = DataPreprocessor('malmem.csv')
    X_train, X_test, y_train, y_test, y_mal_train, y_mal_test = dp.split_data()
    
    adv_trainer = AdvancedModelTrainer(X_train, y_train, X_test, y_test, y_mal_train, y_mal_test)
    adv_trainer.build_and_optimize_mlp()
    adv_trainer.train_malware_type_model()
    adv_trainer.train_ensemble_model()
    adv_trainer.train_anomaly_detector()
    adv_trainer.save_models()
