import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Ensure the graphs folder exists
os.makedirs("graphs", exist_ok=True)

# Latest accuracy data provided by the user
columns = ["Condition", "Extension", "Flexion", "Grasp", "Left", "Nothing", "Open", "Pronation", "Right", "Supination"]
data_accuracy_latest = [
    ["20Hz", 0.6667, 0.6667, 0.6667, 0.0000, 0.0000, 1.0000, 0.3333, 0.3333, 0.0000],
    ["25Hz", 0.3333, 0.0000, 0.3333, 0.0000, 0.0000, 0.3333, 1.0000, 0.0000, 0.0000],
    ["40Hz", 0.3333, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000]
]

df_accuracy_latest = pd.DataFrame(data_accuracy_latest, columns=columns).set_index("Condition")

# Create heatmap for latest accuracy per class
plt.figure(figsize=(12, 6))
sns.heatmap(df_accuracy_latest, annot=True, fmt=".4f", cmap="YlOrRd", cbar_kws={'label': 'Accuracy'})
plt.title("sEMG Per-Class Accuracy Heatmap Across Conditions (Latest Data)")
plt.ylabel("Condition")
plt.xlabel("Class")
plt.tight_layout()

# Save the heatmap
heatmap_path_latest = os.path.join("graphs", "accuracy_heatmap_latest.png")
plt.savefig(heatmap_path_latest)
plt.close()