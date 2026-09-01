import os
import pandas as pd

# ======================================================
# Project Root
# ======================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# ======================================================
# File Paths
# ======================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "evaluation_results.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "comparative_analysis.csv"
)

# ======================================================
# Load CSV
# ======================================================

df = pd.read_csv(INPUT_FILE)

# ======================================================
# Basic Metrics
# ======================================================

total_questions = len(df)

# Count failed responses
failed = len(
    df[
        (df["generated_answer"] == "ERROR") |
        (
            df["generated_answer"]
            .str.contains(
                "I could not find sufficient information",
                case=False,
                na=False
            )
        )
    ]
)

successful = total_questions - failed

success_rate = round((successful / total_questions) * 100, 2)
failure_rate = round((failed / total_questions) * 100, 2)

avg_response = round(df["response_time(sec)"].mean(), 2)
avg_sources = round(df["retrieved_source_count"].mean(), 2)

# ======================================================
# Overall Status
# ======================================================

if success_rate >= 90:
    status = "Excellent"
elif success_rate >= 80:
    status = "Good"
elif success_rate >= 70:
    status = "Average"
else:
    status = "Needs Improvement"

# ======================================================
# Save Comparative Analysis
# ======================================================

comparison = [
    ["Total Questions", total_questions],
    ["Successful Responses", successful],
    ["Failed Responses", failed],
    ["Success Rate (%)", success_rate],
    ["Failure Rate (%)", failure_rate],
    ["Average Response Time (sec)", avg_response],
    ["Average Retrieved Sources", avg_sources],
    ["Overall Status", status]
]

comparison_df = pd.DataFrame(
    comparison,
    columns=["Metric", "Value"]
)

comparison_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ======================================================
# Print Results
# ======================================================

print("=" * 60)
print("Comparative Analysis Generated Successfully")
print("=" * 60)

print(f"Total Questions           : {total_questions}")
print(f"Successful Responses      : {successful}")
print(f"Failed Responses          : {failed}")
print(f"Success Rate              : {success_rate}%")
print(f"Failure Rate              : {failure_rate}%")
print(f"Average Response Time     : {avg_response} sec")
print(f"Average Retrieved Sources : {avg_sources}")
print(f"Overall Status            : {status}")

print()
print(f"Saved to: {OUTPUT_FILE}")