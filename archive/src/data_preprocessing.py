import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.target = 'Class'
        self.malware_type_col = 'MalwareType'
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_mal_train = None
        self.y_mal_test = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.malware_encoder = LabelEncoder()

    def load_data(self):
        """Loads dataset from csv file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        self.df = pd.read_csv(self.file_path)
        print(f"Data loaded. Shape: {self.df.shape}")
        return self.df

    def clean_and_encode(self):
        """Cleans data, encodes categorical columns and extracts MalwareType."""
        if self.df is None:
            self.load_data()
            
        # Extract Malware Type from Category
        # Example: Ransomware-Ako-... -> Ransomware
        if 'Category' in self.df.columns:
            self.df[self.malware_type_col] = self.df['Category'].apply(lambda x: x.split('-')[0] if '-' in str(x) else x)
            print(f"Extracted MalwareType. Unique values: {self.df[self.malware_type_col].unique()}")
            
            # Encode MalwareType
            self.df[self.malware_type_col] = self.malware_encoder.fit_transform(self.df[self.malware_type_col])
            print(f"MalwareType encoded. Classes: {self.malware_encoder.classes_}")
            
            # Drop original Category column
            self.df = self.df.drop(columns=['Category'])

        # Encode Target (Binary)
        if self.target in self.df.columns:
            self.df[self.target] = self.label_encoder.fit_transform(self.df[self.target])
            # print(f"Target '{self.target}' encoded. Classes: {self.label_encoder.classes_}")
            
        return self.df

    def split_data(self, test_size=0.2, random_state=42):
        """Splits data into train and test sets for both binary and multiclass tasks."""
        if self.df is None:
            self.clean_and_encode()
            
        # Features
        X = self.df.drop(columns=[self.target, self.malware_type_col])
        
        # Targets
        y_binary = self.df[self.target]
        y_malware = self.df[self.malware_type_col]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns)
        
        # Split (stratified by binary class for now to ensure good benign/malware split)
        self.X_train, self.X_test, self.y_train, self.y_test, self.y_mal_train, self.y_mal_test = train_test_split(
            X, y_binary, y_malware, test_size=test_size, random_state=random_state, stratify=y_binary
        )
        
        print(f"Data split. Train shape: {self.X_train.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test, self.y_mal_train, self.y_mal_test

    def get_malware_classes(self):
        return self.malware_encoder.classes_

if __name__ == "__main__":
    # Test
    dp = DataPreprocessor('malmem.csv')
    dp.load_data()
    dp.clean_and_encode()
    dp.split_data()
