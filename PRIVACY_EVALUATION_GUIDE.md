# Privacy Evaluation Framework Guide

## Overview

The Privacy Evaluation Framework implements quantitative privacy validation through adversarial attacks, measuring the privacy-utility tradeoff in privacy-preserving machine learning systems.

## Attack Types

### 1. Reconstruction Attack

**Goal**: Attempt to reconstruct original data from latent vectors

**Method**:
- Train a neural network attacker (3-layer MLP)
- Input: Latent vectors
- Output: Reconstructed original data
- Measure reconstruction error (MSE, MAE)

**Metrics**:
- **MSE (Mean Squared Error)**: Average squared difference
- **MAE (Mean Absolute Error)**: Average absolute difference
- **Normalized Error**: Error scaled to data range (0-1)
- **Privacy Score**: 1 - normalized_error (higher is better)
- **Success Rate**: 1 - privacy_score (lower is better)

**Interpretation**:
- High reconstruction error = Good privacy
- Low reconstruction error = Privacy at risk
- Privacy Score > 0.7 = Strong protection
- Privacy Score < 0.4 = Weak protection

### 2. Membership Inference Attack

**Goal**: Predict if a sample was in the training set

**Method**:
- Train a binary classifier
- Input: Latent vectors
- Output: Member (1) or Non-member (0)
- Measure classification accuracy

**Metrics**:
- **Accuracy**: Percentage of correct predictions
- **AUC**: Area under ROC curve
- **Privacy Score**: 1 - |accuracy - 0.5| * 2 (higher is better)
- **Success Rate**: Accuracy (lower is better)
- **Baseline**: 0.5 (random guess)

**Interpretation**:
- Accuracy close to 0.5 = Good privacy (random guess)
- Accuracy close to 1.0 = Privacy at risk
- Privacy Score > 0.7 = Strong protection
- Privacy Score < 0.4 = Weak protection

## API Endpoints

### POST /evaluate_privacy/{dataset_id}

Run both privacy attacks on a dataset.

**Request**:
```bash
POST http://localhost:8000/evaluate_privacy/12
```

**Response**:
```json
{
  "status": "success",
  "dataset_id": 12,
  "sigma": 1.0,
  "reconstruction_attack": {
    "attack_type": "reconstruction",
    "mse": 1.028,
    "mae": 0.811,
    "normalized_error": 0.019,
    "privacy_score": 0.0195,
    "success_rate": 0.9805
  },
  "membership_inference_attack": {
    "attack_type": "membership_inference",
    "accuracy": 0.70,
    "auc": 0.56,
    "privacy_score": 0.60,
    "success_rate": 0.70
  },
  "overall_privacy_score": 0.3097,
  "interpretation": {
    "privacy_level": "Low",
    "recommendation": "Privacy at risk - increase sigma significantly"
  }
}
```

### GET /privacy_attacks/{dataset_id}

Retrieve all privacy attack results for a dataset.

**Response**:
```json
{
  "dataset_id": 12,
  "total_attacks": 2,
  "attacks": [
    {
      "id": 1,
      "attack_type": "reconstruction",
      "success_rate": 0.9805,
      "details": {...},
      "created_at": "2026-02-28T20:26:57"
    }
  ]
}
```

### GET /privacy_tradeoff

Get privacy-utility tradeoff data across all datasets.

**Response**:
```json
{
  "total_datasets": 4,
  "tradeoff_data": [
    {
      "dataset_id": 9,
      "dataset_name": "test.npy",
      "sigma": 1.0,
      "utility": 0.375,
      "privacy_score": 0.3097,
      "reconstruction_privacy": 0.0195,
      "membership_privacy": 0.60
    }
  ],
  "summary": {
    "avg_utility": 0.8438,
    "avg_privacy": 0.3097
  }
}
```

## Privacy Score Interpretation

### Overall Privacy Score Scale

| Score Range | Privacy Level | Interpretation | Action |
|-------------|---------------|----------------|--------|
| 0.7 - 1.0 | High | ✅ Good protection | Maintain current sigma |
| 0.4 - 0.7 | Medium | ⚠ Moderate risk | Consider increasing sigma |
| 0.0 - 0.4 | Low | ❌ Privacy at risk | Increase sigma significantly |

### Attack Success Rate

**Lower is better for privacy**

- **Reconstruction**: Success rate close to 0 means attacker cannot reconstruct data
- **Membership Inference**: Success rate close to 0.5 means attacker is guessing randomly

## Privacy-Utility Tradeoff

### The Fundamental Tradeoff

```
High Privacy (High Sigma)     ←→     High Utility (Low Sigma)
- Better privacy protection          - Better model accuracy
- Lower model accuracy               - Weaker privacy protection
- Higher reconstruction error        - Lower reconstruction error
- Random membership inference        - Accurate membership inference
```

### Finding the Balance

**Optimal Range**: Sigma between 0.5 and 2.0

- **Sigma < 0.5**: High utility, low privacy
- **Sigma 0.5-1.0**: Balanced (recommended starting point)
- **Sigma 1.0-2.0**: Good privacy, acceptable utility
- **Sigma > 2.0**: Strong privacy, degraded utility

## Visualization

### Generate Privacy Graphs

```bash
python backend/visualize_privacy.py
```

**Generated Visualizations**:

1. **privacy_utility_tradeoff.png**
   - Scatter plot of utility vs privacy
   - Color-coded by sigma value
   - Shows ideal operating region

2. **sigma_effects.png**
   - Line plots showing sigma's effect
   - Left: Sigma vs Utility
   - Right: Sigma vs Privacy

