import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from scipy.stats.mstats import winsorize
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="MultiOutput Sales Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.markdown("---")



st.markdown("""
    <style>
    /* Main title */
    .main-title {
        text-align: center;
        color: #fff;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        padding: 1.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Section headers */
    .section-header {
        color: #764ba2;
        border-bottom: 3px solid #764ba2;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
        font-weight: 600;
            
    }
    
    /* Sub headers */
    .sub-header {
        color: #667eea;
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 1.5rem 1rem;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        color: #fff;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #667eea;
        padding: 10px;
        background-color: #f8f9fa;
            
        
    }
    
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #667eea;
        padding: 10px;
        background-color: #f8f9fa;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #667eea;
        background-color: #f8f9fa;
        color: #333;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e6e9ef;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .metric-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Success messages */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #155724;
    }
    
    /* Warning messages */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #856404;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    /* Plot styling */
    .stPlot {
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar slider */
    .stSlider>div>div>div>div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar selectbox */
    .stSelectbox>div>div>div {
        background-color: #f8f9fa;
    }
    
    /* Custom card for prediction results */
    .prediction-card {
        background: linear-gradient(135deg, #e6f7ff 0%, #b3e0ff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .prediction-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #0066cc;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .prediction-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #004d99;
        text-align: center;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
    
            
    /* النصوص جوه الـ selectbox */
    .stSelectbox div[data-baseweb="select"] * {
        color: #212529 !important;   /* لون غامق */
    }
        </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📊 MultiOutput Sales Prediction App</h1>', unsafe_allow_html=True)

if 'df' in st.session_state:
    df = st.session_state['df']
    
    st.markdown("""
    <div class="success-box">
        ✅ <strong>File loaded successfully!</strong> Dataset shape: {} rows × {} columns
    </div>
    """.format(df.shape[0], df.shape[1]), unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
    rows_to_show = st.slider('Choose number of rows to display:', min_value=5, max_value=min(100, df.shape[0]), value=10)
    st.dataframe(df.iloc[:rows_to_show], width='stretch')
    
    st.markdown('<h2 class="section-header">Data Processing</h2>', unsafe_allow_html=True)
    
    with st.expander("View Processing Steps"):
        st.write("1. Selecting relevant columns for the model")
        st.write("2. Converting distribution column to numeric values")
        st.write("3. Encoding categorical variables")
        st.write("4. Handling outliers with winsorization")
        st.write("5. Splitting data into training and test sets")
        st.write("6. Scaling features for better model performance")
    
    df_model = df[['Ship Mode', 'Discount', 'Segment', 'Category', 'Sub-Category',
                   'Quantity', 'Product ID', 'distribution', 'Sales', 'Cost', 'Profit']].copy()

    df_model['distribution'] = df_model['distribution'].astype(str).str.extract('(\d+)').astype(int)

    categorical_cols = df_model.select_dtypes(include=['object', 'string']).columns.tolist()
    
    encoding_progress = st.progress(0)
    status_text = st.empty()
    
    encoders = {}
    for i, col in enumerate(categorical_cols):
        status_text.text(f"Encoding {col}...")
        enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        df_model[[col]] = enc.fit_transform(df_model[[col]])
        encoders[col] = enc
        encoding_progress.progress((i + 1) / len(categorical_cols))
    
    status_text.text("Encoding completed!")
    encoding_progress.empty()
    
    winsorize_progress = st.progress(0)
    status_text.text("Handling outliers with winsorization...")
    
    for i, col in enumerate(['Sales', 'Cost', 'Profit']):
        df_model[col+'_capped'] = winsorize(df_model[col], limits=[0.01,0.01])
        winsorize_progress.progress((i + 1) / 3)
    
    df = pd.concat([df, df_model[['Sales_capped','Cost_capped','Profit_capped']]], axis=1)
    winsorize_progress.empty()
    status_text.text("Outlier handling completed!")

    X = df_model.drop(['Sales', 'Cost', 'Profit', 'distribution', 'Sales_capped', 'Cost_capped', 'Profit_capped'], axis=1)    
    y = df_model[['Sales','Cost' ,'Profit','distribution']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    st.markdown('<h2 class="section-header">Model Training</h2>', unsafe_allow_html=True)
    
    if 'multi_rf' not in st.session_state:
        with st.spinner('Training the MultiOutput Random Forest model... This may take a few moments.'):
            rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
            multi_rf = MultiOutputRegressor(rf, n_jobs=-1)
            multi_rf.fit(X_train_scaled, y_train)
            st.session_state['multi_rf'] = multi_rf
            st.session_state['scaler'] = scaler
            st.session_state['encoders'] = encoders.copy()
            
            st.markdown("""
            <div class="success-box">
                ✅ <strong>Model trained successfully!</strong> Ready for predictions.
            </div>
            """, unsafe_allow_html=True)
    else:
        multi_rf = st.session_state['multi_rf']
        scaler = st.session_state['scaler']
        encoders = st.session_state['encoders']
        
        st.markdown("""
        <div class="info-box">
            ℹ️ <strong>Using pre-trained model</strong> from session state.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">Feature Importance</h2>', unsafe_allow_html=True)
    
    features = X.columns
    outputs = y.columns
    
    importance_tabs = st.tabs([f"{col} Importance" for col in outputs])
    
    for i, tab in enumerate(importance_tabs):
        with tab:
            model = multi_rf.estimators_[i]
            importance = model.feature_importances_
            sorted_idx = np.argsort(importance)
            
            fig = go.Figure(go.Bar(
                x=importance[sorted_idx],
                y=np.array(features)[sorted_idx],
                orientation='h',
                marker_color='#667eea'
            ))
            
            fig.update_layout(
                title=f'Feature Importance for {outputs[i]}',
                xaxis_title='Importance',
                yaxis_title='Features',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, width='stretch')
    
    st.markdown('<h2 class="section-header">Make Predictions</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<h3 class="sub-header">Input Features</h3>', unsafe_allow_html=True)
        
        if 'input_values' not in st.session_state:
            st.session_state['input_values'] = {}
        
        input_dict = {}
        for col in X.columns:
            if col in categorical_cols:
                options = df[col].unique().tolist()
                if col not in st.session_state['input_values']:
                    st.session_state['input_values'][col] = options[0]
                
                if col == 'Sub-Category':
                    options = df[df['Category'] == st.session_state['input_values']['Category']]['Sub-Category'].unique().tolist()
                    
                    if st.session_state['input_values'].get(col) not in options:
                        st.session_state['input_values'][col] = options[0]

                    input_val = st.selectbox(
                        col,
                        options=options,
                        index=options.index(st.session_state['input_values'][col])
                    )
                
                elif col == 'Product ID':
                    options = df[df['Sub-Category'] == st.session_state['input_values']['Sub-Category']]['Product ID'].unique().tolist()
                    
                    if st.session_state['input_values'].get(col) not in options:
                        st.session_state['input_values'][col] = options[0]

                    input_val = st.selectbox(
                        col,
                        options=options,
                        index=options.index(st.session_state['input_values'][col])
                    )
                
                else:
                    if st.session_state['input_values'].get(col) not in options:
                        st.session_state['input_values'][col] = options[0]

                    input_val = st.selectbox(
                        col,
                        options=options,
                        index=options.index(st.session_state['input_values'][col])
                    )
                
                st.session_state['input_values'][col] = input_val
                
                input_val_encoded = encoders[col].transform([[input_val]])[0][0]
                input_dict[col] = [input_val_encoded]

            elif col == "Quantity":
                input_val = st.number_input(
                    col,
                    min_value=int(df[col].min()),
                    max_value=int(df[col].max()),
                    value=int(df[col].median()),
                    step=1
                )
                input_dict[col] = [input_val]

            
            elif col not in ['Sales_capped','Cost_capped','Profit_capped']:
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                default_val = float(df[col].median())
                
                if col not in st.session_state['input_values']:
                    st.session_state['input_values'][col] = default_val
                
                current_value = float(st.session_state['input_values'][col])
                
                input_val = st.slider(
                    col,
                    min_value=float(min_val),
                    max_value=float(max_val),
                    value=float(current_value),
                    step=float((max_val - min_val) / 100) if (max_val - min_val) > 0 else 0.1
                )
                input_dict[col] = [input_val]
            
            else:
                input_dict[col] = [float(df[col].iloc[0])]
            
            if col not in ['Sales_capped','Cost_capped','Profit_capped']:
                if col in categorical_cols:
                    st.session_state['input_values'][col] = input_val
                else:
                    st.session_state['input_values'][col] = float(input_dict[col][0])
    
    with col2:
        st.markdown('<h3 class="sub-header">Prediction Results</h3>', unsafe_allow_html=True)
        
        if st.button("🚀 Predict Sales, Cost, Profit & Distribution", width='stretch'):
            input_df = pd.DataFrame(input_dict)
            input_scaled = st.session_state['scaler'].transform(input_df)
            pred = st.session_state['multi_rf'].predict(input_scaled)
            pred_df = pd.DataFrame(pred, columns=outputs)
            pred_df['Profit'] = pred_df['Sales']-pred_df['Cost']
            
            st.markdown("""
            <div class="success-box">
                ✅ <strong>Prediction completed successfully!</strong>
            </div>
            """, unsafe_allow_html=True)
            
            pred_col1, pred_col2, pred_col3, pred_col4 = st.columns(4)
            
            with pred_col1:
                st.markdown('<div class="prediction-card"><div class="prediction-header">Sales</div><div class="prediction-value">${:,.2f}</div></div>'.format(pred_df['Sales'].iloc[0]), unsafe_allow_html=True)
            
            with pred_col2:
                st.markdown('<div class="prediction-card"><div class="prediction-header">Cost</div><div class="prediction-value">${:,.2f}</div></div>'.format(pred_df['Cost'].iloc[0]), unsafe_allow_html=True)
            
            with pred_col3:
                st.markdown('<div class="prediction-card"><div class="prediction-header">Profit</div><div class="prediction-value">${:,.2f}</div></div>'.format(pred_df['Profit'].iloc[0]), unsafe_allow_html=True)
            
            with pred_col4:
                st.markdown('<div class="prediction-card"><div class="prediction-header">Distribution</div><div class="prediction-value">{:,.0f}</div></div>'.format(pred_df['distribution'].iloc[0]), unsafe_allow_html=True)
            
            with st.expander("View Detailed Prediction Results"):
                st.dataframe(pred_df, width='stretch')
        
        st.markdown("""
        <div class="info-box">
            ℹ️ <strong>Model Information:</strong> MultiOutput Random Forest with 200 estimators per output.
            Trained on {} samples with {} features.
        </div>
        """.format(X_train.shape[0], X_train.shape[1]), unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>No dataset found!</strong> Please upload a file in the Data Frame section first.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <hr>
    <p>MultiOutput Sales Prediction App • Powered by Scikit-learn and Streamlit</p>
</div>
""", unsafe_allow_html=True)
