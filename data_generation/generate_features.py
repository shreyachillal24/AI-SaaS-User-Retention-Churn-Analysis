import pandas as pd
import numpy as np
import random

# -----------------------------
# Config
# -----------------------------
SESSIONS_FILE = "sessions_raw.csv"
SUBS_FILE = "subscriptions_raw.csv"
OUTPUT_FILE = "feature_usage_raw.csv"

random.seed(42)
np.random.seed(42)

features = {
    "sticky": ["AI_Chat", "AI_Rewrite", "AI_Summarize"],
    "secondary": ["Grammar_Check", "Plagiarism_Check"],
    "low": ["Export_PDF", "Settings"]
}

# -----------------------------
# Load data
# -----------------------------
sessions = pd.read_csv(SESSIONS_FILE)
subs = pd.read_csv(SUBS_FILE)[["user_id", "plan_type"]]

sessions = sessions.merge(subs, on="user_id", how="left")

usage_rows = []
usage_id = 1

# -----------------------------
# Generate feature usage
# -----------------------------
for _, row in sessions.iterrows():
    session_id = row["session_id"]
    plan = row["plan_type"]

    # Features per session
    if pd.isna(plan) or plan.lower() == "free":
        num_features = random.randint(1, 2)
        feature_pool = features["sticky"]
    else:
        num_features = random.randint(2, 4)
        feature_pool = (
            features["sticky"]
            + features["secondary"]
            + features["low"]
        )

    selected_features = random.sample(
        feature_pool,
        k=min(num_features, len(feature_pool))
    )

    for feature in selected_features:
        if feature in features["sticky"]:
            usage_count = random.randint(2, 8)
        elif feature in features["secondary"]:
            usage_count = random.randint(1, 4)
        else:
            usage_count = 1

        usage_rows.append([
            usage_id,
            session_id,
            feature,
            usage_count
        ])

        usage_id += 1

usage_df = pd.DataFrame(
    usage_rows,
    columns=["usage_id", "session_id", "feature_name", "usage_count"]
)

# -----------------------------
# Inject messiness
# -----------------------------

# Feature casing inconsistency
usage_df["feature_name"] = usage_df["feature_name"].apply(
    lambda x: random.choice([x, x.lower(), x.upper()])
)

# Zero or negative usage_count (~2%)
bad_idx = usage_df.sample(frac=0.02, random_state=1).index
usage_df.loc[bad_idx, "usage_count"] = np.random.choice([0, -1])

# Duplicate rows (~1%)
duplicates = usage_df.sample(frac=0.01, random_state=2)
usage_df = pd.concat([usage_df, duplicates], ignore_index=True)

# -----------------------------
# Save
# -----------------------------
usage_df.to_csv(OUTPUT_FILE, index=False)

print("feature_usage_raw.csv generated")
print(usage_df.head())
print("Total rows:", len(usage_df))
