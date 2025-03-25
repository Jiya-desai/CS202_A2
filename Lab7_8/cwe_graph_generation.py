import json
import os
import matplotlib.pyplot as plt

# Load CWE counts from JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
cwe_count_file_path = os.path.join(script_dir, "cwe_counts.json")

with open(cwe_count_file_path, "r") as f:
    cwe_counts = json.load(f)

# Sort CWE counts in descending order
sorted_cwe_counts = sorted(cwe_counts.items(), key=lambda x: x[1], reverse=True)
cwe_labels, cwe_values = zip(*sorted_cwe_counts)  # Unpacking labels and values

# Create folder for saving the graph
graph_folder = os.path.join(script_dir, "graphs")
os.makedirs(graph_folder, exist_ok=True)

# Plot CWE frequency
plt.figure(figsize=(10, 5))
plt.bar(cwe_labels, cwe_values, color='teal')

plt.xlabel("CWE ID")
plt.ylabel("Occurrences")
plt.title("CWE Frequency in Repository")

# Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.grid(axis='y')

# Save the figure
plot_path = os.path.join(graph_folder, "cwe_counts.png")
plt.tight_layout()
plt.savefig(plot_path)

# Show the plot
plt.show()

print(f"CWE frequency plot saved at: {plot_path}")
