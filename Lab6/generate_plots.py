import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data from the table
data = [
    ["Load", 1, 1, 5.81, 0],
    ["Load", "auto", 1, 8.3, 0],
    ["Load", 1, "auto", 34.73, 4],
    ["Load", "auto", "auto", 47.56, 3.67],  # Averaged failures
    ["No", 1, 1, 6.38, 0],
    ["No", "auto", 1, 14.67, 0],
    ["No", 1, "auto", 49.96, 4],
    ["No", "auto", "auto", 53.46, 4],
]

# Convert data to a DataFrame
df = pd.DataFrame(data, columns=["Distribution Mode", "Worker Processes (n)", "Parallel Threads", "Execution Time (s)", "Failures"])

# Set Seaborn style
sns.set_style("whitegrid")

# --- Bar Plot: Execution Time ---
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Parallel Threads", y="Execution Time (s)", hue="Distribution Mode", dodge=True)
plt.title("Execution Time vs Parallel Threads")
plt.ylabel("Execution Time (s)")
plt.xlabel("Parallel Threads")
plt.legend(title="Distribution Mode")
plt.show()

# --- Scatter Plot: Failures vs Execution Time ---
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Execution Time (s)", y="Failures", hue="Distribution Mode", style="Parallel Threads", s=100)
plt.title("Failures vs Execution Time")
plt.ylabel("Number of Failing Test Cases")
plt.xlabel("Execution Time (s)")
plt.legend(title="Configuration")
plt.show()
