import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import os
from google.colab import files

# 出力ファイルを保存するフォルダを作成
output_dir = "simulation_results"
os.makedirs(output_dir, exist_ok=True)

# --- Mathematical Model Definitions ---

def u_base(i, peak):
    """Base utility function: linearly decreases based on distance from the peak"""
    return 1.0 - 0.25 * np.abs(i - peak)

def softmax(utilities, beta):
    """Softmax function: converts utility to probability (beta is inverse temperature/certainty)"""
    exp_u = np.exp(beta * utilities)
    return exp_u / np.sum(exp_u)

def calculate_distribution(v2, beta):
    """Calculate overall survey response probability based on Sontaku strength (v2) and certainty (beta)"""
    options = np.array([1, 2, 3, 4, 5])
    
    # Utility calculation (U_true + U_sontaku)
    u_true1 = u_base(options, 1) # True peak for minority (10%) is 1
    u_true2 = u_base(options, 3) # True peak for majority (90%) is 3
    u_sontaku = u_base(options, 4) # Target peak for Sontaku is 4
    
    # Composite utility using AHP-like weighting
    U1 = (1 - v2) * u_true1 + v2 * u_sontaku
    U2 = (1 - v2) * u_true2 + v2 * u_sontaku
    
    # Probabilities via Softmax
    prob_g1 = softmax(U1, beta)
    prob_g2 = softmax(U2, beta)
    
    # Overall distribution (Minority 10%, Majority 90%)
    total_prob = 0.10 * prob_g1 + 0.90 * prob_g2
    return total_prob

# --- Graph 1: Phase Transition (Cliff of Signal Loss) ---

v2_range = np.linspace(0, 1, 100)
betas_to_test = [1.0, 3.0, 5.0, 7.0]

# CSV出力用のデータフレームを作成
df_graph1 = pd.DataFrame({'v2': v2_range})

plt.figure(figsize=(10, 6))
for b in betas_to_test:
    prob_1_list = [calculate_distribution(v, b)[0] for v in v2_range] # Index 0 is the probability of 'Rating 1'
    plt.plot(v2_range, prob_1_list, label=f'Certainty (Beta) = {b}', linewidth=2)
    df_graph1[f'Beta_{b}_Prob_Rating_1'] = prob_1_list # データを記録

plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Critical Point of Utility Inversion (v2=0.5)')
plt.title("Fig 1: Survival Curve of 'Rating 1 (Warning)' with Increasing Bias (v2)", fontsize=14)
plt.xlabel('Strength of Social Desirability Bias (v2)', fontsize=12)
plt.ylabel('Observation Probability of Rating 1', fontsize=12)
plt.xlim(0, 1)
plt.ylim(0, 0.12)
plt.legend()
plt.grid(True, alpha=0.3)

# グラフ1の画像保存 (dpi=300で論文クオリティに)
fig1_path = os.path.join(output_dir, 'fig1_survival_curve.png')
plt.savefig(fig1_path, bbox_inches='tight', dpi=300, facecolor='white')
plt.show()

# グラフ1のCSV保存
csv1_path = os.path.join(output_dir, 'data_fig1_survival_curve.csv')
df_graph1.to_csv(csv1_path, index=False)


# --- Graph 2: Structural Alteration in 5 Scenarios ---

fixed_beta = 5.0
scenarios = [
    (0.00, "Scenario 1: Zero Bias\n(Baseline)"),
    (0.25, "Scenario 2: Mild Bias\n(Perturbation)"),
    (0.50, "Scenario 3: Critical Point\n(Cliff Edge)"),
    (0.75, "Scenario 4: False\nConsensus"),
    (0.95, "Scenario 5: Totalitarian\nConvergence")
]

fig, axes = plt.subplots(1, 5, figsize=(20, 5), sharey=True)
options = [1, 2, 3, 4, 5]

# CSV出力用のデータフレームを作成
df_graph2 = pd.DataFrame({'Likert_Scale': options})

for ax, (v2, title) in zip(axes, scenarios):
    dist = calculate_distribution(v2, fixed_beta)
    
    # データを記録
    scenario_col_name = f'v2_{v2}_Prob'
    df_graph2[scenario_col_name] = dist
    
    # 棒グラフの描画
    colors = ['red' if i==1 else 'orange' if i==4 else 'skyblue' for i in options]
    bars = ax.bar(options, dist, color=colors, edgecolor='black', alpha=0.8)
    
    ax.set_title(f"{title}\n(v2={v2})", fontsize=11)
    ax.set_xlabel('Likert Scale', fontsize=10)
    ax.set_xticks(options)
    ax.set_ylim(0, 1.0)
    ax.grid(axis='y', alpha=0.3)
    
    # パーセンテージの表示
    for bar in bars:
        height = bar.get_height()
        if height > 0.01: # 1%以上のものだけ数値を表示
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height*100:.1f}%', ha='center', va='bottom', fontsize=9)

axes[0].set_ylabel('Observation Probability', fontsize=12)
plt.suptitle(f'Fig 2: Structural Alteration of Data by Bias Level (Certainty Beta={fixed_beta})', fontsize=16, y=1.05)
plt.tight_layout()

# グラフ2の画像保存
fig2_path = os.path.join(output_dir, 'fig2_distribution_scenarios.png')
plt.savefig(fig2_path, bbox_inches='tight', dpi=300, facecolor='white')
plt.show()

# グラフ2のCSV保存
csv2_path = os.path.join(output_dir, 'data_fig2_distribution_scenarios.csv')
df_graph2.to_csv(csv2_path, index=False)

# --- ZIPファイルの作成と自動ダウンロード ---

zip_filename = "simulation_results_archive"
shutil.make_archive(zip_filename, 'zip', output_dir)

print(f"✅ Calculation complete! Automatically downloading {zip_filename}.zip ...")
files.download(f"{zip_filename}.zip")
