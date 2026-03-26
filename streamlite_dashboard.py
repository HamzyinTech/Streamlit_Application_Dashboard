# streamlit_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 1️⃣ Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Books Analytics Dashboard",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# 2️⃣ Dark Theme Styling
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stMetric {
    background-color: #1a1f2e;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3️⃣ Load Data (Cached for Performance)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("books_cleaned.csv")

df = load_data()



# --------------------------------------------------
# 4️⃣ Sidebar Filters
# --------------------------------------------------
st.sidebar.title("📊 Dashboard Filters")

# Price Range Filter
price_options = df["Price Range (₦)"].dropna().unique()
selected_price = st.sidebar.multiselect(
    "Select Price Range",
    price_options,
    default=price_options
)

# Rating Group Filter
rating_options = df["Rating Group"].dropna().unique()
selected_rating = st.sidebar.multiselect(
    "Select Rating Group",
    rating_options,
    default=rating_options
)

# Availability Filter
availability_options = df["Availability"].unique()
selected_availability = st.sidebar.multiselect(
    "Select Availability",
    availability_options,
    default=availability_options
)

# Book Search
search_book = st.sidebar.text_input("🔍 Search Book Title")

# --------------------------------------------------
# 5️⃣ Apply Filters
# --------------------------------------------------
filtered_df = df[
    (df["Price Range (₦)"].isin(selected_price)) &
    (df["Rating Group"].isin(selected_rating)) &
    (df["Availability"].isin(selected_availability))
]

# Search filter
if search_book:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(search_book, case=False)
    ]

# --------------------------------------------------
# 6️⃣ Dashboard Title
# --------------------------------------------------
st.title("📚 Books Analytics Dashboard")
st.markdown("Interactive dashboard analyzing scraped book data.")

# --------------------------------------------------
# 7️⃣ KPI Section
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Books",
    len(filtered_df)
)

col2.metric(
    "Average Price (₦)",
    f"{filtered_df['Price (₦)'].mean():,.0f}"
)

col3.metric(
    "Average Rating",
    f"{filtered_df['Rating'].mean():.2f}"
)

col4.metric(
    "Max Book Price",
    f"₦{filtered_df['Price (₦)'].max():,.0f}"
)

st.divider()

# --------------------------------------------------
# 8️⃣ Charts Section
# --------------------------------------------------

col1, col2 = st.columns(2)

# Price Range Chart
fig_price = px.histogram(
    filtered_df,
    x="Price Range (₦)",
    color="Price Range (₦)",
    color_discrete_sequence=px.colors.sequential.Blues,
    title="Books Distribution by Price Range"
)

fig_price.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

col1.plotly_chart(fig_price, use_container_width=True)

# Rating Distribution Pie Chart
fig_rating = px.pie(
    filtered_df,
    names="Rating Group",
    title="Books by Rating Group",
    color_discrete_sequence=px.colors.sequential.Blues
)

fig_rating.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

col2.plotly_chart(fig_rating, use_container_width=True)

st.divider()

# --------------------------------------------------
# 9️⃣ Top Expensive Books Chart
# --------------------------------------------------
st.subheader("💰 Top 10 Most Expensive Books")

top_books = filtered_df.sort_values(
    by="Price (₦)",
    ascending=False
).head(10)

fig_top = px.bar(
    top_books,
    x="Price (₦)",
    y="Title",
    orientation="h",
    color="Price (₦)",
    color_continuous_scale="Blues"
)

fig_top.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white",
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# --------------------------------------------------
# 🔟 Data Table Section
# --------------------------------------------------
st.subheader("📋 Filtered Books Dataset")

st.dataframe(
    filtered_df.reset_index(drop=True),
    use_container_width=True
)

# --------------------------------------------------
# 1️⃣1️⃣ Download Button
# --------------------------------------------------
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_books.csv",
    mime="text/csv"
)