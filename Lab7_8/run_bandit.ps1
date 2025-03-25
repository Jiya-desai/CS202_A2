# Create a directory for Bandit reports if it doesn't exist
New-Item -ItemType Directory -Path "bandit_reports" -Force

# Get the last 100 non-merge commits
$commits = git log --format="%H" --no-merges -n 100

# Loop through each commit and run Bandit
foreach ($commit in $commits) {
    Write-Host "Checking out commit: $commit"
    git checkout $commit

    # Run Bandit and save the output
    $reportFile = "bandit_reports/bandit_report_$commit.json"
    bandit -r . --format json -o $reportFile

    Write-Host "Bandit report saved: $reportFile"
}

# Restore the latest commit
git checkout main
Write-Host "Restored to the latest commit."
