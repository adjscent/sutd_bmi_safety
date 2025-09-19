import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Ensure the graphs folder exists
os.makedirs("graphs", exist_ok=True)

# Latest accuracy data provided by the user
columns = [
    "Condition",
    "Extension",
    "Flexion",
    "Grasp",
    "Left",
    "Nothing",
    "Open",
    "Pronation",
    "Right",
    "Supination",
]
data_accuracy_latest = [
    [
        "Baseline",
        1.0000,
        1.0000,
        1.0000,
        0.8000,
        1.0000,
        1.0000,
        1.0000,
        0.8000,
        0.8000,
    ],
    ["Unseen", 1.0000, 0.6667, 1.0000, 0.6667, 0.3333, 1.0000, 0.3333, 1.0000, 1.0000],
    ["Laser", 0.6667, 0.0000, 0.0000, 0.3333, 1.0000, 1.0000, 0.0000, 1.0000, 0.0000],
    [
        "Microwave",
        1.0000,
        0.0000,
        0.6667,
        0.0000,
        0.3333,
        0.3333,
        0.0000,
        0.0000,
        0.6667,
    ],
    ["5G", 1.0000, 0.3333, 1.0000, 1.0000, 0.0000, 0.6667, 1.0000, 0.0000, 1.0000],
    [
        "Low Frequency",
        0.3333,
        0.0000,
        0.0000,
        0.0000,
        0.0000,
        1.0000,
        0.0000,
        0.0000,
        0.0000,
    ],
]

df_accuracy_latest = pd.DataFrame(data_accuracy_latest, columns=columns).set_index(
    "Condition"
)

# Create heatmap for latest accuracy per class
plt.figure(figsize=(12, 6))
ax = sns.heatmap(
    df_accuracy_latest,
    annot=False,
    fmt=".4f",
    cmap="YlOrRd",
    cbar_kws={"label": "Accuracy"},
)
ax.collections[0].colorbar.ax.yaxis.label.set_size(14)  # Set colorbar label fontsize
ax.collections[0].colorbar.ax.tick_params(labelsize=14)  # Set colorbar ticks fontsize
plt.title(
    "sEMG Per-Class Accuracy Heatmap Across Conditions (Latest Data)", fontsize=18
)
plt.ylabel("Condition", fontsize=14)
plt.xlabel("Class", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()

# Save the heatmap
heatmap_path_latest = os.path.join("graphs", "accuracy_heatmap_latest.png")
plt.savefig(heatmap_path_latest)
plt.close()
