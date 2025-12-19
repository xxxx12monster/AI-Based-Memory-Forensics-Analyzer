from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import joblib
import os

class BaseModelTrainer:
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.models = {
            'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
            'DecisionTree': DecisionTreeClassifier(random_state=42),
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        self.results = {}
        self.trained_models = {}

    def train_models(self):
        """Trains all base models and evaluates them."""
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(self.X_train, self.y_train)
            self.trained_models[name] = model
            
            y_pred = model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            report = classification_report(self.y_test, y_pred, output_dict=True)
            
            print(f"{name} Accuracy: {accuracy:.4f}")
            self.results[name] = {
                'accuracy': accuracy,
                'report': report,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred).tolist()
            }
        
    def save_models(self, save_dir='models'):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        for name, model in self.trained_models.items():
            path = os.path.join(save_dir, f"{name}.pkl")
            joblib.dump(model, path)
            print(f"Saved {name} to {path}")

    def get_results(self):
        return self.results

if __name__ == "__main__":
    from data_preprocessing import DataPreprocessor
    dp = DataPreprocessor('malmem.csv')
    X_train, X_test, y_train, y_test, _, _ = dp.split_data()
    
    trainer = BaseModelTrainer(X_train, y_train, X_test, y_test)
    trainer.train_models()
    trainer.save_models()
