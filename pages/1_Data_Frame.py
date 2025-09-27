import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import random as rd
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import base64
import base64
import streamlit as st






def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    image_base64 = get_base64_image("ahmed_sarhan.jpg")
except FileNotFoundError:
    st.error("صورة الملف الشخصي (ahmed_sarhan.jpg) غير موجودة. يرجى التأكد من أنها في نفس مجلد التطبيق.")
    st.stop()


with st.container():
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown('<div class="profile-image"></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="profile-text">
                <h2>Ahmed Sarhan</h2>
                <p><strong>Data Analyst</strong></p>
                <p>Faculty of Computer and Data Science</p>
                <div class="social-links">
                    <a href="https://www.linkedin.com/in/your-linkedin-profile" target="_blank">
                        <i class="fab fa-linkedin fa-2x"></i>
                    </a>
                    <a href="https://github.com/your-github-profile" target="_blank">
                        <i class="fab fa-github fa-2x"></i>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown(f"""
<style>
.profile-container {{
    background: linear-gradient(135deg, #2c3a50, #1f2735);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    border: 1px solid #3d4a60;
}}
.profile-image {{
    width: 150px;
    height: 150px;
    background-image: url(data:image/jpeg;base64,{image_base64});
    background-size: cover;
    background-position: center;
    border-radius: 50%;
    border: 4px solid #00c6ff;
    box-shadow: 0 0 15px rgba(0, 198, 255, 0.5);
}}
.profile-text {{
    margin-left: 20px;
    color: #f0f2f6;
}}
.profile-text h2 {{
    font-size: 2rem;
    font-weight: 700;
    color: #f0f2f6;
    margin: 0;
}}
.profile-text p {{
    font-size: 1rem;
    margin: 0;
    color: #a0a0a0;
}}
.social-links {{
    margin-top: 15px;
}}
.social-links a {{
    color: #00c6ff;
    margin-right: 15px;
    transition: color 0.3s;
}}
.social-links a:hover {{
    color: #0072ff;
}}
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Title */
    h1 {
        text-align: center;
        color: #fff;
        font-size: 48px !important;
        text-shadow: 2px 2px 5px #000;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141e30, #243b55);
        color: white;
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
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 10px rgba(255,75,43,0.6);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: bold;
        color: #333;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #ff4b2b;
        color: #ff4b2b;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def data_load(file):
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
        return df
    
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
        return df
    
    elif file.name.endswith('.pkl'):
        df = pd.read_pickle(file)
        return df


select_order = st.sidebar.selectbox('select' ,['Show Data Frame' , 'Visualization'])


if select_order == 'Show Data Frame' :
    file = st.file_uploader('Upload file' , type=['xlsx' , 'csv' , 'pkl'])

    if file is not None :
        st.session_state['df'] = data_load(file=file)

    
    
    if 'df' in st.session_state:

        df = st.session_state['df']

        if 'columns_remove_btn' not in st.session_state:
            st.session_state['columns_remove_btn'] = False


        if 'columns_selected' not in st.session_state:
            st.session_state['columns_selected'] = df.columns.tolist()

        if (st.session_state['columns_selected'] != df.columns.tolist()) and not( st.session_state['columns_remove_btn']):
            st.session_state['columns_selected'] = df.columns.tolist()


        st.session_state['columns_selected'] = st.multiselect(
            'Select columns to show:',
            options=df.columns.tolist(),
            default=st.session_state['columns_selected']
        )

        col_5 , col_6 = st.columns(2)
        
        with col_5:
            if st.button('Remove all columns'):
                st.session_state['columns_selected'] = []
                st.session_state['columns_remove_btn'] = True
                st.rerun()

        with col_6:
            if st.button('Return all columns'):
                st.session_state['columns_selected'] = df.columns.tolist()
                st.session_state['columns_remove_btn'] = False
                st.rerun()


        rows_to_show = st.slider('Choose number of rows to display :' , min_value=5 ,
                    max_value=df.shape[0])
        
        st.dataframe(df.loc[:rows_to_show, st.session_state['columns_selected']])
        
elif select_order == 'Visualization':


    if 'df' in st.session_state:
        df = st.session_state['df']


        columns_numirec = df.select_dtypes('number').columns.tolist()

        tab_Dynamic_vis , tab_Static_vis = st.tabs(['Dynamic Visualization' , 'Static Visualization'])

        
        with tab_Dynamic_vis:
            
            tab_1,tap_2 = st.tabs(tabs = ['Scatter' ,'Histogram'])

            with tab_1:

                col_1,col_2 = st.columns(2)
                col_3,col_4 = st.columns(2)
                
                with col_1:
                    axis_x_scatt = st.selectbox('Select column to be axis \'x\' for scatter' , options=columns_numirec)
                with col_2:
                    color_scatt = st.selectbox('Select column to be color for scatter' , options=columns_numirec)
                with col_3:
                    size_scatt = st.selectbox('Select column to be size for scatter' , options=columns_numirec)
                with col_4:
                    color_map = st.selectbox('Color Maps Style' , options=['plasma', 'rainbow' , 'viridis'])


                size_over = st.selectbox('Size of colomn' , options=[20,40,10])


                try:
                    fig_scatter = px.scatter(
                    df ,
                    axis_x_scatt ,
                    color=color_scatt ,
                    size=size_scatt ,
                    size_max=size_over,
                    color_continuous_scale=color_map
                    )
                        
                    fig_scatter.update_layout(
                        yaxis_title = 'Count'
                    )

                    st.plotly_chart(fig_scatter)

                except:
                    st.warning('Size cannot be negative.')
                    
                    st.warning(f'{size_scatt} : Have a negative value.')
            
            with tap_2:

                axis_x_hist = st.selectbox('Select column to be axis \'x\' for histogram' , options=columns_numirec)

                fig_histogram = px.histogram(df , axis_x_hist )
                st.plotly_chart(fig_histogram)

        
        with tab_Static_vis:
            tap_plotly , tap_matplotlib= st.tabs(['Show by Plotly' , 'Show by Matplotlib'])


            with tap_plotly:
                tab_plotly1 , tab_plotly2 , tab_plotly3 ,tab_plotly4 ,tab_plotly5 ,tab_plotly6 = st.tabs([
                                                                                                "Category Analysis",
                                                                                                "Sub-Category Analysis",
                                                                                                "State sales",
                                                                                                "Customer sales",
                                                                                                "Company Computing",
                                                                                                "Company Productivity"
                                                                                            ])


                with tab_plotly1:
                    
                    Category_sales = df.groupby("Category")["Sales"].sum().reset_index()
                    Category_cost = df.groupby("Category")["Cost"].sum().reset_index()
                    category_counts = df["Category"].value_counts().reset_index()
                    category_counts.columns = ["Category", "Counts"]
                    Category_profit = df.groupby("Category")["Profit"].sum().reset_index()
                    Category_computing = df.groupby("Category")[["Sales", "Cost", "Profit"]].sum().reset_index()

                   
                    st.subheader("Category Analysis")

                    col1, col2 = st.columns(2)
                    with col1:
                        fig1 = px.bar(Category_sales, x="Category", y="Sales", color="Category",
                                    title="Category Vs Sales")
                        st.plotly_chart(fig1, width='stretch', key="fig1")

                    with col2:
                        fig2 = px.bar(category_counts, x="Category", y="Counts", color="Category",
                                    title="Category Vs Counts")
                        st.plotly_chart(fig2, width='stretch', key="fig2")

                    col3, col4 = st.columns(2)
                    with col3:
                        fig3 = px.bar(Category_cost, x="Category", y="Cost", color="Category",
                                    title="Category Vs Cost")
                        st.plotly_chart(fig3, width='stretch', key="fig3")

                    with col4:
                        fig4 = px.bar(Category_profit, x="Category", y="Profit", color="Category",
                                    title="Category Vs Profit")
                        st.plotly_chart(fig4,width='stretch', key="fig4")

                    
                    st.title('='*30)
                    

                    col5, col6 = st.columns(2)
                    with col5:
                        fig5 = px.bar(
                            Category_computing,
                            x="Category",
                            y=["Sales", "Cost", "Profit"],
                            barmode="group",
                            title="Sales Vs Cost Vs Profit"
                        )
                        st.plotly_chart(fig5, width='stretch', key="fig5")

                    with col6:
                        fig6 = px.bar(
                            category_counts,
                            x="Category",
                            y="Counts",
                            color="Category",
                            title="Category Vs Counts"
                        )
                        st.plotly_chart(fig6, width='stretch', key="fig6")

                with tab_plotly2:

                    st.subheader("Sub-Category Analysis")

                    
                    technology = df[df['Category'] == 'Technology']
                    Technology_Sub_Category = (
                        technology.groupby('Sub-Category')['Sales']
                        .sum()
                        .reset_index()
                        .sort_values('Sales', ascending=False)
                    )

                    Furniture = df[df['Category'] == 'Furniture']
                    Furniture_Sub_Category = (
                        Furniture.groupby('Sub-Category')['Sales']
                        .sum()
                        .reset_index()
                        .sort_values('Sales', ascending=False)
                    )

                    Office_Supplies = df[df['Category'] == 'Office Supplies']
                    Office_Supplies_Sub_Category = (
                        Office_Supplies.groupby('Sub-Category')['Sales']
                        .sum()
                        .reset_index()
                        .sort_values('Sales', ascending=False)
                    )

                    Office_Supplies_Sub_Category_pie = (
                        Office_Supplies.groupby('Sub-Category')['Sales']
                        .sum()
                        .reset_index()
                        .sort_values('Sales', ascending=False)
                        .head(6)
                    )

                    
                    col1, col2 = st.columns(2)

                   
                    with col1:
                        fig1 = px.pie(
                            Technology_Sub_Category,
                            names="Sub-Category",
                            values="Sales",
                            title="Technology Sub Category",
                            hole=0.3
                        )
                        st.plotly_chart(fig1,width='stretch', key="pie1")

                    with col2:
                        fig2 = px.pie(
                            Furniture_Sub_Category,
                            names="Sub-Category",
                            values="Sales",
                            title="Furniture Sub Category",
                            hole=0.3
                        )
                        st.plotly_chart(fig2, width='stretch', key="pie2")

                    
                    fig3 = px.pie(
                        Office_Supplies_Sub_Category_pie,
                        names="Sub-Category",
                        values="Sales",
                        title="Top 6 Office Supplies Sub Category",
                        hole=0.3
                    )
                    st.plotly_chart(fig3,width='stretch', key="pie3")

                   
                    fig4 = px.bar(
                        Technology_Sub_Category,
                        x="Sub-Category",
                        y="Sales",
                        color="Sub-Category",
                        title="Technology Sub Category Sales"
                    )
                    fig4.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig4, width='stretch', key="bar1")

                    
                    col5, col6 = st.columns(2)


                    with col5:
                        fig5 = px.bar(
                            Furniture_Sub_Category,
                            x="Sub-Category",
                            y="Sales",
                            color="Sub-Category",
                            title="Furniture Sub Category Sales"
                        )
                        fig5.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig5, width='stretch', key="bar2")

                    with col6:
                        fig6 = px.bar(
                            Office_Supplies_Sub_Category,
                            x="Sub-Category",
                            y="Sales",
                            color="Sub-Category",
                            title="Office Supplies Sub Category Sales"
                        )
                        fig6.update_layout(xaxis_tickangle=45)
                        st.plotly_chart(fig6,width='stretch', key="bar3")
                

                with tab_plotly3:
                    st.subheader("Top 20 State sales")

                    Top_20_State_sales = df.groupby(['State'])['Sales'].sum().sort_values(ascending=False).head(20)

                    fig = px.bar(
                        Top_20_State_sales,
                        x=Top_20_State_sales.index,
                        y="Sales",
                        color="Sales",
                        color_continuous_scale="Blues",
                        title="Top 20 State Sales"
                    )
                    fig.update_layout(
                        xaxis_title="State",
                        yaxis_title="Sales",
                        title_font=dict(size=20),
                        xaxis_tickangle=50
                    )
                    st.plotly_chart(fig,width='stretch')


                with tab_plotly4:
                    st.subheader("Top 10 Customer sales")

                    profit = (
                        df.groupby(['Customer Name', 'Segment', 'Discount'])[['Sales', 'Cost', 'Profit']]
                        .sum()
                        .sort_values(by='Sales', ascending=False)
                        .head(10)
                    ).reset_index()

                    fig = go.Figure()
                    fig.add_bar(x=profit['Customer Name'], y=profit['Sales'], name="Sales", marker_color='blue')
                    fig.add_bar(x=profit['Customer Name'], y=profit['Cost'], name="Cost", marker_color='red')
                    fig.add_bar(x=profit['Customer Name'], y=profit['Profit'], name="Profit", marker_color='green')

                    fig.update_layout(
                        barmode='group',
                        xaxis_tickangle=25,
                        title="Sales Vs Profit Vs Discount (Top 10 Customers)",
                        title_font=dict(size=25),
                        xaxis_title="Customer Name , Segment , Discount",
                        yaxis_title="Values",
                        legend=dict(x=0, y=1.2, orientation="h")
                    )
                    st.plotly_chart(fig,width='stretch')


                with tab_plotly5:
                    st.subheader('Company computing')

                    company_computing = df[['Sales', 'Cost', 'Profit']].sum()

                    fig = px.bar(
                        x=company_computing.index,
                        y=company_computing.values,
                        color=company_computing.index,
                        text=company_computing.values,
                        title="Sales Vs Cost Vs Profit (Company computing)",
                        color_discrete_map={"Sales": "blue", "Cost": "red", "Profit": "green"}
                    )
                    fig.update_layout(
                        yaxis_title="Values",
                        xaxis_tickangle=45,
                        title_font=dict(size=25)
                    )
                    st.plotly_chart(fig,width='stretch')


                with tab_plotly6:
                    st.subheader('Company Productivity')

                    Company_Productivity = df[['Profit', 'Cost', 'Sales']].agg(['min', 'mean', 'max']).reset_index()
                    Company_Productivity.rename(columns={'index': 'Metric'}, inplace=True)

                    fig = make_subplots(rows=1, cols=3, subplot_titles=("Sales", "Cost", "Profit"))

                    fig.add_trace(go.Scatter(
                        x=Company_Productivity['Metric'],
                        y=Company_Productivity['Sales'],
                        mode="lines+markers",
                        line=dict(color="blue", dash="dash"),
                        name="Sales"
                    ), row=1, col=1)

                    fig.add_trace(go.Scatter(
                        x=Company_Productivity['Metric'],
                        y=Company_Productivity['Cost'],
                        mode="lines+markers",
                        line=dict(color="red", dash="dash"),
                        name="Cost"
                    ), row=1, col=2)

                    fig.add_trace(go.Scatter(
                        x=Company_Productivity['Metric'],
                        y=Company_Productivity['Profit'],
                        mode="lines+markers",
                        line=dict(color="green", dash="dash"),
                        name="Profit"
                    ), row=1, col=3)

                    fig.update_layout(title_text="Company Productivity (Min / Mean / Max)", title_font=dict(size=20))
                    st.plotly_chart(fig,width='stretch')

                    fig_zoom = px.line(
                        Company_Productivity,
                        x="Metric",
                        y=["Sales", "Cost", "Profit"],
                        markers=True,
                        title="Zoomed Company Productivity"
                    )
                    fig_zoom.update_traces(line=dict(dash="dash"))
                    fig_zoom.update_layout(yaxis=dict(range=[-4000, 20000]))
                    st.plotly_chart(fig_zoom,width='stretch')



            with tap_matplotlib:
                
                tab_matp1 , tab_matp2 , tab_matp3 ,tab_matp4 ,tab_matp5 ,tab_matp6 = st.tabs([
                                                                                                "Category Analysis",
                                                                                                "Sub-Category Analysis",
                                                                                                "State sales",
                                                                                                "Customer sales",
                                                                                                "Company Computing",
                                                                                                "Company Productivity"
                                                                                            ])
                


                with tab_matp1:
                    
                    st.subheader("Category Analysis")

                    category_counts = df['Category'].value_counts()
                    Category_sales = df.groupby('Category')['Sales'].sum()
                    Category_cost= df.groupby('Category')['Cost'].sum()
                    Category_profit = df.groupby('Category')['Profit'].sum()
                    Category_computing = df.groupby('Category')[['Sales','Cost','Profit']].sum()


                    fig_bars,ax = plt.subplots(2,2 , figsize=(12,7))
                    Category_sales.plot(
                        kind='bar',
                        edgecolor = 'black',
                        color = ['g' , 'b' , 'r'],
                        ax=ax[0][0]
                    )

                    category_counts.plot(
                        kind='bar' , 
                        edgecolor = 'black' , 
                        color = ['b' , 'g' , 'r'] , 
                        ax= ax[0][1]
                    )

                    Category_cost.plot(
                        kind='bar' ,
                        edgecolor = 'black' , 
                        color = ['g' , 'b' , 'r'] ,
                        ax = ax[1][0]
                    )

                    Category_profit.plot(
                        kind='bar' ,
                        edgecolor = 'black' , 
                        color = ['g' , 'b' , 'r'] ,
                        ax = ax[1][1]
                    )


                    ax[0][0].set_xlabel('Category' , fontsize = 15)
                    ax[0][0].set_ylabel('Sales' , fontsize = 15)
                    ax[0][0].set_title('Category Vs Sales' , fontsize = 25 , pad = 20)
                    ax[0][0].tick_params(axis = 'x', rotation=20)

                    ax[0][1].set_xlabel('Category' , fontsize = 15)
                    ax[0][1].set_ylabel('Counts' , fontsize = 15)
                    ax[0][1].set_title('Category Vs Counts' , fontsize = 25 ,pad = 20)
                    ax[0][1].tick_params(axis = 'x', rotation=20)

                    ax[1][0].set_xlabel('Category' , fontsize = 15)
                    ax[1][0].set_ylabel('Cost' , fontsize = 15)
                    ax[1][0].set_title('Category Vs Cost' , fontsize = 25 , pad = 20)
                    ax[1][0].tick_params(axis = 'x', rotation=20)

                    ax[1][1].set_xlabel('Category' , fontsize = 15)
                    ax[1][1].set_ylabel('Profit' , fontsize = 15)
                    ax[1][1].set_title('Category Vs Profit' , fontsize = 25  , pad = 20)
                    ax[1][1].tick_params(axis = 'x', rotation=20)


                    plt.tight_layout()
                    st.pyplot(fig_bars)


                    fig_bars,ax = plt.subplots(1,2 , figsize=(12,6))
                    Category_computing[['Sales','Cost','Profit']].plot(kind='bar' , ax=ax[0],
                        edgecolor = 'black',
                        color = ['r' , 'g' , 'b']
                    )

                    ax[1].bar(
                        x = category_counts.index ,
                        height = category_counts.values ,
                        edgecolor = 'black' , 
                        color = ['b' , 'g' , 'r']
                    )


                    ax[0].set_xlabel('Category' , fontsize = 15)
                    ax[0].set_ylabel('Money' , fontsize = 15)
                    ax[0].set_title('Sales Vs Cost Vs Profit' , fontsize = 25 , pad = 20)
                    ax[0].tick_params(axis = 'x', rotation=20)

                    ax[1].set_xlabel('Category' , fontsize = 15)
                    ax[1].set_ylabel('Counts' , fontsize = 15)
                    ax[1].set_title('Category Vs Counts' , fontsize = 25 , pad = 20)


                    plt.tight_layout()
                    st.pyplot(fig_bars)



                with tab_matp2:
                    st.subheader("Sub-Category Analysis")

                    

                    technology = df[df['Category']=='Technology']
                    Technology_Sub_Category = technology.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)

                    Furniture = df[df['Category']=='Furniture']
                    Furniture_Sub_Category = Furniture.groupby(['Sub-Category'])['Sales'].sum().sort_values(ascending=False)
                    
                    Office_Supplies	= df[df['Category']=='Office Supplies']
                    Office_Supplies_Sub_Category = Office_Supplies.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)
                    
                    Office_Supplies_Sub_Category_pie = Office_Supplies.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(6)
                    

                    explode_len = [.17 for i in Office_Supplies_Sub_Category_pie.index]

                    
                    fig_pies,ax = plt.subplots(1,3,figsize = (13,5))

                    Technology_Sub_Category.plot(
                        kind='pie' ,
                        ylabel='' ,
                        autopct='%1.1f%%' ,
                        shadow = True ,
                        startangle = 0 ,
                        explode = [.05 ,.05,.05,.05] ,
                        wedgeprops = {'edgecolor' :'black'} ,
                        ax=ax[0]
                    )

                    Furniture_Sub_Category.plot(
                    kind='pie' ,
                    ylabel='',
                    autopct = '%1.2f%%' ,
                    shadow = True ,
                    startangle = 0 ,
                    explode = [.05 ,.05,.05,.05] ,
                    wedgeprops = {'edgecolor' :'black'} ,
                    ax = ax[1]
                    )

                    Office_Supplies_Sub_Category_pie.plot(
                        kind='pie' ,
                        ylabel='' ,
                        autopct='%1.1f%%' ,
                        shadow = True ,
                        startangle = 90 ,
                        explode = explode_len ,
                        wedgeprops = {'edgecolor' :'black'} ,
                        labeldistance = 1.2,
                        ax=ax[2]
                    )

                    ax[0].set_title('Technology Sub Category' , fontsize = 20  ,pad = 30)
                    ax[1].set_title('Furniture Sub Category' , fontsize = 20  ,pad = 30)
                    ax[2].set_title('Office Supplies Sub Category' , fontsize = 20 ,pad = 30)

                    plt.tight_layout()
                    st.pyplot(fig_pies)


                    fig_bars,ax = plt.subplots(1,3,figsize = (14,4))

                    Technology_Sub_Category.plot(
                        kind='bar' ,
                        edgecolor  ='black' ,
                        color = 'g',
                        ax=ax[0]
                    )

                    Furniture_Sub_Category.plot(
                        kind='bar' ,
                        edgecolor  ='black' ,
                        color = 'g',
                        ax = ax[1]
                    )

                    Office_Supplies_Sub_Category.plot(
                        kind='bar' ,
                        edgecolor  ='black' ,
                        color = 'g',
                        ax = ax[2]
                    )

                    ax[0].tick_params(axis = 'x' , rotation = 45)
                    ax[0].set_ylabel('Sales' , fontsize = 14)
                    ax[0].set_xlabel('Sub Category' , fontsize = 14)
                    ax[0].set_title('Technologys Sub Category' , fontsize = 20 , pad = 30)

                    ax[1].tick_params(axis = 'x' , rotation = 45)
                    ax[1].set_ylabel('Sales' , fontsize = 14)
                    ax[1].set_xlabel('Sub Category' , fontsize = 14)
                    ax[1].set_title('Furniture Sub Category' , fontsize = 20 , pad = 30)

                    ax[2].tick_params(axis = 'x' , rotation = 45)
                    ax[2].set_ylabel('Sales' , fontsize = 14)
                    ax[2].set_xlabel('Sub Category' , fontsize = 14)
                    ax[2].set_title('Office Supplies Sub Category' , fontsize = 20 , pad = 30)

                    plt.tight_layout()
                    st.pyplot(fig_bars)

                with tab_matp3:
                    st.subheader("Top 20 State sales")

                    Top_20_State_sales = df.groupby(['State'])['Sales'].sum().sort_values(ascending=False).head(20)

                    fig, ax = plt.subplots(figsize=(16,5))

                    Top_20_State_sales.plot(
                        kind='bar',
                        edgecolor='black',
                        color='b',
                        ax=ax
                    )

                    ax.set_xticklabels(ax.get_xticklabels(), rotation=50)
                    ax.set_xlabel('State', fontsize=15)
                    ax.set_ylabel('Sales', fontsize=15)

                    ax.legend()
                    ax.set_title('Top 20 State sales', fontsize=20)

                    st.pyplot(fig)

                with tab_matp4:
                    
                    st.subheader("Top 10 Customer sales")

                    profit = df.groupby(['Customer Name' , 'Segment' ,'Discount' ])[['Sales' , 'Cost' , 'Profit']].sum().sort_values(by = 'Sales' ,ascending=False).head(10)
                    
                    fig, ax = plt.subplots(figsize=(16,5))

                    profit.plot(
                    kind='bar' ,
                    figsize=(13 ,5)  ,
                    edgecolor = 'black' ,
                    color = ['b' , 'r' , 'g'],
                    ax = ax
                    )

                    ax.set_xticklabels(ax.get_xticklabels(),rotation = 25)
                    ax.set_ylabel('Sales' , fontsize = 15)
                    ax.set_xlabel('Customer Name , Segment , Discount' , fontsize = 15)

                    ax.set_title('Sales V.S Profit V.S Disconut' , fontsize = 25)
                    plt.legend( loc = 'upper left' , bbox_to_anchor = (-.1,1.2))
                    st.pyplot(fig)


                with tab_matp5:
                    fig, ax = plt.subplots(figsize=(16,5))

                    st.subheader('Company computing')

                    company_computing = df[['Sales', 'Cost' ,'Profit' ]].sum()

                    company_computing.plot(
                    kind='bar' ,
                    edgecolor = 'black' ,
                    color = ['blue', 'red'  , 'green'] ,
                    figsize=(12,5),
                    ax = ax
                    )

                    ax.set_ylabel('Sales' , fontsize = 15)
                    ax.set_title('Sales Vs Cost Vs Profit (Company computing)' , fontsize = 25 , pad=20)
                    ax.set_xticklabels(ax.get_xticklabels(),rotation = 45)

                    st.pyplot(fig)

                with tab_matp6:
                    st.subheader('Company_Productivity')

                    Company_Productivity = df[['Profit' ,'Cost' , 'Sales']].agg(['min' , 'mean' , 'max'])

                    fig , ax = plt.subplots(1,3,figsize=(10,3))

                    Company_Productivity['Sales'].plot(
                        ax=ax[0] ,
                        color ='b' ,
                        marker = 'o' ,
                        alpha = .5 ,
                        linestyle = '--'
                    )

                    Company_Productivity['Cost'].plot(
                        ax=ax[1] ,
                        color = 'r' ,
                        marker = 'o' ,
                        alpha = .5 ,
                        linestyle = '--'
                    )

                    Company_Productivity['Profit'].plot(
                        ax=ax[2] ,
                        color = 'g' ,
                        marker = 'o' ,
                        alpha = .5 ,
                        linestyle = '--'
                    )

                    ax[0].set_ylabel('Money' , fontsize = 13)
                    ax[0].set_title('Sales' , fontsize = 20)

                    ax[1].set_ylabel('Money' , fontsize = 13)
                    ax[1].set_title('Cost' , fontsize = 20)

                    ax[2].set_ylabel('Money' , fontsize = 13)
                    ax[2].set_title('Profit' , fontsize = 20)

                    plt.tight_layout()
                    st.pyplot(fig)

                    fig_zoom, ax_zoom = plt.subplots(figsize=(8,5))
                    Company_Productivity.plot(
                        ax=ax_zoom,
                        color=['g' , 'r' , 'b'],
                        alpha=1,
                        linestyle='--'
                    )
                    ax_zoom.set_ylim(-4000, 20000)
                    st.pyplot(fig_zoom)           


    else:
        st.warning('Upload File')