## users_raw.csv

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
Faker.seed(42)
np.random.seed(42)

# -----------------------------
# Configuration
# -----------------------------
NUM_USERS = 10_000

acquisition_channels = {
    "Organic": 0.45,
    "Paid Ads": 0.30,
    "Referral": 0.15,
    "Partnership": 0.10
}

countries = {
    "India": 0.35,
    "USA": 0.30,
    "UK": 0.15,
    "Germany": 0.10,
    "Others": 0.10
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# -----------------------------
# Helper functions
# -----------------------------
def random_signup_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# -----------------------------
# Data generation
# -----------------------------
user_ids = np.arange(1, NUM_USERS + 1)

signup_dates = [random_signup_date(start_date, end_date) for _ in range(NUM_USERS)]

acquisition_channel_values = np.random.choice(
    list(acquisition_channels.keys()),
    size=NUM_USERS,
    p=list(acquisition_channels.values())
)

country_values = np.random.choice(
    list(countries.keys()),
    size=NUM_USERS,
    p=list(countries.values())
)

users_df = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": signup_dates,
    "country": country_values,
    "acquisition_channel": acquisition_channel_values
})

# -----------------------------
# Intentional messiness (REALISTIC)
# -----------------------------

# Introduce null countries (≈3%)
null_country_idx = users_df.sample(frac=0.03, random_state=42).index
users_df.loc[null_country_idx, "country"] = None

# Inconsistent acquisition channel casing
mask = users_df["acquisition_channel"] == "Paid Ads"
users_df.loc[mask, "acquisition_channel"] = np.random.choice(
    ["Paid Ads", "paid ads", "PAID ADS"],
    size=mask.sum()
)

# Duplicate a small number of rows (≈0.5%)
duplicates = users_df.sample(frac=0.005, random_state=1)
users_df = pd.concat([users_df, duplicates], ignore_index=True)

# -----------------------------
# Save to CSV
# -----------------------------
users_df.to_csv("users_raw.csv", index=False)

print("users_raw.csv generated successfully")
print(users_df.head())
