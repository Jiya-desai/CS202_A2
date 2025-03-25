import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Load the timeline data
with open("timeline_data.json", "r") as f:
    timeline = json.load(f)

# Extract commit hashes sorted chronologically
commits = sorted(timeline.keys())

# Extract data for plotting
high_severity = [timeline[c]["severity"]["HIGH"] for c in commits]
medium_severity = [timeline[c]["severity"]["MEDIUM"] for c in commits]
low_severity = [timeline[c]["severity"]["LOW"] for c in commits]

high_confidence = [timeline[c]["confidence"]["HIGH"] for c in commits]
medium_confidence = [timeline[c]["confidence"]["MEDIUM"] for c in commits]
low_confidence = [timeline[c]["confidence"]["LOW"] for c in commits]

# Define step size for x-axis labels (intervals of 10)
step_size = 10  # Adjust dynamically for smaller datasets
x_indices = np.arange(len(commits))  # Numeric indices for commits

# Create folder for saving graphs
graph_folder = "graphs"
os.makedirs(graph_folder, exist_ok=True)

# Plot severity trend
plt.figure(figsize=(12, 6))
plt.plot(x_indices, high_severity, label='High Severity', color='red')
plt.plot(x_indices, medium_severity, label='Medium Severity', color='orange')
plt.plot(x_indices, low_severity, label='Low Severity', color='green')

plt.xlabel("Commit Index (starting from the latest commmit for the last 100 non-merge commits)")
plt.ylabel("Number of Issues")
plt.title("Trend of Severity Levels Over Commits")

plt.xticks(x_indices[::step_size])  # X-axis labels at intervals of 10
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(graph_folder, "severity_trend.png"))  # Save the plot
plt.show()

# Plot confidence trend
plt.figure(figsize=(12, 6))
plt.plot(x_indices, high_confidence, label='High Confidence', color='blue')
plt.plot(x_indices, medium_confidence, label='Medium Confidence', color='purple')
plt.plot(x_indices, low_confidence, label='Low Confidence', color='brown')

plt.xlabel("Commit Index (starting from the latest commmit for the last 100 non-merge commits)")
plt.ylabel("Number of Issues")
plt.title("Trend of Confidence Levels Over Commits")

plt.xticks(x_indices[::step_size])  # X-axis labels at intervals of 10
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(graph_folder, "confidence_trend.png"))  # Save the plot
plt.show()

# Plot severity vs. confidence trends in separate graphs
severity_levels = {
    "High Severity": (high_severity, high_confidence, "red", "blue"),
    "Medium Severity": (medium_severity, medium_confidence, "orange", "purple"),
    "Low Severity": (low_severity, low_confidence, "green", "brown")
}

for severity_label, (severity_data, confidence_data, severity_color, confidence_color) in severity_levels.items():
    plt.figure(figsize=(12, 6))
    plt.plot(x_indices, severity_data, label=f'{severity_label}', color=severity_color)
    # plt.plot(x_indices, confidence_data, label=f'{severity_label} Confidence', color=confidence_color, linestyle='dashed')

    plt.xlabel("Commit Index (starting from the latest commmit for the last 100 non-merge commits)")
    plt.ylabel("Number of Issues")
    plt.title(f"Trend of {severity_label}")

    plt.xticks(x_indices[::step_size])  # X-axis labels at intervals of 10
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, f"{severity_label.replace(' ', '_').lower()}_trend.png"))  # Save the plot
    plt.show()
