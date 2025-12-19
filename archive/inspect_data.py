import pandas as pd
import sys

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path = 'malmem.csv'
output_file = 'data_info.txt'

try:
    with open(output_file, 'w') as f:
        df = pd.read_csv(file_path)
        f.write("Dataset loaded successfully.\n")
        f.write("\nFirst 5 rows:\n")
        f.write(str(df.head()) + "\n")
        f.write("\nInfo:\n")
        # capture info output
        import io
        buffer = io.StringIO()
        df.info(buf=buffer)
        f.write(buffer.getvalue() + "\n")
        f.write("\nDescription:\n")
        f.write(str(df.describe()) + "\n")
        f.write("\nColumns:\n")
        f.write(str(df.columns.tolist()) + "\n")
        
        # Check for missing values
        f.write("\nMissing values:\n")
        f.write(str(df.isnull().sum().sum()) + "\n")
        
        if 'Class' in df.columns:
            f.write("\nClass distribution:\n")
            f.write(str(df['Class'].value_counts()) + "\n")

    print(f"Analysis written to {output_file}")

except Exception as e:
    print(f"Error loading dataset: {e}")
