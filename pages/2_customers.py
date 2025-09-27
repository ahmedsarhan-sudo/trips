import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import random as rd





st.markdown("---")


st.set_page_config(
    page_title="Customer Analysis Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    /* Main title */
    .main-title {
        text-align: center;
        color: #fff;
        font-size: 48px !important;
        text-shadow: 2px 2px 5px #000;
        margin-bottom: 30px;
        padding: 15px;
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        border-radius: 10px;
    }
    
    /* Section headers */
    .section-header {
        color: #ff4b2b;
        border-bottom: 2px solid #ff4b2b;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
        font-size: 28px;
    }
    
    /* Sub headers */
    .sub-header {
        color: #243b55;
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141e30, #243b55);
        color: white;
    }
    
    .sidebar-header {
        font-size: 24px;
        color: #ff4b2b;
        margin-bottom: 20px;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 16px;
        border: none;
        transition: 0.3s;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 10px rgba(255,75,43,0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        font-size: 18px !important;
        font-weight: bold;
        color: #333;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ff4b2b;
        color: white;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #243b55;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #ff4b2b;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #243b55;
        padding: 10px;
    }
    
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #243b55;
        padding: 10px;
    }
    
    /* Warning messages */
    .warning-box {
            
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }
    
    /* Success messages */
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-title">👥 Customer Analysis Dashboard</h1>', unsafe_allow_html=True)


if 'df' in st.session_state:
    df = st.session_state['df']
    
   
    if 'ID' not in st.session_state:
        st.session_state['ID'] = ""
    if 'Name' not in st.session_state:
        st.session_state['Name'] = ""
    if 'index' not in st.session_state:
        st.session_state['index'] = 0
    
 
    Custemer_ID_tab, Custemer_Name_tab, index_tap = st.tabs(['Customer ID', 'Customer Name', 'Index Search'])
    
    with Custemer_ID_tab:
        st.markdown('<h2 class="section-header">Search by Customer ID</h2>', unsafe_allow_html=True)
        
      
        cust_id = st.text_input('Enter customer ID', value=st.session_state['ID'], key="ID_input", 
                               placeholder="e.g., CG-12520, SO-20335, etc.")
        
        if cust_id:
            
            cust_df = df[df['Customer ID'] == cust_id]
            
            if not cust_df.empty:
                st.markdown('<h3 class="sub-header">Customer Overview</h3>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col4, col5, col6 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Number of Transactions</div>
                        <div class="metric-value">{cust_df.shape[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Sales</div>
                        <div class="metric-value">${cust_df['Sales'].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Cost</div>
                        <div class="metric-value">${cust_df["Cost"].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Profit</div>
                        <div class="metric-value">${cust_df['Profit'].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Quantity</div>
                        <div class="metric-value">{cust_df['Quantity'].sum()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col6:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Customer Name</div>
                        <div class="metric-value">{cust_df['Customer Name'].unique()[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<h3 class="sub-header">Customer Details</h3>', unsafe_allow_html=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("**Category Distribution**")
                    category_counts = cust_df['Category'].value_counts().reset_index()
                    category_counts.columns = ['Category', 'Count']
                    
                    fig = px.pie(category_counts, values='Count', names='Category', 
                                title='Products by Category', hole=0.4)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, width='stretch')
                
                with col_right:
                    st.markdown("**Sales by Category**")
                    category_sales = cust_df.groupby('Category')['Sales'].sum().reset_index()
                    
                    fig = px.bar(category_sales, x='Category', y='Sales', color='Category',
                                title='Sales by Category')
                    st.plotly_chart(fig, width='stretch')
                
                st.markdown('<h3 class="sub-header">Sub-Category Analysis</h3>', unsafe_allow_html=True)
                
                cat = cust_df['Category'].unique()
                
                category_tabs = st.tabs([f"{category}" for category in cat])
                
                for idx, category in enumerate(cat):
                    with category_tabs[idx]:
                        sub_df = cust_df[cust_df['Category'] == category]
                        sub_category_counts = sub_df['Sub-Category'].value_counts().reset_index()
                        sub_category_counts.columns = ['Sub-Category', 'Count']
                        
                        sub_col1, sub_col2 = st.columns(2)
                        
                        with sub_col1:
                            fig = px.pie(sub_category_counts, values='Count', names='Sub-Category',
                                        title=f'Sub-Categories in {category}')
                            st.plotly_chart(fig, width='stretch' , key=f'sub_category_counts{idx}')
                        
                        with sub_col2:
                            sub_category_sales = sub_df.groupby('Sub-Category')['Sales'].sum().reset_index()
                            fig = px.bar(sub_category_sales, x='Sub-Category', y='Sales', 
                                        color='Sub-Category', title=f'Sales by Sub-Category in {category}')
                            st.plotly_chart(fig, width='stretch' , key=f'sub_category_sales{idx}')
                
                st.markdown('<h3 class="sub-header">Transaction History</h3>', unsafe_allow_html=True)
                st.dataframe(cust_df, width='stretch')
                
            else:
                st.markdown("""
                <div class="warning-box">
                    ⚠️ No customer found with this ID. Please check the ID and try again.
                </div>
                """, unsafe_allow_html=True)
    
    with Custemer_Name_tab:
        st.markdown('<h2 class="section-header">Search by Customer Name</h2>', unsafe_allow_html=True)
        
        cust_name = st.text_input('Enter customer name', value=st.session_state['Name'], key='Name_input',
                                 placeholder="e.g., Claire Gute, Sean O'Donnell, etc.")
        
        if cust_name:
            matching_names = df[df['Customer Name'].str.contains(cust_name, case=False)]['Customer Name'].unique()
            if len(matching_names) > 0:
                st.markdown(f"**Matching names:** {', '.join(matching_names[:5])}{'...' if len(matching_names) > 5 else ''}")
        
        if cust_name:
            cust_df = df[df['Customer Name'] == cust_name]
            
            if not cust_df.empty:
                st.markdown('<h3 class="sub-header">Customer Overview</h3>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col4, col5, col6 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Number of Transactions</div>
                        <div class="metric-value">{cust_df.shape[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Sales</div>
                        <div class="metric-value">${cust_df['Sales'].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Cost</div>
                        <div class="metric-value">${cust_df["Cost"].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Profit</div>
                        <div class="metric-value">${cust_df['Profit'].sum():.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Quantity</div>
                        <div class="metric-value">{cust_df['Quantity'].sum()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col6:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Customer ID</div>
                        <div class="metric-value">{cust_df['Customer ID'].unique()[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<h3 class="sub-header">Customer Details</h3>', unsafe_allow_html=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("**Category Distribution**")
                    category_counts = cust_df['Category'].value_counts().reset_index()
                    category_counts.columns = ['Category', 'Count']
                    
                    fig = px.pie(category_counts, values='Count', names='Category', 
                                title='Products by Category', hole=0.4)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, width='stretch' , key='category_counts_')
                
                with col_right:
                    date_columns = [col for col in cust_df.columns if 'date' in col.lower() or 'time' in col.lower()]
                    if date_columns:
                        st.markdown("**Sales Over Time**")
                        time_series = cust_df.groupby(date_columns[0])['Sales'].sum().reset_index()
                        fig = px.line(time_series, x=date_columns[0], y='Sales', title='Sales Trend Over Time')
                        st.plotly_chart(fig, width='stretch' , key='time_series')
                    else:
                        st.markdown("**Profit by Category**")
                        category_profit = cust_df.groupby('Category')['Profit'].sum().reset_index()
                        fig = px.bar(category_profit, x='Category', y='Profit', color='Category',
                                    title='Profit by Category')
                        st.plotly_chart(fig, width='stretch' , key='category_profit')
                
                st.markdown('<h3 class="sub-header">Transaction History</h3>', unsafe_allow_html=True)
                st.dataframe(cust_df, width='stretch')
                
            else:
                st.markdown("""
                <div class="warning-box">
                    ⚠️ No customer found with this name. Please check the name and try again.
                </div>
                """, unsafe_allow_html=True)
    
    with index_tap:
        st.markdown('<h2 class="section-header">Search by Index</h2>', unsafe_allow_html=True)
        

        if 'index' not in st.session_state:
            st.session_state['index'] = 1  

        
        if st.session_state['index'] < 1:
            st.session_state['index'] = 1
        elif st.session_state['index'] > df.shape[0]:
            st.session_state['index'] = df.shape[0]



        cust_idx = st.number_input('Enter the row index', min_value=1, max_value=df.shape[0], 
                                  step=1, value=st.session_state['index'], key='Index_input')
        
        if cust_idx is not None:
            cust_series = df.iloc[cust_idx-1]
            
            if not cust_series.empty:
                cust_df = cust_series.to_frame().T
                
                st.markdown('<h3 class="sub-header">Transaction Details</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Transaction Summary**")
                    
                    metric_data = [
                        {"title": "Sales", "value": f"${cust_series['Sales']:.2f}"},
                        {"title": "Cost", "value": f"${cust_series['Cost']:.2f}"},
                        {"title": "Profit", "value": f"${cust_series['Profit']:.2f}"},
                        {"title": "Quantity", "value": f"{cust_series['Quantity']}"}
                    ]
                    
                    for metric in metric_data:
                        st.markdown(f"""
                        <div class="metric-card" style="height: 80px; margin-bottom: 10px;">
                            <div class="metric-title">{metric['title']}</div>
                            <div class="metric-value">{metric['value']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Product Details**")
                    
                    product_data = [
                        {"title": "Category", "value": cust_series.get('Category', 'N/A')},
                        {"title": "Sub-Category", "value": cust_series.get('Sub-Category', 'N/A')},
                        {"title": "Product Name", "value": cust_series.get('Product Name', 'N/A')},
                        {"title": "Customer", "value": f"{cust_series.get('Customer Name', 'N/A')} ({cust_series.get('Customer ID', 'N/A')})"}
                    ]
                    
                    for item in product_data:
                        st.markdown(f"""
                        <div style="background-color: #f8f9fa; border-radius: 8px; padding: 12px; color: #000000; margin-bottom: 10px;">
                            <strong>{item['title']}:</strong> {item['value']}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("**Full Transaction Record**")
                st.dataframe(cust_df, width='stretch')
                
                col_prev, col_next, _ = st.columns([1, 1, 3])
                
                with col_prev:
                    if st.button("⬅️ Previous", key="prev_btn"):
                        if cust_idx > 1:
                            st.session_state['index'] = cust_idx - 1
                            st.rerun()
                
                with col_next:
                    if st.button("Next ➡️", key="next_btn"):
                        if cust_idx < df.shape[0]:
                            st.session_state['index'] = cust_idx + 1
                            st.rerun()
            
            else:
                st.markdown("""
                <div class="warning-box">
                    ⚠️ No transaction found with this index. Please check the index and try again.
                </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="info-box">
        ℹ️ Please upload a dataset first using the Data Frame section before accessing customer analytics.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Go to Data Upload"):
        st.info("In a full application, this would navigate to the data upload section.")