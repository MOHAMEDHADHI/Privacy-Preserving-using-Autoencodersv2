# Privacy Visualizations Guide

## 📊 Overview

Privacy visualizations are **already implemented** in two ways:
1. **Interactive Dashboard** (Web-based, real-time)
2. **Static Images** (Python-generated, high-resolution)

---

## 🌐 Option 1: Interactive Dashboard

### Location
```
http://localhost:3000/privacy-evaluation
```

### Features

#### 1. Privacy-Utility Scatter Plot
- **X-axis**: Utility (Model Accuracy)
- **Y-axis**: Privacy Score
- **Color**: Sigma value
- **Interactive**: Hover for details
- **Real-time**: Updates with new data

#### 2. Privacy Score Cards
```
┌─────────────────────────┐
│ Overall Privacy Score   │
│      31.0%              │
│   [Low Privacy]         │
└─────────────────────────┘
```

#### 3. Attack Results Display
```
Reconstruction Attack:
├─ Privacy Score: 1.95%
├─ MSE: 1.028
├─ MAE: 0.811
└─ Success Rate: 98.05%

Membership Inference:
├─ Privacy Score: 60.0%
├─ Accuracy: 70.0%
├─ AUC: 0.56
└─ Baseline: 50%
```

#### 4. Attack History Table
- Sortable columns
- Progress bars
- Color-coded privacy levels
- Timestamps

### How to Use

**Step 1: Login**
```
http://localhost:3000/login
Email: test@example.com
Password: password123
```

**Step 2: Navigate**
```
Click: "Privacy Evaluation" in sidebar
```

**Step 3: Select Dataset**
```
Choose dataset from dropdown
```

**Step 4: Run Evaluation**
```
Click: "Run Privacy Evaluation"
Wait: ~5-10 seconds
```

**Step 5: View Results**
```
✅ Interactive scatter plot
✅ Privacy score cards
✅ Attack comparison
✅ History table
```

---

## 📈 Option 2: Static Visualizations

### Generate Images

```bash
python backend/visualize_privacy.py
```

### Generated Files

#### 1. `privacy_utility_tradeoff.png`
**Description**: Scatter plot showing privacy vs utility
- Each point = one dataset
- Color = sigma value
- Shows ideal operating region
- High-resolution (300 DPI)

**Interpretation**:
- Top-right: Best (high privacy + high utility)
- Top-left: High privacy, low utility
- Bottom-right: Low privacy, high utility
- Bottom-left: Worst (low privacy + low utility)

#### 2. `sigma_effects.png`
**Description**: Two line plots showing sigma's impact
- Left: Sigma vs Utility
- Right: Sigma vs Privacy

**Interpretation**:
- Shows how increasing sigma affects both metrics
- Helps identify optimal sigma value
- Visualizes privacy-utility tradeoff

#### 3. `attack_comparison.png`
**Description**: Bar chart comparing attack types
- Reconstruction privacy (blue bars)
- Membership inference privacy (red bars)
- Per-dataset breakdown

**Interpretation**:
- Which attack is more successful?
- Which datasets are more vulnerable?
- Where to improve privacy?

#### 4. `privacy_dashboard.png`
**Description**: Comprehensive 4-panel dashboard
- Panel 1: Privacy-utility scatter
- Panel 2: Sigma effects
- Panel 3: Attack comparison
- Panel 4: Summary statistics

**Interpretation**:
- Complete overview in one image
- Ready for presentations
- All metrics visible

---

## 📊 Visualization Details

### Privacy-Utility Scatter Plot

```python
# What it shows
X-axis: Model Accuracy (0-100%)
Y-axis: Privacy Score (0-100%)
Color: Sigma value (0-3)
Size: Fixed
Shape: Circle

# Interpretation
- Each point = one experiment
- Higher right = better
- Color gradient = privacy level
```

### Sigma Effects Charts

```python
# Left Chart: Utility
X-axis: Sigma value
Y-axis: Model Accuracy
Trend: Usually decreasing

# Right Chart: Privacy
X-axis: Sigma value
Y-axis: Privacy Score
Trend: Usually increasing
```

### Attack Comparison

```python
# Bar Chart
X-axis: Dataset ID
Y-axis: Privacy Score
Bars: Two per dataset
  - Blue: Reconstruction
  - Red: Membership Inference
```

---

## 🎨 Customization

### Change Colors

Edit `backend/visualize_privacy.py`:

```python
# Line 45-50
scatter = plt.scatter(
    utilities, privacies, 
    c=sigmas, 
    cmap='viridis',  # Change to 'plasma', 'coolwarm', etc.
    s=100
)
```

### Change Resolution

```python
# Line 120
plt.savefig(output_path, dpi=300)  # Change to 150, 600, etc.
```

