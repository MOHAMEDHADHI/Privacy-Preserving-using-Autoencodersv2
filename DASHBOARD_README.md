# Professional SaaS Dashboard - User Guide

## 🎨 Overview

A modern, responsive web dashboard for the Privacy-Preserving ML Platform with real-time analytics, interactive visualizations, and comprehensive privacy evaluation tools.

## ✨ Features

### 1. Main Dashboard
- **Real-time Statistics**
  - Total datasets uploaded
  - Models trained (MLP & CNN)
  - Average accuracy across all models
  - Privacy score monitoring
  
- **Privacy-Utility Tradeoff Visualization**
  - Interactive scatter plot
  - Shows relationship between privacy and utility
  - Color-coded by sigma values

- **Recent Results Table**
  - Latest training results
  - Sortable and filterable
  - Quick access to detailed metrics

- **Quick Actions**
  - One-click navigation to key features
  - Upload, train, evaluate, analyze

### 2. Upload Page
- **Drag & Drop File Upload**
  - Support for .npy files
  - Visual feedback
  - File validation

- **Privacy Settings**
  - Interactive sigma slider (0-3)
  - Real-time recommendations
  - Visual privacy level indicator

- **Model Selection**
  - Choose MLP, CNN, or both
  - Visual model cards
  - Performance descriptions

- **Training Progress**
  - Real-time status updates
  - Automatic redirection to results

### 3. Results Analytics
- **Comprehensive Filters**
  - Filter by dataset
  - Filter by model type
  - Dynamic result updates

- **MLP vs CNN Comparison**
  - Side-by-side bar charts
  - Accuracy comparison
  - Per-dataset breakdown

- **Performance Metrics**
  - Radar chart visualization
  - Accuracy, Precision, Recall, F1
  - Interactive tooltips

- **Detailed Results Table**
  - All metrics displayed
  - Progress bars for visual feedback
  - Sortable columns

### 4. Privacy Evaluation
- **Dataset Selection**
  - Choose dataset for evaluation
  - One-click privacy attack execution

- **Privacy Assessment**
  - Overall privacy score
  - Reconstruction attack results
  - Membership inference results
  - Actionable recommendations

- **Attack Details**
  - MSE, MAE, normalized error
  - Attack accuracy and AUC
  - Comparison with baseline

- **Privacy-Utility Tradeoff**
  - Interactive scatter plot
  - Identify optimal operating points
  - Visual interpretation guide

- **Attack History**
  - Complete attack log
  - Success rates over time
  - Privacy score trends

## 🚀 Getting Started

### Prerequisites

```bash
# Backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend
npm install
```

### Installation

1. **Install Additional Frontend Dependencies**
```bash
cd frontend
npm install recharts lucide-react
```

2. **Start Backend Server**
```bash
# From project root
python backend/main.py
```

3. **Start Frontend Development Server**
```bash
# From frontend directory
cd frontend
npm start
```

4. **Access Dashboard**
```
Open browser to: http://localhost:3000
```

## 📊 Dashboard Pages

### Main Dashboard (`/`)
- Overview of all system metrics
- Quick access to all features
- Real-time data updates

### Upload Page (`/upload`)
- Upload latent vectors
- Configure privacy settings
- Select models for training

### Results Page (`/results`)
- View all training results
- Compare MLP vs CNN
- Filter and analyze data

### Privacy Evaluation (`/privacy-evaluation`)
- Run privacy attacks
- View attack results
- Analyze privacy-utility tradeoff

## 🎨 UI Components

### Stats Cards
- Display key metrics
- Color-coded icons
- Trend indicators

### Charts
- **Scatter Plot**: Privacy-utility tradeoff
- **Bar Chart**: MLP vs CNN comparison
- **Radar Chart**: Multi-metric comparison
- **Line Chart**: Trends over time

### Tables
- Sortable columns
- Filterable data
- Progress bars
- Badge indicators

### Forms
- File upload with drag & drop
- Range sliders
- Select dropdowns
- Validation feedback

## 🔧 Configuration

### API Endpoint
Update in each page file:
```javascript
const API_BASE = 'http://localhost:8000';
```

### CORS Settings
Backend automatically configured for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 📱 Responsive Design

