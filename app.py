import streamlit as st
import pandas as pd
from itertools import combinations

# Load data
med_df = pd.read_csv("medications.csv")
supp_df = pd.read_csv("supplements.csv")
int_df = pd.read_csv("interactions.csv")

# Combine all items into one list
all_items = list(med_df["name"].dropna().unique()) + list(supp_df["name"].dropna().unique())

# Title
st.title("🛡️ MedGuard")
st.subheader("Take control of your medication")

st.write("Enter your medications and supplements to check for interactions.")

# User input
selected_items = st.multiselect("Select items:", sorted(all_items))

# Function to check interactions
def check_all_interactions(items, interactions_df):
    results = []

    for a, b in combinations(items, 2):
        result = interactions_df[
            ((interactions_df["item_a"] == a) & (interactions_df["item_b"] == b)) |
            ((interactions_df["item_a"] == b) & (interactions_df["item_b"] == a))
        ]
        
        if not result.empty:
            results.append(result.iloc[0].to_dict())

    return results

# Button
if st.button("Check Interactions"):

    if len(selected_items) < 2:
        st.warning("Please select at least two items.")
    else:
        results = check_all_interactions(selected_items, int_df)

        if results:
            st.error("⚠ Interactions Found")

            for r in results:
                st.write(f"**{r['item_a']} + {r['item_b']}**")
                st.write(f"Severity: {r['severity']}")
                st.write(f"Details: {r['description']}")
                st.write("---")
        else:
            st.success("✅ No known interactions found.")

# Disclaimer
st.caption("MedGuard provides informational insights only and does not replace professional medical advice.")