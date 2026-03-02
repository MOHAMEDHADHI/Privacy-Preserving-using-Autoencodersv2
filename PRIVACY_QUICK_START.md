# Privacy Evaluation - Quick Start

## 🚀 3-Step Privacy Evaluation

### Step 1: Run Privacy Attacks
```bash
# Evaluate privacy for dataset 12
curl -X POST http://localhost:8000/evaluate_privacy/12
```

### Step 2: View Results
```bash
# Get attack history
curl http://localhost:8000/privacy_attacks/12

# Get tradeoff analysis
curl http://localhost:8000/privacy_tradeoff
```

### Step 3: Generate Visualizations
```bash
python backend/visualize_privacy.py
```

---

## 📊 Understanding Results

### Privacy Score
- **0.7-1.0**: ✅ High Privacy (Good)
- **0.4-0.7**: ⚠ Medium Privacy (Adjust)
- **0.0-0.4**: ❌ Low Privacy (Increase sigma)

### Attack Success Rate
- **Lower is better** for privacy
- Reconstruction: 0 = Cannot reconstruct
- Membership: 0.5 = Random guess

---

## 🔍 Example Output

```json
{
  "overall_privacy_score": 0.3097,
  "privacy_level": "Low",
  "recommendation": "Privacy at risk - increase sigma significantly",
  
  "reconstruction_attack": {
    "privacy_score": 0.0195,
    "success_rate": 0.9805
  },
  
  "membership_inference_attack": {
    "privacy_score": 0.6000,
    "success_rate": 0.7000
  }
}
```

**Interpretation**: Privacy is low. Attacker can reconstruct data well and identify training members. Increase sigma from 1.0 to 1.5-2.0.

---

## 📈 Visualizations

Generated in `privacy_visualizations/`:

1. **privacy_utility_tradeoff.png** - Scatter plot
2. **sigma_effects.png** - Line plots
3. **attack_comparison.png** - Bar chart
4. **privacy_dashboard.png** - Complete dashboard

---

## 🎯 Quick Test

```bash
# 1. Start server (if not running)
python backend/main.py

# 2. Run test script
python backend/test_privacy_attacks.py

# 3. Generate graphs
python backend/visualize_privacy.py

# 4. View results
# Check privacy_visualizations/ folder
```

---

## 💡 Tips

### Improve Privacy
- Increase sigma value
- Reduce latent dimension
- Add more noise

### Improve Utility
- Decrease sigma value
- Increase latent dimension
- Better encoder training

### Find Balance
- Test multiple sigma values (0.5, 1.0, 1.5, 2.0)
- Plot privacy-utility curve
- Choose acceptable tradeoff point

---

## 📚 Full Documentation

- **Complete Guide**: `PRIVACY_EVALUATION_GUIDE.md`
- **Implementation**: `PRIVACY_IMPLEMENTATION_SUMMARY.md`
- **API Docs**: `API_DOCUMENTATION.md`

---

**Quick Reference**: This file
**Status**: ✅ Ready to use
