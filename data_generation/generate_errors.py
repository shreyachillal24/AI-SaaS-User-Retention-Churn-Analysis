import pandas as pd
import numpy as np
import random
from datetime import timedelta

# -----------------------------
# Config
# -----------------------------
SESSIONS_FILE = "sessions_raw.csv"
OUTPUT_FILE = "error_logs_raw.csv"

random.seed(42)
np.random.seed(42)

error_types = {
    "Timeout": 0.40,
    "Rate_Limit": 0.30,
    "Model_Error": 0.20,
    "UI_Bug": 0.10
}

# -----------------------------
# Load sessions
# -----------------------------
sessions = pd.read_csv(
    SESSIONS_FILE,
    parse_dates=["session_start", "session_end"]
)

error_rows = []
error_id = 1

# -----------------------------
# Generate errors
# -----------------------------
for _, row in sessions.iterrows():
    session_id = row["session_id"]
    start = row["session_start"]
    end = row["session_end"]

    # Decide if this session has errors (≈25%)
    if random.random() > 0.25:
        continue

    num_errors = random.randint(1, 3)

    for _ in range(num_errors):
        error_type = np.random.choice(
            list(error_types.keys()),
            p=list(error_types.values())
        )

        # If session_end is null, simulate partial logging
        if pd.isna(end):
            error_time = start + timedelta(
                minutes=random.randint(0, 10)
            )
        else:
            duration_minutes = max(
                int((end - start).total_seconds() / 60), 1
            )
            error_time = start + timedelta(
                minutes=random.randint(0, duration_minutes)
            )

        error_rows.append([
            error_id,
            session_id,
            error_type,
            error_time
        ])

        error_id += 1

errors_df = pd.DataFrame(
    error_rows,
    columns=["error_id", "session_id", "error_type", "error_time"]
)

# -----------------------------
# Inject messiness
# -----------------------------

# Error type casing inconsistency
errors_df["error_type"] = errors_df["error_type"].apply(
    lambda x: random.choice([x, x.lower(), x.upper()])
)

# Error timestamps slightly outside session window (~2%)
bad_time_idx = errors_df.sample(frac=0.02, random_state=1).index
errors_df.loc[bad_time_idx, "error_time"] = (
    errors_df.loc[bad_time_idx, "error_time"]
    + timedelta(minutes=random.randint(5, 30))
)

# Duplicate error rows (~1%)
duplicates = errors_df.sample(frac=0.01, random_state=2)
errors_df = pd.concat([errors_df, duplicates], ignore_index=True)

# -----------------------------
# Save
# -----------------------------
errors_df.to_csv(OUTPUT_FILE, index=False)

print("error_logs_raw.csv generated successfully")
print(errors_df.head())
print("Total rows:", len(errors_df))
