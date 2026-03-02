"""
Privacy-Utility Tradeoff Visualization
Generates graphs showing the relationship between privacy and utility
"""
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path("privacy_visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_tradeoff_data():
    """Fetch privacy-utility tradeoff data from API"""
    try:
        response = requests.get("http://localhost:8000/privacy_tradeoff")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def plot_privacy_utility_tradeoff(data):
    """
    Create privacy vs utility scatter plot
    """
    if not data or not data.get("tradeoff_data"):
        print("No data available for plotting")
        return
    
    tradeoff = data["tradeoff_data"]
    
    sigmas = [d["sigma"] for d in tradeoff]
    utilities = [d["utility"] for d in tradeoff]
    privacies = [d["privacy_score"] for d in tradeoff]
    
    plt.figure(figsize=(10, 6))
    
    # Scatter plot with sigma as color
    scatter = plt.scatter(utilities, privacies, c=sigmas, cmap='viridis', 
                         s=100, alpha=0.6, edgecolors='black')
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Sigma (Privacy Parameter)', rotation=270, labelpad=20)
    
    # Add labels for each point
    for i, d in enumerate(tradeoff):
        plt.annotate(f"σ={d['sigma']:.1f}", 
                    (utilities[i], privacies[i]),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center',
                    fontsize=8)
    
    plt.xlabel('Utility (Model Accuracy)', fontsize=12)
    plt.ylabel('Privacy Score', fontsize=12)
    plt.title('Privacy-Utility Tradeoff', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add ideal region
    plt.axhline(y=0.7, color='g', linestyle='--', alpha=0.3, label='High Privacy Threshold')
    plt.axvline(x=0.8, color='b', linestyle='--', alpha=0.3, label='High Utility Threshold')
    
    plt.legend()
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "privacy_utility_tradeoff.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def plot_sigma_effects(data):
    """
    Create line plots showing how sigma affects privacy and utility
    """
    if not data or not data.get("tradeoff_data"):
        return
    
    tradeoff = sorted(data["tradeoff_data"], key=lambda x: x["sigma"])
    
    sigmas = [d["sigma"] for d in tradeoff]
    utilities = [d["utility"] for d in tradeoff]
    privacies = [d["privacy_score"] for d in tradeoff]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Sigma vs Utility
    ax1.plot(sigmas, utilities, 'b-o', linewidth=2, markersize=8, label='Utility')
    ax1.set_xlabel('Sigma (Privacy Parameter)', fontsize=12)
    ax1.set_ylabel('Utility (Model Accuracy)', fontsize=12, color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_title('Effect of Sigma on Utility', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Sigma vs Privacy
    ax2.plot(sigmas, privacies, 'g-o', linewidth=2, markersize=8, label='Privacy')
    ax2.set_xlabel('Sigma (Privacy Parameter)', fontsize=12)
    ax2.set_ylabel('Privacy Score', fontsize=12, color='g')
    ax2.tick_params(axis='y', labelcolor='g')
    ax2.set_title('Effect of Sigma on Privacy', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "sigma_effects.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def plot_attack_comparison(data):
    """
    Compare reconstruction vs membership inference attack success
    """
    if not data or not data.get("tradeoff_data"):
        return
    
    tradeoff = data["tradeoff_data"]
    
    dataset_names = [f"D{d['dataset_id']}" for d in tradeoff]
    recon_privacy = [d["reconstruction_privacy"] for d in tradeoff]
    mi_privacy = [d["membership_privacy"] for d in tradeoff]
    
    x = np.arange(len(dataset_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars1 = ax.bar(x - width/2, recon_privacy, width, label='Reconstruction Privacy', 
                   color='skyblue', edgecolor='black')
    bars2 = ax.bar(x + width/2, mi_privacy, width, label='Membership Inference Privacy',
                   color='lightcoral', edgecolor='black')
    
    ax.set_xlabel('Dataset', fontsize=12)
    ax.set_ylabel('Privacy Score', fontsize=12)
    ax.set_title('Privacy Attack Comparison by Dataset', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(dataset_names)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "attack_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def plot_combined_dashboard(data):
    """
    Create a comprehensive dashboard with multiple subplots
    """
    if not data or not data.get("tradeoff_data"):
        return
    
    tradeoff = sorted(data["tradeoff_data"], key=lambda x: x["sigma"])
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Plot 1: Privacy-Utility Scatter
    ax1 = fig.add_subplot(gs[0, 0])
    sigmas = [d["sigma"] for d in tradeoff]
    utilities = [d["utility"] for d in tradeoff]
    privacies = [d["privacy_score"] for d in tradeoff]
    
    scatter = ax1.scatter(utilities, privacies, c=sigmas, cmap='viridis', 
                         s=150, alpha=0.6, edgecolors='black')
    ax1.set_xlabel('Utility (Accuracy)')
    ax1.set_ylabel('Privacy Score')
    ax1.set_title('Privacy-Utility Tradeoff')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Sigma')
    
    # Plot 2: Sigma Effects
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(sigmas, utilities, 'b-o', label='Utility', linewidth=2)
    ax2.plot(sigmas, privacies, 'g-o', label='Privacy', linewidth=2)
    ax2.set_xlabel('Sigma')
    ax2.set_ylabel('Score')
    ax2.set_title('Sigma Effects on Privacy & Utility')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Attack Types
    ax3 = fig.add_subplot(gs[1, 0])
    recon_privacy = [d["reconstruction_privacy"] for d in tradeoff]
    mi_privacy = [d["membership_privacy"] for d in tradeoff]
    x = np.arange(len(tradeoff))
    width = 0.35
    ax3.bar(x - width/2, recon_privacy, width, label='Reconstruction', color='skyblue')
    ax3.bar(x + width/2, mi_privacy, width, label='Membership Inference', color='lightcoral')
    ax3.set_xlabel('Dataset Index')
    ax3.set_ylabel('Privacy Score')
    ax3.set_title('Attack-Specific Privacy Scores')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Summary Statistics
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    summary_text = f"""
    PRIVACY EVALUATION SUMMARY
    ═══════════════════════════════
    
    Total Datasets: {len(tradeoff)}
    
    Average Utility: {data['summary']['avg_utility']:.3f}
    Average Privacy: {data['summary']['avg_privacy']:.3f}
    
    Sigma Range: {min(sigmas):.1f} - {max(sigmas):.1f}
    
    Best Privacy: {max(privacies):.3f}
    Best Utility: {max(utilities):.3f}
    
    Privacy-Utility Balance:
    {_get_balance_assessment(data['summary'])}
    """
    
    ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
            verticalalignment='center')
    
    fig.suptitle('Privacy Evaluation Dashboard', fontsize=16, fontweight='bold')
    
    output_path = OUTPUT_DIR / "privacy_dashboard.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def _get_balance_assessment(summary):
    """Assess the privacy-utility balance"""
    avg_util = summary['avg_utility']
    avg_priv = summary['avg_privacy']
    
    if avg_util > 0.8 and avg_priv > 0.7:
        return "✅ Excellent balance"
    elif avg_util > 0.7 and avg_priv > 0.5:
        return "✓ Good balance"
    elif avg_util > 0.6 or avg_priv > 0.4:
        return "⚠ Moderate - needs tuning"
    else:
        return "❌ Poor - adjust sigma"


def generate_all_visualizations():
    """Generate all privacy visualization graphs"""
    print("=" * 60)
    print("PRIVACY-UTILITY TRADEOFF VISUALIZATION")
    print("=" * 60)
    
    print("\n📊 Fetching data from API...")
    data = fetch_tradeoff_data()
    
    if not data:
        print("❌ No data available. Make sure:")
        print("   1. Server is running (python backend/main.py)")
        print("   2. Datasets have been uploaded")
        print("   3. Privacy attacks have been run")
        return
    
    print(f"✅ Fetched data for {data['total_datasets']} datasets")
    
    print("\n📈 Generating visualizations...")
    
    plot_privacy_utility_tradeoff(data)
    plot_sigma_effects(data)
    plot_attack_comparison(data)
    plot_combined_dashboard(data)
    
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE")
    print("=" * 60)
    print(f"\n📁 All graphs saved to: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    print("  1. privacy_utility_tradeoff.png")
    print("  2. sigma_effects.png")
    print("  3. attack_comparison.png")
    print("  4. privacy_dashboard.png")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_visualizations()
