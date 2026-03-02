# How to Encode Your Own CSV/Excel Data

## 🎯 Quick Start

### Method 1: Interactive Script (Recommended)

```bash
python local_module/encode_my_data.py
```

Then follow the prompts:
1. Enter your file path
2. Select label column
3. Select feature columns
4. Configure encoder settings
5. Generate encoded files

### Method 2: With File Path

```bash
python local_module/encode_my_data.py path/to/your/data.csv
```

---

## 📋 Step-by-Step Guide

### Step 1: Prepare Your Data

Your CSV/Excel file should have:
- **Feature columns**: Data you want to use for prediction
- **Label column**: What you want to predict

**Example CSV:**
```csv
income,credit_score,debt,age,risk_label
75000,720,25000,35,Low Risk
85000,680,30000,42,High Risk
60000,750,15000,28,Low Risk
```

### Step 2: Run the Script

```bash
cd local_module
python encode_my_data.py
```

### Step 3: Answer the Prompts

**Prompt 1: File Path**
```
Enter path to your CSV/Excel file: ../my_data.csv
```

**Prompt 2: Label Column**
```
Enter label column name: risk_label
```

**Prompt 3: Feature Columns**
```
Enter choice (1 or 2): 1
# Option 1: Use all columns except label
# Option 2: Select specific columns
```

**Prompt 4: Encoder Settings**
```
Latent dimension (default: 32): [press Enter]
Training epochs (default: 30): [press Enter]
```

**Prompt 5: Privacy Settings**
```
Enter sigma values (comma-separated): 0.5,1.0,1.5
Output filename prefix: my_encoded_data
```

### Step 4: Get Your Files

The script will generate:
```
my_encoded_data_sigma_0.5.npy
my_encoded_data_sigma_1.0.npy
my_encoded_data_sigma_1.5.npy
```

---

## 📊 Supported File Formats

### CSV Files (.csv)
```python
python encode_my_data.py data.csv
```

### Excel Files (.xlsx, .xls)
```python
python encode_my_data.py data.xlsx
```

---

## 🎯 Example Use Cases

### Finance: Credit Risk
```csv
income,credit_score,debt,employment_years,risk
75000,720,25000,5,0
85000,680,30000,3,1
```

### Healthcare: Disease Diagnosis
```csv
age,temperature,blood_pressure,symptoms_count,diagnosis
45,100.1,140,3,COVID
32,98.6,120,1,Flu
```

### Marketing: Customer Churn
```csv
usage_hours,support_tickets,subscription_months,churned
120,2,12,0
45,8,3,1
```

---

## ⚙️ Configuration Options

### Latent Dimension
- **Small (16-32)**: Faster, less information
- **Medium (32-64)**: Balanced (recommended)
- **Large (64-128)**: Slower, more information

### Training Epochs
- **Quick (10-20)**: Fast, may underfit
- **Standard (30-50)**: Balanced (recommended)
- **Thorough (50-100)**: Slow, better quality

### Sigma Values
- **0.5**: Low privacy, high accuracy
- **1.0**: Balanced (recommended)
- **1.5-2.0**: High privacy, lower accuracy

---

## 🔍 What Happens During Encoding

### 1. Data Loading
```
✅ Load CSV/Excel file
✅ Display columns and preview
```

### 2. Feature Selection
```
✅ Select label column
✅ Select feature columns
✅ Handle non-numeric data (auto-encoding)
```

### 3. Data Preprocessing
```
✅ Convert categorical to numeric
✅ Normalize features (StandardScaler)
✅ Encode labels if needed
```

### 4. Encoder Training
```
✅ Initialize autoencoder
✅ Train for specified epochs
✅ Learn data patterns
```

### 5. Latent Generation
```
✅ Encode features to latent space
✅ Add differential privacy noise
✅ Combine with labels
```

### 6. File Export
```
✅ Save as .npy files
✅ Ready for cloud upload
```

---

## 🔒 Privacy Protection

### What's Protected
- ✅ Original feature values (income, age, etc.)
- ✅ Individual records
- ✅ Sensitive attributes
- ✅ Personal information

### What's Preserved
- ✅ Statistical patterns
- ✅ Class relationships
- ✅ Predictive power
- ✅ Label information

---

## 📤 After Encoding

### Upload to Dashboard

1. **Open**: `http://localhost:3000/upload`
2. **Login**: Any email/password
3. **Upload**: Your generated .npy file
4. **Train**: Select MLP/CNN models
5. **Evaluate**: View results and privacy scores

---

## 🐛 Troubleshooting

### Error: File not found
```
Solution: Use full path or relative path from local_module/
Example: python encode_my_data.py ../data/my_file.csv
```

### Error: Column not found
```
Solution: Check column names (case-sensitive)
Use: df.columns to see exact names
```

### Error: Non-numeric data
```
Solution: Script auto-handles this with one-hot encoding
Or: Pre-process your data to numeric values
```

### Error: Memory error
```
Solution: Reduce dataset size or latent dimension
Or: Process in batches
```

---

## 💡 Tips

### 1. Start Small
- Test with a small dataset first
- Verify the process works
- Then use your full dataset

### 2. Check Your Data
- Remove missing values
- Ensure label column is correct
- Verify feature columns make sense

### 3. Experiment with Sigma
- Generate multiple files with different sigma
- Upload and compare results
- Find optimal privacy-utility balance

### 4. Save Your Settings
- Note which columns you used
- Record sigma values tested
- Document your results

---

## 📚 Example Session

```bash
$ python encode_my_data.py

======================================================================
ENCODE YOUR OWN DATA - Interactive Script
======================================================================

📁 Step 1: Load Your Data
----------------------------------------------------------------------
Enter path to your CSV/Excel file: ../financial_data.csv
✅ Loaded 100 rows, 5 columns

Columns: ['income', 'credit_score', 'debt', 'age', 'risk']

======================================================================
📊 Step 2: Select Label Column
----------------------------------------------------------------------
Enter label column name: risk

======================================================================
🔧 Step 3: Select Feature Columns
----------------------------------------------------------------------
Enter choice (1 or 2): 1
✅ Selected 4 features: ['income', 'credit_score', 'debt', 'age']

======================================================================
🤖 Step 5: Configure Encoder
----------------------------------------------------------------------
Latent dimension (default: 32): 
Training epochs (default: 30): 

======================================================================
🎓 Step 6: Training Encoder
----------------------------------------------------------------------
Epoch 10/30 - Loss: 0.8234
Epoch 20/30 - Loss: 0.3456
Epoch 30/30 - Loss: 0.1789
✅ Encoder trained successfully!

======================================================================
🔒 Step 7: Generate Privacy-Protected Latent Vectors
----------------------------------------------------------------------
Enter sigma values: 1.0
Output filename prefix: my_financial_data

✅ ENCODING COMPLETE!

📁 Generated Files:
   • my_financial_data_sigma_1.0.npy

📤 Next Steps:
   1. Go to: http://localhost:3000/upload
   2. Upload: my_financial_data_sigma_1.0.npy
   3. Train and evaluate!
```

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Encode CSV | `python encode_my_data.py data.csv` |
| Encode Excel | `python encode_my_data.py data.xlsx` |
| Interactive | `python encode_my_data.py` |
| Help | Check this guide |

---

**Your data, your privacy, your control!** 🔒
