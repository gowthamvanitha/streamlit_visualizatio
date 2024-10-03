import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"C:\Users\gowth\OneDrive\Desktop\streamlit tut\sales_dataset_with_items.xlsx"
df = pd.read_excel(file_path)

# Dashboard title and style
st.set_page_config(page_title="Corporate Sales Dashboard", page_icon="🏢", layout="wide")
st.title("Corporate Sales Dashboard")
st.markdown("<hr>", unsafe_allow_html=True)

# Custom styling for the dashboard
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #f0f4f7;
    }
    .css-ffhzg2 {
        color: #2C3E50;
        font-family: 'Arial', sans-serif;
    }
    .css-1v3fvcr {
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar design
with st.sidebar:
    st.markdown("<h2 style='color: #2C3E50;'>Filters</h2>", unsafe_allow_html=True)
    state = st.selectbox("Select State", df['State'].unique())
    district = st.selectbox("Select District", df[df['State'] == state]['District'].unique())
    item = st.selectbox("Select Item", df[df['District'] == district]['Items Name'].unique())
    year = st.selectbox("Select Year", df['Year'].unique())

# Filter dataset based on selections
filtered_df = df[(df['State'] == state) &
                 (df['District'] == district) &
                 (df['Items Name'] == item) &
                 (df['Year'] == year)]

# Display selected data
st.subheader(f"Data for {state}, {district}, Item: {item}, Year: {year}")
st.dataframe(filtered_df)

# Enhanced visualization of sales trend
st.subheader("Sales Trend over the Years")
yearly_sales = df[(df['State'] == state) & (df['District'] == district) & (df['Items Name'] == item)].groupby('Year')['Counts'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.set_theme(style="whitegrid")
sns.lineplot(x='Year', y='Counts', data=yearly_sales, marker='o', color='#1f77b4', lw=2)

plt.title(f'Sales Trend for {item} in {state} - {district}', fontsize=16, color="#2C3E50")
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Sales Quantity', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)

# Add a bar chart showing the total quantity sold per year for the selected item
st.subheader("Year-wise Sales Comparison")
plt.figure(figsize=(10, 5))

# Updated usage of 'hue' to avoid FutureWarning
sns.barplot(x='Year', y='Counts', data=yearly_sales, hue='Year', palette='Blues_d', legend=False)

plt.title(f'Sales Comparison for {item} across Years', fontsize=16, color="#2C3E50")
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Sales Quantity', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)

# **New Visualization**: Pie chart showing the sales distribution across years
st.subheader("Sales Distribution by Year")
plt.figure(figsize=(7, 7))
sales_by_year = df[df['Items Name'] == item].groupby('Year')['Counts'].sum().reset_index()
sales_by_year.set_index('Year', inplace=True)

plt.pie(sales_by_year['Counts'], labels=sales_by_year.index, autopct='%1.1f%%', colors=sns.color_palette("Blues_d", len(sales_by_year)))

plt.title(f'Sales Distribution for {item} by Year', fontsize=16, color="#2C3E50")
plt.tight_layout()

st.pyplot(plt)

# **New Visualization**: Histogram to visualize the distribution of sales quantities
st.subheader("Sales Quantity Distribution")
plt.figure(figsize=(10, 5))
sns.histplot(df[(df['State'] == state) & (df['District'] == district) & (df['Items Name'] == item)]['Counts'], bins=10, kde=True, color='#2C3E50')

plt.title(f'Distribution of Sales Quantities for {item}', fontsize=16, color="#2C3E50")
plt.xlabel('Sales Quantity', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.tight_layout()

st.pyplot(plt)

# **New Visualization**: Heatmap for correlation analysis of numeric fields
st.subheader("Correlation Heatmap")
numeric_cols = ['Counts', 'Demand', 'Items Purchased']
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

plt.title("Correlation Heatmap of Sales and Demand Metrics", fontsize=16, color="#2C3E50")
plt.tight_layout()

st.pyplot(plt)

# KPI display for better insight
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Key Metrics")

total_sales = filtered_df['Counts'].sum()
average_sales_per_year = yearly_sales['Counts'].mean()

# KPI display using metric widget
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Average Sales per Year", f"{average_sales_per_year:,.0f}")
col3.metric("Selected Year Sales", f"{filtered_df['Counts'].sum():,.0f}")

# Add a footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='color: #7f8c8d; font-size: 12px;'>© 2024 Corporate Sales Insights | All rights reserved</footer>", unsafe_allow_html=True)
