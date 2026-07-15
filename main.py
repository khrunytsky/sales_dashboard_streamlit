import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from city_coords import CITY_COORDS

# KONFIGURACJA STRONY
#-----------------------------------------------------------------------------
st.set_page_config(
    page_title="Adidas USA - Sales Performance Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ŁADOWANIE DANYCH
#-----------------------------------------------------------------------------
@st.cache_data

def load_data():
    file_path = 'Adidas US Sales Datasets.xlsx'
    df = pd.read_excel(file_path, sheet_name='Data Sales Adidas', skiprows=4)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
    df['Year'] = df['Invoice Date'].dt.year
    df['Month_Year'] = df['Invoice Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# PANEL BOCZNY
#-----------------------------------------------------------------------------
st.sidebar.header("🔍 Filtry Dashboardu")
st.sidebar.caption("Zostaw puste pole, aby wyświetlić wszystko.")

selected_years = st.sidebar.multiselect("Rok:", sorted(df['Year'].unique()))
selected_methods = st.sidebar.multiselect("Metoda Sprzedaży:", df['Sales Method'].unique())
selected_retailer = st.sidebar.multiselect("Retailer:", df['Retailer'].unique())

if not selected_methods: selected_methods = df['Sales Method'].unique()
if not selected_years: selected_years = df['Year'].unique()
if not selected_retailer: selected_retailer = df['Retailer'].unique()


filtered_df = df[
    (df['Sales Method'].isin(selected_methods)) &
    (df['Year'].isin(selected_years)) &
    (df['Retailer'].isin(selected_retailer))
]


# NAGŁÓWEK I KPI
#-----------------------------------------------------------------------------
st.title(" Adidas USA – Dashboard")

"---"

total_sales = filtered_df['Total Sales'].sum()
total_profit = filtered_df['Operating Profit'].sum()
total_units = filtered_df['Units Sold'].sum()
avg_margin = filtered_df['Operating Margin'].mean() * 100 if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Całkowity Przychód", value=f"${total_sales/1e6:,.2f} M")
with col2:
    st.metric(label="Zysk Operacyjny", value=f"${total_profit/1e6:,.2f} M")
with col3:
    st.metric(label="Sprzedane Sztuki", value=f"{total_units:,.0f}")
with col4:
    st.metric(label="Średnia Marża", value=f"{avg_margin:.1f}%")

"---"


# WIERSZ 1: Wykres Liniowy + Wykres Donut
# -----------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("Dynamika Przychodu i Zysku w Czasie")
    monthly_trend = filtered_df.groupby('Month_Year')[['Total Sales', 'Operating Profit']].sum().reset_index()
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=monthly_trend['Month_Year'], y=monthly_trend['Total Sales']/1e6,
        mode='lines+markers', name='Przychód ($M)',
        line=dict(color='#0066CC', width=3), marker=dict(size=7)
    ))
    fig_line.add_trace(go.Scatter(
        x=monthly_trend['Month_Year'], y=monthly_trend['Operating Profit']/1e6,
        mode='lines+markers', name='Zysk ($M)',
        line=dict(color='#00CC66', width=3), marker=dict(size=7)
    ))
    fig_line.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_line)

with row1_col2:
    st.subheader("Udział Metod Sprzedaży")
    method_sales = filtered_df.groupby('Sales Method')['Total Sales'].sum().reset_index()
    
    fig_donut = px.pie(
        method_sales, values='Total Sales', names='Sales Method',
        hole=0.5,
        color_discrete_sequence=['#00529B', '#3399FF', '#80E5FF']
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_donut)

"---"


# WIERSZ 2: Bubble Map
#-----------------------------------------------------------------------------
st.subheader("Mapa Przychodu wg Miast (Wielkość bąbelka = Przychód)")

city_df = filtered_df.groupby('City')['Total Sales'].sum().reset_index()
city_df['lat'] = city_df['City'].map(lambda x: CITY_COORDS.get(x, (None, None))[0])
city_df['lon'] = city_df['City'].map(lambda x: CITY_COORDS.get(x, (None, None))[1])
city_df = city_df.dropna(subset=['lat', 'lon'])
city_df['Przychód ($M)'] = city_df['Total Sales'] / 1e6

fig_geo = px.scatter_geo(
    city_df,
    lat="lat",
    lon="lon",
    size="Przychód ($M)",
    color="Przychód ($M)",
    hover_name="City",
    size_max=35,
    scope="usa",
    color_continuous_scale="Blues"
)
fig_geo.update_traces(
    marker=dict(line=dict(width=1, color='DarkSlateGrey'))
)
fig_geo.update_layout(
    template="plotly_white",
    margin=dict(l=0, r=0, t=10, b=0),
    coloraxis_colorbar=dict(title="Przychód ($M)"),
    autosize=True
)

st.plotly_chart(fig_geo, use_container_width=True)

"---"

# WIERSZ 3: Przychody wg Kategorii i Regionów
#-----------------------------------------------------------------------------
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("Przychody wg Kategorii Produktów")
    product_sales = filtered_df.groupby('Product')['Total Sales'].sum().reset_index().sort_values(by='Total Sales', ascending=True)
    product_sales['Total Sales ($M)'] = product_sales['Total Sales'] / 1e6
    
    fig_bar_prod = px.bar(
        product_sales, x='Total Sales ($M)', y='Product',
        orientation='h',
        text_auto='.1f',
        color_discrete_sequence=['#0066CC']
    )
    fig_bar_prod.update_layout(
        template="plotly_white",
        xaxis_title="Przychód w mln USD", yaxis_title="",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar_prod)

with row3_col2:
    st.subheader("Przychody wg Regionów")
    region_sales = filtered_df.groupby('Region')['Total Sales'].sum().reset_index().sort_values(by='Total Sales', ascending=False)
    region_sales['Total Sales ($M)'] = region_sales['Total Sales'] / 1e6
    
    fig_bar_reg = px.bar(
        region_sales, x='Region', y='Total Sales ($M)',
        text_auto='.1f',
        color='Total Sales ($M)',
        color_continuous_scale='Blues'
    )
    fig_bar_reg.update_layout(
        template="plotly_white",
        coloraxis_showscale=False,
        xaxis_title="Region", yaxis_title="Przychód w mln USD",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar_reg)