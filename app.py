import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="E-Commerce Product Analysis Dashboard",
    page_icon="🛒",
    layout="wide",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.08);
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #475569;
        margin-bottom: 0.35rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Product Data
# -----------------------------
products = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Smart Watch",
            "Tablet",
            "Keyboard",
            "Mouse",
            "Monitor",
            "Power Bank",
            "Bluetooth Speaker",
        ],
        "Category": [
            "Electronics",
            "Electronics",
            "Audio",
            "Wearables",
            "Electronics",
            "Accessories",
            "Accessories",
            "Electronics",
            "Accessories",
            "Audio",
        ],
        "Price": [65000, 35000, 2500, 5000, 28000, 1800, 900, 15000, 2200, 3500],
        "Rating": [4.5, 4.4, 4.2, 4.3, 4.1, 4.0, 4.2, 4.5, 4.0, 4.3],
        "Sales": [120, 250, 420, 180, 150, 300, 500, 110, 380, 290],
    }
)
products["Revenue"] = products["Price"] * products["Sales"]

# -----------------------------
# Sidebar Filters
# -----------------------------
with st.sidebar:
    st.header("Filters")
    selected_categories = st.multiselect(
        "Select Product Categories",
        options=sorted(products["Category"].unique()),
        default=sorted(products["Category"].unique()),
    )
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, step=0.1)

filtered_products = products[
    products["Category"].isin(selected_categories)
    & (products["Rating"] >= min_rating)
].copy()

if filtered_products.empty:
    st.warning("No products match the current filters. Please adjust the filter settings.")
    st.stop()

# -----------------------------
# KPI Calculations
# -----------------------------
total_products = len(filtered_products)
total_sales = int(filtered_products["Sales"].sum())
total_revenue = filtered_products["Revenue"].sum()
average_price = filtered_products["Price"].mean()
average_rating = filtered_products["Rating"].mean()
best_seller = filtered_products.loc[filtered_products["Sales"].idxmax(), "Product"]

# -----------------------------
# Header
# -----------------------------
st.title("🛒 E-Commerce Performance Dashboard")
st.caption("Sales, pricing, rating, and category performance overview")

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Products</div>
            <div class="metric-value">{total_products}</div>
            <div class="metric-sub">Visible catalog items</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Sales</div>
            <div class="metric-value">{total_sales:,}</div>
            <div class="metric-sub">Units sold</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Revenue</div>
            <div class="metric-value">₹{total_revenue:,.0f}</div>
            <div class="metric-sub">Gross revenue</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg. Rating</div>
            <div class="metric-value">{average_rating:.2f}/5</div>
            <div class="metric-sub">Top product: {best_seller}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# -----------------------------
# Chart Row 1
# -----------------------------
col_left, col_right = st.columns([1.7, 1])

with col_left:
    st.subheader("📊 Product Sales Performance")
    sales_data = filtered_products.sort_values("Sales", ascending=False)
    fig_sales = px.bar(
        sales_data,
        x="Sales",
        y="Product",
        orientation="h",
        color="Sales",
        color_continuous_scale="Viridis",
        title="Sales by Product",
        labels={"Sales": "Units Sold", "Product": "Product"},
        text="Sales",
    )
    fig_sales.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_x=0.05,
        margin=dict(l=10, r=20, t=40, b=10),
    )
    st.plotly_chart(fig_sales, use_container_width=True)

with col_right:
    st.subheader("💵 Revenue Mix")
    category_revenue = (
        filtered_products.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    )
    fig_donut = px.pie(
        category_revenue,
        names="Category",
        values="Revenue",
        hole=0.55,
        title="Revenue by Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_donut.update_traces(textinfo="percent+label", pull=[0.04 for _ in category_revenue["Category"]])
    fig_donut.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.05,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------
# Chart Row 2
# -----------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("💰 Product Pricing")
    price_data = filtered_products.sort_values("Price", ascending=False)
    fig_price = px.bar(
        price_data,
        x="Product",
        y="Price",
        color="Price",
        color_continuous_scale="Blues",
        title="Price Comparison",
        labels={"Price": "Price (₹)", "Product": "Product"},
        text="Price",
    )
    fig_price.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.05,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_tickangle=-25,
    )
    st.plotly_chart(fig_price, use_container_width=True)

with col_b:
    st.subheader("📈 Price vs Rating")
    fig_scatter = px.scatter(
        filtered_products,
        x="Price",
        y="Rating",
        size="Sales",
        color="Category",
        hover_name="Product",
        title="Price vs Rating",
        labels={"Price": "Price (₹)", "Rating": "Rating", "Sales": "Units Sold"},
        size_max=30,
    )
    fig_scatter.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.05,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Category Performance
# -----------------------------
st.subheader("📦 Category Performance")
category_summary = (
    filtered_products.groupby("Category", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Average_Price=("Price", "mean"),
        Average_Rating=("Rating", "mean"),
        Revenue=("Revenue", "sum"),
    )
    .sort_values("Revenue", ascending=False)
)

fig_category = px.bar(
    category_summary,
    x="Category",
    y="Revenue",
    color="Category",
    title="Category Revenue",
    labels={"Revenue": "Revenue (₹)", "Category": "Category"},
    text_auto=".2s",
)
fig_category.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_x=0.05,
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig_category, use_container_width=True)

# -----------------------------
# Product Details & Insights
# -----------------------------
st.subheader("📋 Product Performance Table")
product_table = filtered_products[
    ["Product", "Category", "Price", "Sales", "Rating", "Revenue"]
].sort_values("Revenue", ascending=False)

st.dataframe(product_table, use_container_width=True, hide_index=True)

# -----------------------------
# Top insights
# -----------------------------
st.subheader("✨ Executive Summary")

best_category = category_summary.loc[category_summary["Revenue"].idxmax(), "Category"]
best_product = filtered_products.loc[filtered_products["Sales"].idxmax(), "Product"]
highest_value_product = filtered_products.loc[filtered_products["Revenue"].idxmax(), "Product"]

st.markdown(
    f"""
    - Best performing category: **{best_category}**
    - Best selling product: **{best_product}**
    - Highest revenue product: **{highest_value_product}**
    - Average product revenue: **₹{(filtered_products['Revenue'].mean()):,.0f}**
    - Average product price: **₹{average_price:,.0f}**
    """
)

st.caption("This dashboard is designed to highlight the strongest revenue drivers, category trends, and product value opportunities.")