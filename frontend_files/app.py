import streamlit as st
import pandas as pd
import requests
import json
import os

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 SuperKart Outlet Sales Forecasting")
st.markdown("Predict product-level sales revenue across outlets using our tuned ensemble model.")

# Backend API endpoint - uses container name 'backend' in Docker network or localhost as fallback
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000/predict")

st.sidebar.header("Store & Product Configuration")

# User input form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Product Attributes")
        product_weight = st.number_input("Product Weight (kg)", min_value=1.0, max_value=30.0, value=12.5, step=0.1)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_allocated_area = st.slider("Product Display Area Ratio", min_value=0.001, max_value=0.35, value=0.05, step=0.005)
        product_type = st.selectbox(
            "Product Type",
            [
                "Fruits and Vegetables", "Snack Foods", "Household", "Frozen Foods", 
                "Dairy", "Canned", "Baking Goods", "Health and Hygiene", 
                "Meat", "Soft Drinks", "Breads", "Hard Drinks", 
                "Others", "Starchy Foods", "Breakfast", "Seafood"
            ]
        )
        product_mrp = st.number_input("Product MRP ($)", min_value=10.0, max_value=350.0, value=150.0, step=1.0)
        product_category_code = st.selectbox("Product Category Code", ["FD", "DR", "NC"], help="FD = Food, DR = Drinks, NC = Non-Consumable")

    with col2:
        st.subheader("🏬 Store Attributes")
        store_id = st.selectbox("Store Identifier", ["OUT001", "OUT002", "OUT003", "OUT004"])
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
        store_age = st.slider("Store Age (Years)", min_value=1, max_value=50, value=15, step=1)

    submitted = st.form_submit_button("Forecast Sales 🚀", use_container_width=True)

if submitted:
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Id": store_id,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_city_type,
        "Store_Type": store_type,
        "Store_Age": store_age,
        "Product_Category_Code": product_category_code
    }
    
    with st.spinner("Generating sales forecast..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                predicted_sales = result["predictions"][0]
                st.success(f"### 📈 Projected Product Store Sales: **${predicted_sales:,.2f}**")
            else:
                st.error(f"API Error (Status {response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to backend service at `{BACKEND_URL}`. Ensure backend container is running.")
        except Exception as e:
            st.error(f"Prediction request failed: {str(e)}")
