import os
import subprocess
import re

# Define test configurations
commands = {
    "pytest_n1_dist_load_parallel_1": "pytest -n 1 --dist load --parallel-threads 1",
    "pytest_n1_dist_load_parallel_auto": "pytest -n 1 --dist load --parallel-threads auto",
    "pytest_n_auto_dist_load_parallel_1": "pytest -n auto --dist load --parallel-threads 1",
    "pytest_n_auto_dist_load_parallel_auto": "pytest -n auto --dist load --parallel-threads auto",
    "pytest_n1_dist_no_parallel_1": "pytest -n 1 --dist no --parallel-threads 1",
    "pytest_n1_dist_no_parallel_auto": "pytest -n 1 --dist no --parallel-threads auto",
    "pytest_n_auto_dist_no_parallel_1": "pytest -n auto --dist no --parallel-threads 1",
    "pytest_n_auto_dist_no_parallel_auto": "pytest -n auto --dist no --parallel-threads auto",
}

main_folder = "parallel_test_results"
os.makedirs(main_folder, exist_ok=True)

# to extract execution time from the output of the command
execution_time_pattern = re.compile(r"=+ .* in (\d+\.\d+)s =+")
for test_name, command in commands.items():
    test_folder = os.path.join(main_folder, test_name)
    os.makedirs(test_folder, exist_ok=True)

    execution_times = []
    failure_counts = []
    all_failing_tests = []

    print(f"Running: {test_name}")
    
    for i in range(1, 4):
        log_file = os.path.join(test_folder, f"run_{i}.log")
        with open(log_file, "w") as f:
            process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            f.write(process.stdout)  # write output to file

        with open(log_file, "r") as f:
            log_content = f.readlines()

        # execution time:
        execution_time = -1
        for line in log_content:
            match = execution_time_pattern.search(line)
            if match:
                execution_time = float(match.group(1))
                break

        execution_times.append(execution_time)

        # failing test names extraction:
        failed_tests = [line.strip() for line in log_content if "FAILED" in line and "::" in line]
        failure_counts.append(len(failed_tests))
        all_failing_tests.append(failed_tests)

    # summary file to get average execution time of three runs of each configuration:
    summary_file = os.path.join(test_folder, "summary.log")
    with open(summary_file, "w") as f:
        f.write(f"Test Configuration: {test_name}\n")
        f.write(f"Command: {command}\n\n")
        
        for i, (time_taken, failures, failing_tests) in enumerate(zip(execution_times, failure_counts, all_failing_tests), start=1):
            f.write(f"Run {i}: Time = {time_taken:.2f}s, Failures = {failures}\n")
            if failing_tests:
                f.write(f"  Failing Tests:\n")
                for test in failing_tests:
                    f.write(f"    {test}\n")
        
        avg_time = sum(execution_times) / 3
        avg_failures = sum(failure_counts) / 3

        f.write(f"\nAverage Execution Time: {avg_time:.2f}s\n")
        f.write(f"Average Failures: {avg_failures:.2f}\n")

print("done")