- **Desktop**: Full sidebar navigation
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu (planned)

## 🎯 Key Features

### Real-time Updates
- Automatic data refresh
- Live training progress
- Instant result display

### Interactive Visualizations
- Hover tooltips
- Click interactions
- Zoom and pan (where applicable)

### Modern UI/UX
- Clean, professional design
- Intuitive navigation
- Consistent color scheme
- Smooth animations

### Performance
- Optimized rendering
- Lazy loading
- Efficient data fetching

## 📈 Data Flow

```
User Action
    ↓
Frontend (React)
    ↓
API Request (Axios)
    ↓
Backend (FastAPI)
    ↓
Database (PostgreSQL)
    ↓
Response (JSON)
    ↓
Frontend Update
    ↓
UI Refresh
```

## 🎨 Color Scheme

```css
Primary: #6366f1 (Indigo)
Success: #10b981 (Green)
Warning: #f59e0b (Amber)
Danger: #ef4444 (Red)
Info: #3b82f6 (Blue)
```

## 📊 Chart Types

### Scatter Plot
- **Use**: Privacy-utility tradeoff
- **X-axis**: Utility (accuracy)
- **Y-axis**: Privacy score
- **Color**: Sigma value

### Bar Chart
- **Use**: MLP vs CNN comparison
- **X-axis**: Dataset
- **Y-axis**: Accuracy
- **Bars**: MLP (blue), CNN (green)

### Radar Chart
- **Use**: Multi-metric comparison
- **Axes**: Accuracy, Precision, Recall, F1
- **Series**: MLP, CNN

## 🔍 Privacy Evaluation Workflow

1. **Select Dataset**
   - Choose from uploaded datasets
   - View dataset metadata

2. **Run Evaluation**
   - Click "Run Privacy Evaluation"
   - Wait for attacks to complete (~5-10 seconds)

3. **View Results**
   - Overall privacy score
   - Attack-specific metrics
   - Recommendations

4. **Analyze Tradeoff**
   - View scatter plot
   - Identify optimal sigma
   - Compare with other datasets

5. **Review History**
   - Check past evaluations
   - Track privacy trends
   - Monitor improvements

## 🛠️ Troubleshooting

### Frontend Won't Start
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### API Connection Error
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API_BASE URL in frontend

### Charts Not Displaying
```bash
# Reinstall chart library
npm install recharts --save
```

### Styling Issues
- Clear browser cache
- Check Dashboard.css is imported
- Verify CSS file path

## 📚 Component Structure

```
frontend/src/
├── pages/
│   ├── MainDashboard.js      # Main dashboard
│   ├── UploadPage.js          # Upload interface
│   ├── ResultsPage.js         # Results analytics
│   └── PrivacyEvaluationPage.js # Privacy evaluation
├── styles/
│   └── Dashboard.css          # Global styles
├── App.js                     # Route configuration
└── index.js                   # Entry point
```

## 🎯 Best Practices

### Performance
- Use React.memo for expensive components
- Implement pagination for large datasets
- Lazy load charts

### UX
- Provide loading indicators
- Show error messages clearly
- Offer helpful tooltips

### Accessibility
- Use semantic HTML
- Provide alt text for icons
- Ensure keyboard navigation

## 🚀 Future Enhancements

### Planned Features
- [ ] Real-time WebSocket updates
- [ ] Export results to PDF/CSV
- [ ] Custom dashboard layouts
- [ ] Dark mode toggle
- [ ] Mobile app version
- [ ] Advanced filtering
- [ ] Saved views/bookmarks
- [ ] Collaborative features

### UI Improvements
- [ ] Animated transitions
- [ ] More chart types
- [ ] Custom themes
- [ ] Accessibility improvements

## 📞 Support

For issues or questions:
1. Check this README
2. Review API documentation
3. Check browser console for errors
4. Verify backend logs

## 🎉 Success Metrics

Dashboard provides:
- ✅ Modern, professional UI
- ✅ Real-time analytics
- ✅ Interactive visualizations
- ✅ Comprehensive privacy evaluation
- ✅ Responsive design
- ✅ Intuitive navigation
- ✅ Fast performance

---

**Status**: ✅ Production Ready
**Version**: 1.0
**Last Updated**: February 28, 2026
