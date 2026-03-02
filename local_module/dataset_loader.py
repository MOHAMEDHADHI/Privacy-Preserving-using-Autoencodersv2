import pandas as pd
import os
from pathlib import Path
from PIL import Image

class DatasetLoader:
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
    
    def load_csv(self, file_path):
        """Load CSV file"""
        df = pd.read_csv(file_path)
        return self._preprocess(df)
    
    def load_excel(self, file_path):
        """Load Excel file"""
        df = pd.read_excel(file_path)
        return self._preprocess(df)
    
    def load_images(self, folder_path):
        """Load images from folder"""
        images = []
        folder = Path(folder_path)
        for img_path in folder.glob('*'):
            if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                img = Image.open(img_path)
                images.append({'path': str(img_path), 'size': img.size})
        return images
    
    def load_dataset(self, path):
        """Auto-detect and load dataset"""
        path = Path(path)
        
        if path.is_dir():
            return self.load_images(path)
        
        ext = path.suffix.lower()
        if ext == '.csv':
            return self.load_csv(path)
        elif ext in ['.xlsx', '.xls']:
            return self.load_excel(path)
        else:
            raise ValueError(f"Unsupported format: {ext}")
    
    def _preprocess(self, df):
        """Basic preprocessing"""
        df = df.dropna()
        df = df.drop_duplicates()
        return df

if __name__ == "__main__":
    loader = DatasetLoader()
    print("Dataset Loader initialized successfully")