### Add More Charts

```python
# Add your own visualization function
def plot_my_custom_chart(data):
    plt.figure(figsize=(10, 6))
    # Your plotting code
    plt.savefig('my_chart.png', dpi=300)
```

---

## 📁 File Locations

### Dashboard Visualizations
```
Frontend: http://localhost:3000/privacy-evaluation
Code: frontend/src/pages/PrivacyEvaluationPage.js
Charts: Recharts library (React)
```

### Static Visualizations
```
Script: backend/visualize_privacy.py
Output: privacy_visualizations/
Format: PNG (300 DPI)
Library: Matplotlib
```

---

## 🔄 Workflow

### Complete Visualization Workflow

```
1. Upload Data
   ↓
2. Train Models
   ↓
3. Run Privacy Evaluation
   POST /evaluate_privacy/{dataset_id}
   ↓
4. View in Dashboard
   http://localhost:3000/privacy-evaluation
   ↓
5. Generate Static Images
   python backend/visualize_privacy.py
   ↓
6. Use in Reports/Presentations
   privacy_visualizations/*.png
```

---

## 📊 Available Metrics

### Displayed in Visualizations

**Privacy Scores**:
- Overall privacy score (0-100%)
- Reconstruction privacy (0-100%)
- Membership inference privacy (0-100%)

**Attack Metrics**:
- Reconstruction MSE, MAE
- Membership accuracy, AUC
- Success rates

**Model Metrics**:
- Accuracy, Precision, Recall, F1
- MLP vs CNN comparison

**Privacy-Utility**:
- Tradeoff curves
- Sigma effects
- Optimal operating points

---

## 🎯 Use Cases

### 1. Research Papers
```
Use: privacy_dashboard.png
Why: Comprehensive overview
Format: High-resolution PNG
```

### 2. Presentations
```
Use: privacy_utility_tradeoff.png
Why: Clear, simple message
Format: 300 DPI for projectors
```

### 3. Reports
```
Use: All 4 images
Why: Complete analysis
Format: Include in PDF/Word
```

### 4. Real-time Monitoring
```
Use: Dashboard
Why: Live updates
Access: http://localhost:3000/privacy-evaluation
```

---

## 🔍 Interpretation Guide

### Privacy Score Scale

| Score | Level | Color | Meaning |
|-------|-------|-------|---------|
| 70-100% | High | Green | Good protection |
| 40-70% | Medium | Yellow | Moderate risk |
| 0-40% | Low | Red | Privacy at risk |

### Attack Success Rate

| Rate | Meaning | Action |
|------|---------|--------|
| <30% | Good | Maintain |
| 30-70% | Moderate | Consider increasing sigma |
| >70% | Poor | Increase sigma significantly |

### Privacy-Utility Tradeoff

| Position | Interpretation |
|----------|----------------|
| Top-right | Ideal: High privacy + High utility |
| Top-left | High privacy, sacrifice utility |
| Bottom-right | High utility, sacrifice privacy |
| Bottom-left | Poor: Low privacy + Low utility |

---

## 🚀 Quick Commands

### Generate All Visualizations
```bash
python backend/visualize_privacy.py
```

### View in Dashboard
```bash
# Open browser
http://localhost:3000/privacy-evaluation
```

### Check Generated Files
```bash
# Windows
dir privacy_visualizations

# Linux/Mac
ls privacy_visualizations/
```

### Open Visualization
```bash
# Windows
start privacy_visualizations/privacy_dashboard.png

# Linux
xdg-open privacy_visualizations/privacy_dashboard.png

# Mac
open privacy_visualizations/privacy_dashboard.png
```

---

## 📚 Additional Resources

### Documentation
- **Privacy Evaluation Guide**: `PRIVACY_EVALUATION_GUIDE.md`
- **Implementation Summary**: `PRIVACY_IMPLEMENTATION_SUMMARY.md`
- **Quick Start**: `PRIVACY_QUICK_START.md`

### Code
- **Visualization Script**: `backend/visualize_privacy.py`
- **Dashboard Page**: `frontend/src/pages/PrivacyEvaluationPage.js`
- **Privacy Attacks**: `backend/privacy_attacks.py`

---

## ✅ Summary

### Interactive Visualizations (Dashboard)
✅ Real-time updates
✅ Interactive charts
✅ Hover tooltips
✅ Color-coded metrics
✅ Sortable tables

### Static Visualizations (Python)
✅ High-resolution PNG
✅ 4 comprehensive charts
✅ Publication-ready
✅ Customizable
✅ Batch generation

### Both Options Available
✅ Use dashboard for exploration
✅ Use static images for reports
✅ Complementary approaches
✅ Same underlying data

---

**Privacy visualizations are fully implemented and ready to use!** 📊
