# app.py

from __future__ import annotations

import streamlit as st
import pandas as pd
from datetime import date

from matcher import load_units, rank_units
from email_utils import send_results_email


st.set_page_config(page_title="Tenant Preference Matcher", page_icon="🏘️")

st.title(" Tenant Preference Matching Assistant")
st.write(
    "Answer a few questions and I'll find rental units that best match your needs. "
    "You can optionally get the results emailed to you."
)

# Initialize session state for matches
if "matches_df" not in st.session_state:
    st.session_state["matches_df"] = None


st.subheader(" Tell me about your preferences")

with st.form("preferences_form"):
    col1, col2 = st.columns(2)

    with col1:
        budget = st.number_input(
            "Max monthly rent ($)",
            min_value=500,
            max_value=10000,
            value=2000,
            step=50,
        )
        beds = st.selectbox("Minimum bedrooms", [0, 1, 2, 3, 4], index=1)
        baths = st.selectbox("Minimum bathrooms", [1, 1.5, 2, 2.5, 3], index=0)

    with col2:
        move_in = st.date_input(
            "Target move-in date",
            value=date(2025, 2, 1),
        )
        pets_allowed = st.radio(
            "Pets requirement",
            options=["no_preference", "must_allow"],
            format_func=lambda x: "No preference" if x == "no_preference" else "Must allow pets",
        )

        amenities_wanted = st.multiselect(
            "Preferred amenities (optional)",
            options=[
                "pool",
                "gym",
                "parking",
                "washer_dryer",
                "balcony",
                "clubhouse",
                "elevator",
                "storage",
                "covered_parking",
                "dog_park",
            ],
        )

    submitted = st.form_submit_button("🔍 Find matching units")

if submitted:
    with st.spinner("Finding the best matches for you..."):
        units_df = load_units("data/tenant_units_demo.csv")

        matches_df = rank_units(
            units_df,
            max_rent=int(budget),
            min_beds=int(beds),
            min_baths=float(baths),
            move_in_date=move_in,
            pets=pets_allowed,
            amenities=amenities_wanted,
        )

        if matches_df.empty:
            st.warning("No units matched your criteria. Try relaxing one of your filters.")
            st.session_state["matches_df"] = None
        else:
            st.success(f"Found {len(matches_df)} matching units.")
            st.session_state["matches_df"] = matches_df

# -----------------------------------------
# 2️⃣ Show results (if any)
# -----------------------------------------
matches_df = st.session_state.get("matches_df")

if matches_df is not None:
    st.subheader("2️⃣ Matching Units")

    st.dataframe(
        matches_df[
            [
                "unit_id",
                "community",
                "rent",
                "beds",
                "baths",
                "sqft",
                "amenities",
                "available_from",
                "pets",
                "availability",
            ]
        ],
        use_container_width=True,
    )

    # -----------------------------------------
    # 3️⃣ Email results
    # -----------------------------------------
    st.subheader("3️⃣ Email these results to yourself")

    email = st.text_input("Your email address")

    selectable_units = matches_df["unit_id"].tolist()
    selected_unit_ids = st.multiselect(
        "Which units would you like included in the email?",
        options=selectable_units,
        default=selectable_units,  # by default include all
    )

    if st.button("📩 Send email with selected units"):
        if not email:
            st.error("Please enter your email address.")
        elif not selected_unit_ids:
            st.error("Please select at least one unit.")
        else:
            subset = matches_df[matches_df["unit_id"].isin(selected_unit_ids)]

            try:
                send_results_email(email, subset)
                st.success(f"Email sent to {email} with {len(subset)} units. ✅")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
else:
    st.info("Fill in your preferences above and click **Find matching units** to see results.")