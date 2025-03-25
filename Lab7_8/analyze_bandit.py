import json
import os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
report_folder = os.path.join(script_dir, "bandit_reports")

# counters:
severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
confidence_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
cwe_counts = Counter()
timeline = {}

# set to count CWEs across commits only once and avoid incorrect calculations by adding them multiple times
seen_global_issues = set()

if not os.path.exists(report_folder):
    print(f"Error: Report folder '{report_folder}' not found.")
    exit(1)


for filename in sorted(os.listdir(report_folder)):  
    if filename.endswith(".json"):
        commit_hash = filename.replace("bandit_report_", "").replace(".json", "")

        with open(os.path.join(report_folder, filename), "r") as f:
            data = json.load(f)

            high, medium, low = 0, 0, 0
            high_conf, medium_conf, low_conf = 0, 0, 0
            commit_cwe_counts = Counter()
            seen_commit_issues = set()

            for issue in data.get("results", []):
                severity = issue["issue_severity"]
                confidence = issue["issue_confidence"]
                cwe = issue.get("issue_cwe", "Unknown CWE")

                
                if isinstance(cwe, dict):
                    cwe = cwe.get("id", "Unknown CWE")

                issue_location = (issue["filename"], issue["line_number"], cwe)

                if issue_location not in seen_commit_issues:
                    seen_commit_issues.add(issue_location)
                    commit_cwe_counts[cwe] += 1

                if issue_location not in seen_global_issues:
                    seen_global_issues.add(issue_location)
                    cwe_counts[cwe] += 1

                if severity == "HIGH":
                    high += 1
                elif severity == "MEDIUM":
                    medium += 1
                elif severity == "LOW":
                    low += 1

                if confidence == "HIGH":
                    high_conf += 1
                elif confidence == "MEDIUM":
                    medium_conf += 1
                elif confidence == "LOW":
                    low_conf += 1

            # for storing the data in json file:
            timeline[commit_hash] = {
                "severity": {"HIGH": high, "MEDIUM": medium, "LOW": low},
                "confidence": {"HIGH": high_conf, "MEDIUM": medium_conf, "LOW": low_conf},
                "cwe_counts": dict(commit_cwe_counts)
            }

# once json file for severity and confidence information and one for cwe counts
timeline_file_path = os.path.join(script_dir, "timeline_data.json")

with open(timeline_file_path, "w") as f:
    json.dump(timeline, f, indent=4)

cwe_count_file_path = os.path.join(script_dir, "cwe_counts.json")

with open(cwe_count_file_path, "w") as f:
    json.dump(dict(cwe_counts), f, indent=4)

print(f"\nData saved in '{timeline_file_path}' for commit-level analysis.")
print(f"CWE counts saved in '{cwe_count_file_path}' for global analysis.")
