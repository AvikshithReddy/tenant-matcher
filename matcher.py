# matcher.py

from __future__ import annotations

import pandas as pd
from datetime import date
from typing import List


def load_units(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Ensure date column is parsed
    df["available_from"] = pd.to_datetime(df["available_from"]).dt.date
    return df


def rank_units(
    df: pd.DataFrame,
    max_rent: int | None,
    min_beds: int,
    min_baths: float | int,
    move_in_date: date,
    pets: str,
    amenities: List[str],
) -> pd.DataFrame:
    """Filter and rank units based on user preferences."""

    filtered = df.copy()

    # Rent filter
    if max_rent is not None:
        filtered = filtered[filtered["rent"] <= max_rent]

    # Beds / baths
    filtered = filtered[filtered["beds"] >= min_beds]
    filtered = filtered[filtered["baths"] >= min_baths]

    # Availability date
    filtered = filtered[filtered["available_from"] <= move_in_date]

    # Pets
    if pets == "must_allow":
        filtered = filtered[filtered["pets"].str.lower() == "allowed"]

    # Amenities scoring
    amenities = [a.lower() for a in amenities if a]  # clean list

    def amenity_score(amenity_str: str) -> int:
        if not amenities:
            return 0
        existing = [x.strip().lower() for x in str(amenity_str).split(",")]
        return sum(1 for a in amenities if a in existing)

    filtered["amenity_score"] = filtered["amenities"].apply(amenity_score)

    # Rank: more amenity matches first, then cheaper rent
    ranked = filtered.sort_values(
        by=["amenity_score", "rent"],
        ascending=[False, True],
    )

    # Return top N (e.g., 20)
    ranked = ranked.head(20).copy()

    return ranked