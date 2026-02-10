import pandas as pd
import numpy as np
import random
from datetime import timedelta

# -----------------------------
# Configuration
# -----------------------------
INPUT_USERS_FILE = "users_raw.csv"
OUTPUT_FILE = "subscriptions_raw.csv"

random.seed(42)
np.random.seed(42)

PLAN_DISTRIBUTION = {
    "Free": 0.70,
    "Pro": 0.25,
    "Team": 0.05
}

CHURN_RATES = {
    "Free": 0.35,
    "Pro": 0.20,
    "Team": 0.10
}

# -----------------------------
# Load users
# -----------------------------
users_df = pd.read_csv(INPUT_USERS_FILE, parse_dates=["signup_date"])

# 🔴 SANITY CHECK (this is the fix)
if len(users_df) < 9000:
    raise ValueError(
        f"users_raw.csv has only {len(users_df)} rows. "
        "Expected ~10,000. Fix users_raw before generating subscriptions."
    )

# Drop ~2% users to simulate missing subscriptions
users_df = users_df.sample(frac=0.98, random_state=42).reset_index(drop=True)

# -----------------------------
# Assign plans
# -----------------------------
users_df["plan_type"] = np.random.choice(
    list(PLAN_DISTRIBUTION.keys()),
    size=len(users_df),
    p=list(PLAN_DISTRIBUTION.values())
)

# -----------------------------
# Generate subscription dates
# -----------------------------
start_dates = []
end_dates = []
statuses = []

for _, row in users_df.iterrows():
    signup_date = row["signup_date"]
    plan = row["plan_type"]

    if plan == "Free":
        start_date = signup_date + timedelta(days=random.randint(0, 3))
    else:
        start_date = signup_date + timedelta(days=random.randint(0, 14))

    churned = random.random() < CHURN_RATES[plan]

    if churned:
        status = "cancelled"
        lifetime_days = random.randint(7, 180)
        end_date = start_date + timedelta(days=lifetime_days)
    else:
        status = "active"
        end_date = None

    start_dates.append(start_date)
    end_dates.append(end_date)
    statuses.append(status)

users_df["start_date"] = start_dates
users_df["end_date"] = end_dates
users_df["status"] = statuses

# -----------------------------
# Intentional messiness
# -----------------------------
mask = users_df.sample(frac=0.10, random_state=1).index
users_df.loc[mask, "plan_type"] = users_df.loc[mask, "plan_type"].apply(
    lambda x: random.choice([x.lower(), x.upper(), x])
)

null_mask = users_df.sample(frac=0.02, random_state=2).index
users_df.loc[null_mask, "plan_type"] = None

# -----------------------------
# Finalize table
# -----------------------------
subscriptions_df = users_df.reset_index(drop=True)
subscriptions_df.insert(0, "subscription_id", range(1, len(subscriptions_df) + 1))

subscriptions_df = subscriptions_df[
    ["subscription_id", "user_id", "plan_type", "start_date", "end_date", "status"]
]

# -----------------------------
# Save output
# -----------------------------
subscriptions_df.to_csv(OUTPUT_FILE, index=False)

print("subscriptions_raw.csv generated successfully")
print("Total rows:", len(subscriptions_df))
print(subscriptions_df.head())
