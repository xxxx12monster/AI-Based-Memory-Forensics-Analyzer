import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

class FeatureSelector:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.selected_features = None

    def select_features_rfe(self, n_features_to_select=10):
        """Selects features using Recursive Feature Elimination with Random Forest."""
        print(f"Starting RFE to assign importance rankings...")
        estimator = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
        selector = RFE(estimator, n_features_to_select=n_features_to_select, step=1)
        selector = selector.fit(self.X, self.y)
        
        self.selected_features = self.X.columns[selector.support_]
        print(f"RFE selected {n_features_to_select} features: {list(self.selected_features)}")
        return self.selected_features

    def get_selected_features(self):
        return self.selected_features

class DataSearcher:
    def __init__(self, df):
        self.df = df

    def search_by_query(self, query_string):
        """Filters dataframe using a pandas query string."""
        try:
            return self.df.query(query_string)
        except Exception as e:
            print(f"Search error: {e}")
            return pd.DataFrame() # Return empty on error
    
    def search_by_criteria(self, criteria_dict):
        """Criteria dict: {'column': (min, max)} or {'column': 'exact_value'}"""
        temp_df = self.df.copy()
        for col, criteria in criteria_dict.items():
            if col not in temp_df.columns:
                continue
                
            if isinstance(criteria, tuple) and len(criteria) == 2:
                # Range search
                temp_df = temp_df[(temp_df[col] >= criteria[0]) & (temp_df[col] <= criteria[1])]
            else:
                # Exact match
                temp_df = temp_df[temp_df[col] == criteria]
        return temp_df

if __name__ == "__main__":
    # Test
    from data_preprocessing import DataPreprocessor
    dp = DataPreprocessor('malmem.csv')
    X_train, X_test, y_train, y_test, _, _ = dp.split_data()
    
    fs = FeatureSelector(X_train, y_train)
    fs.select_features_rfe(n_features_to_select=5)
    
    # Test DataSearcher (using raw df)
    raw_df = dp.df
    searcher = DataSearcher(raw_df)
    results = searcher.search_by_query("`pslist.nproc` > 50")
    print(f"Query returned {len(results)} rows.")