3. **attack_comparison.png**
   - Bar chart comparing attack types
   - Reconstruction vs Membership Inference
   - Per-dataset comparison

4. **privacy_dashboard.png**
   - Comprehensive 4-panel dashboard
   - All metrics in one view
   - Summary statistics

## Usage Examples

### Example 1: Evaluate Single Dataset

```python
import requests

# Run privacy attacks
response = requests.post("http://localhost:8000/evaluate_privacy/12")
result = response.json()

print(f"Privacy Score: {result['overall_privacy_score']:.3f}")
print(f"Privacy Level: {result['interpretation']['privacy_level']}")
print(f"Recommendation: {result['interpretation']['recommendation']}")
```

### Example 2: Compare Multiple Sigma Values

```python
import numpy as np
import requests

# Upload datasets with different sigma values
for sigma in [0.5, 1.0, 1.5, 2.0]:
    # Create and upload latent vectors
    data = create_latent_vectors(sigma=sigma)
    
    # Upload
    response = requests.post(
        "http://localhost:8000/upload_latent",
        files={"file": data},
        data={"sigma": sigma}
    )
    dataset_id = response.json()["dataset_id"]
    
    # Evaluate privacy
    privacy_response = requests.post(
        f"http://localhost:8000/evaluate_privacy/{dataset_id}"
    )
    
    print(f"Sigma {sigma}: Privacy {privacy_response.json()['overall_privacy_score']:.3f}")
```

### Example 3: Generate Tradeoff Analysis

```python
import requests

# Get tradeoff data
response = requests.get("http://localhost:8000/privacy_tradeoff")
data = response.json()

# Analyze
for item in data['tradeoff_data']:
    print(f"Sigma: {item['sigma']:.1f}")
    print(f"  Utility: {item['utility']:.3f}")
    print(f"  Privacy: {item['privacy_score']:.3f}")
    print(f"  Balance: {'✅ Good' if item['utility'] > 0.7 and item['privacy_score'] > 0.5 else '⚠ Adjust'}")
```

## Testing

### Run Privacy Attack Tests

```bash
# Test privacy evaluation
python backend/test_privacy_attacks.py

# Generate visualizations
python backend/visualize_privacy.py
```

### Expected Output

```
======================================================================
PRIVACY ATTACK EVALUATION TEST
======================================================================

✅ Privacy evaluation successful!

RECONSTRUCTION ATTACK RESULTS
MSE: 1.028071
Privacy Score: 0.0195 (higher is better)

MEMBERSHIP INFERENCE ATTACK RESULTS
Accuracy: 0.7000
Privacy Score: 0.6000 (higher is better)

OVERALL PRIVACY ASSESSMENT
Overall Privacy Score: 0.3097
Privacy Level: Low
Recommendation: Privacy at risk - increase sigma significantly
```

## Best Practices

### 1. Start with Baseline

- Begin with sigma = 1.0
- Evaluate privacy and utility
- Adjust based on requirements

### 2. Iterative Tuning

- Test multiple sigma values
- Plot privacy-utility curve
- Find acceptable balance point

### 3. Regular Evaluation

- Run privacy attacks periodically
- Monitor for privacy degradation
- Update sigma if needed

### 4. Consider Use Case

- **High-stakes applications**: Prioritize privacy (sigma > 1.5)
- **Research applications**: Balance both (sigma 0.8-1.2)
- **Low-risk applications**: Prioritize utility (sigma < 0.8)

## Technical Details

### Reconstruction Attacker Architecture

```
Input: (batch, latent_dim)
├─ Linear(latent_dim → 128) + ReLU + Dropout(0.3)
├─ Linear(128 → 256) + ReLU + Dropout(0.3)
└─ Linear(256 → output_dim)

Training: 30 epochs, Adam optimizer
```

### Membership Inference Attacker Architecture

```
Input: (batch, latent_dim)
├─ Linear(latent_dim → 64) + ReLU + Dropout(0.2)
├─ Linear(64 → 32) + ReLU + Dropout(0.2)
└─ Linear(32 → 2)  # Binary classification

Training: 20 epochs, Adam optimizer
```

## Database Storage

### privacy_attack_results Table

```sql
CREATE TABLE privacy_attack_results (
    id SERIAL PRIMARY KEY,
    model_result_id INTEGER REFERENCES model_results(id),
    attack_type VARCHAR(50),  -- 'reconstruction' or 'membership_inference'
    success_rate FLOAT,
    details TEXT,  -- JSON with full metrics
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Troubleshooting

### Low Privacy Scores

**Problem**: Privacy score < 0.4

**Solutions**:
1. Increase sigma value
2. Reduce latent dimension
3. Add more noise layers
4. Use stronger privacy mechanisms

### Low Utility Scores

**Problem**: Model accuracy < 0.6

**Solutions**:
1. Decrease sigma value
2. Increase latent dimension
3. Improve encoder training
4. Use better architecture

### Attack Failures

**Problem**: Attacks fail to run

**Solutions**:
1. Check data format
2. Ensure sufficient samples
3. Verify latent vectors exist
4. Check server logs

## References

### Privacy Metrics

- **Differential Privacy**: Formal privacy guarantee
- **Reconstruction Error**: Empirical privacy measure
- **Membership Inference**: Practical privacy attack

### Related Work

- Shokri et al. (2017): Membership Inference Attacks
- Fredrikson et al. (2015): Model Inversion Attacks
- Dwork & Roth (2014): Differential Privacy Theory

---

**Status**: ✅ Fully Implemented
**Version**: 1.0
**Last Updated**: February 28, 2026
