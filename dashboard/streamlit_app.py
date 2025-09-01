"""
AI Market Intelligence Dashboard
Interactive Streamlit dashboard for AI market analysis and predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="AI Market Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #3498db;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    try:
        data_dir = Path('../data/raw')
        
        # Load with encoding handling
        try:
            popularity_df = pd.read_csv(data_dir / 'AI_ML_popularity.csv', encoding='utf-8')
        except UnicodeDecodeError:
            popularity_df = pd.read_csv(data_dir / 'AI_ML_popularity.csv', encoding='latin-1')
        
        try:
            market_df = pd.read_csv(data_dir / 'The_Rise_of_AI.csv', encoding='utf-8')
        except UnicodeDecodeError:
            market_df = pd.read_csv(data_dir / 'The_Rise_of_AI.csv', encoding='latin-1')
        
        return market_df, popularity_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Market Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    market_df, popularity_df = load_data()
    
    if market_df is None or popularity_df is None:
        st.error("Failed to load data. Please check data files.")
        return
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["📊 Executive Summary", "📈 Predictive Analytics", "🌍 Regional Intelligence", 
         "💼 Investment Advisor", "📡 Market Signals"]
    )
    
    # Page routing
    if page == "📊 Executive Summary":
        executive_summary_page(market_df, popularity_df)
    elif page == "📈 Predictive Analytics":
        predictive_analytics_page(market_df)
    elif page == "🌍 Regional Intelligence":
        regional_intelligence_page(popularity_df)
    elif page == "💼 Investment Advisor":
        investment_advisor_page(market_df)
    elif page == "📡 Market Signals":
        market_signals_page(market_df, popularity_df)

def executive_summary_page(market_df, popularity_df):
    """Executive Summary Dashboard"""
    st.markdown('<h2 class="section-header">📊 Executive Summary</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    latest_year = market_df['Year'].max()
    latest_data = market_df[market_df['Year'] == latest_year].iloc[0]
    
    with col1:
        st.metric(
            "AI Market Value",
            f"${latest_data['Global AI Market Value(in Billions)']}B",
            delta=f"{((latest_data['Global AI Market Value(in Billions)'] / market_df['Global AI Market Value(in Billions)'].iloc[0] - 1) * 100):.1f}% growth"
        )
    
    with col2:
        adoption_rate = float(latest_data['AI Adoption (%)'].strip('%'))
        st.metric(
            "AI Adoption Rate",
            f"{adoption_rate}%",
            delta=f"{adoption_rate - float(market_df['AI Adoption (%)'].iloc[0].strip('%')):.1f}pp increase"
        )
    
    with col3:
        st.metric(
            "AI Software Revenue",
            f"${latest_data['AI Software Revenue(in Billions)']}B",
            delta=f"{((latest_data['AI Software Revenue(in Billions)'] / market_df['AI Software Revenue(in Billions)'].iloc[0] - 1) * 100):.1f}% growth"
        )
    
    with col4:
        jobs_created = latest_data['Estimated New Jobs Created by AI (millions)']
        jobs_eliminated = latest_data['Estimated Jobs Eliminated by AI (millions)']
        net_impact = jobs_created - jobs_eliminated
        st.metric(
            "Net Job Impact",
            f"{net_impact:.1f}M jobs",
            delta="Created - Eliminated"
        )
    
    # Market growth visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('AI Market Value Growth', 'Software Revenue Trend', 
                       'Adoption Rate Progress', 'Job Market Impact'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": True}]]
    )
    
    # Market value
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Global AI Market Value(in Billions)'],
                   mode='lines+markers',
                   name='Market Value ($B)',
                   line=dict(color='#1f77b4', width=3)),
        row=1, col=1
    )
    
    # Software revenue
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['AI Software Revenue(in Billions)'],
                   mode='lines+markers',
                   name='Software Revenue ($B)',
                   line=dict(color='#ff7f0e', width=3)),
        row=1, col=2
    )
    
    # Adoption rate
    adoption_values = [float(x.strip('%')) for x in market_df['AI Adoption (%)']]
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=adoption_values,
                   mode='lines+markers',
                   name='Adoption Rate (%)',
                   line=dict(color='#2ca02c', width=3)),
        row=2, col=1
    )
    
    # Job impact
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Estimated New Jobs Created by AI (millions)'],
                   mode='lines+markers',
                   name='Jobs Created',
                   line=dict(color='#2ca02c', width=3)),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Estimated Jobs Eliminated by AI (millions)'],
                   mode='lines+markers',
                   name='Jobs Eliminated',
                   line=dict(color='#d62728', width=3)),
        row=2, col=2, secondary_y=False
    )
    
    fig.update_layout(height=600, showlegend=True, title_text="AI Market Overview")
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### 🔑 Key Insights")
    
    growth_rate = ((latest_data['Global AI Market Value(in Billions)'] / market_df['Global AI Market Value(in Billions)'].iloc[0] - 1) * 100)
    
    insights = [
        f"🚀 AI market has grown **{growth_rate:.1f}%** from {market_df['Year'].min()} to {latest_year}",
        f"📈 Current adoption rate is **{adoption_rate}%** with strong upward trend",
        f"💼 Net job creation: **{net_impact:.1f}M** new jobs (positive impact)",
        f"💰 Software revenue reached **${latest_data['AI Software Revenue(in Billions)']}B** in {latest_year}",
        f"🌍 Global coverage: **{len(popularity_df)}** countries/cities analyzed"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def predictive_analytics_page(market_df):
    """Predictive Analytics Page"""
    st.markdown('<h2 class="section-header">📈 Predictive Analytics</h2>', unsafe_allow_html=True)
    
    st.info("🔮 **Future Predictions & Trend Analysis**")
    
    # Simple trend projection
    col1, col2 = st.columns(2)
    
    with col1:
        target_metric = st.selectbox(
            "Select Metric to Predict",
            ["AI Software Revenue(in Billions)", 
             "Global AI Market Value(in Billions)",
             "AI Adoption (%)"]
        )
    
    with col2:
        years_ahead = st.slider("Years to Predict", 1, 10, 3)
    
    # Generate simple predictions using linear regression
    from sklearn.linear_model import LinearRegression
    
    if target_metric == "AI Adoption (%)":
        y_values = [float(x.strip('%')) for x in market_df[target_metric]]
    else:
        y_values = market_df[target_metric].values
    
    X = market_df['Year'].values.reshape(-1, 1)
    y = np.array(y_values).reshape(-1, 1)
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future
    future_years = np.arange(market_df['Year'].max() + 1, 
                           market_df['Year'].max() + years_ahead + 1).reshape(-1, 1)
    predictions = model.predict(future_years)
    
    # Create visualization
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=market_df['Year'],
        y=y_values,
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#1f77b4', width=3)
    ))
    
    # Predictions
    fig.add_trace(go.Scatter(
        x=future_years.flatten(),
        y=predictions.flatten(),
        mode='lines+markers',
        name='Predictions',
        line=dict(color='#ff7f0e', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=f"{target_metric} - Historical Trends & Predictions",
        xaxis_title="Year",
        yaxis_title=target_metric,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Prediction table
    st.markdown("### 📋 Prediction Summary")
    pred_df = pd.DataFrame({
        'Year': future_years.flatten(),
        'Predicted Value': predictions.flatten().round(2)
    })
    st.dataframe(pred_df, use_container_width=True)
    
    # Model performance
    r2_score = model.score(X, y)
    st.markdown(f"**Model R² Score:** {r2_score:.3f}")

def regional_intelligence_page(popularity_df):
    """Regional Intelligence Page"""
    st.markdown('<h2 class="section-header">🌍 Regional Intelligence</h2>', unsafe_allow_html=True)
    
    st.info("🗺️ **Global AI Popularity & Regional Patterns**")
    
    # Get numeric popularity columns
    numeric_cols = popularity_df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        # Country-wise analysis
        if 'Country' in popularity_df.columns:
            st.markdown("### 🏁 Top Countries by AI Interest")
            
            # Clean and process country data
            country_col = popularity_df.columns[1]  # Assuming second column is country popularity
            if pd.api.types.is_numeric_dtype(popularity_df[country_col]):
                top_countries = popularity_df.nlargest(10, country_col)[['Country', country_col]]
                
                fig = px.bar(
                    top_countries, 
                    x='Country', 
                    y=country_col,
                    title="Top 10 Countries by AI Popularity",
                    color=country_col,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # City-wise analysis if available
        if 'City' in popularity_df.columns:
            st.markdown("### 🏙️ Top Cities by AI Interest")
            
            city_col = popularity_df.columns[3]  # Assuming fourth column is city popularity
            if pd.api.types.is_numeric_dtype(popularity_df[city_col]):
                top_cities = popularity_df.nlargest(10, city_col)[['City', city_col]]
                
                fig = px.bar(
                    top_cities, 
                    x='City', 
                    y=city_col,
                    title="Top 10 Cities by AI Popularity",
                    color=city_col,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Regional insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### 🎯 Regional Insights")
    st.markdown(f"""
    - **Total Regions Analyzed:** {len(popularity_df)} countries/cities
    - **Data Coverage:** Global AI search trends and popularity
    - **Key Finding:** AI interest varies significantly by region
    - **Opportunity:** Emerging markets show high growth potential
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def investment_advisor_page(market_df):
    """Investment Advisor Page"""
    st.markdown('<h2 class="section-header">💼 Investment Advisor</h2>', unsafe_allow_html=True)
    
    st.info("💰 **Investment Insights & Recommendations**")
    
    # Get latest data
    latest_year = market_df['Year'].max()
    latest_data = market_df[market_df['Year'] == latest_year].iloc[0]
    
    # Investment metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Market Growth Analysis")
        
        # Calculate growth rates
        revenue_growth = []
        market_growth = []
        years = market_df['Year'].values[1:]
        
        for i in range(1, len(market_df)):
            rev_growth = ((market_df['AI Software Revenue(in Billions)'].iloc[i] / 
                          market_df['AI Software Revenue(in Billions)'].iloc[i-1] - 1) * 100)
            market_val_growth = ((market_df['Global AI Market Value(in Billions)'].iloc[i] / 
                                 market_df['Global AI Market Value(in Billions)'].iloc[i-1] - 1) * 100)
            revenue_growth.append(rev_growth)
            market_growth.append(market_val_growth)
        
        growth_df = pd.DataFrame({
            'Year': years,
            'Revenue Growth (%)': revenue_growth,
            'Market Growth (%)': market_growth
        })
        
        fig = px.line(
            growth_df, 
            x='Year', 
            y=['Revenue Growth (%)', 'Market Growth (%)'],
            title="Annual Growth Rates",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Investment Recommendations")
        
        avg_revenue_growth = np.mean(revenue_growth)
        avg_market_growth = np.mean(market_growth)
        
        recommendations = []
        if avg_revenue_growth > 20:
            recommendations.append("🟢 **STRONG BUY** - Software revenue showing excellent growth")
        elif avg_revenue_growth > 10:
            recommendations.append("🟡 **BUY** - Moderate growth in software revenue")
        else:
            recommendations.append("🔴 **HOLD** - Revenue growth slowing")
        
        if avg_market_growth > 25:
            recommendations.append("🚀 **HIGH GROWTH** - Market expanding rapidly")
        
        latest_adoption = float(latest_data['AI Adoption (%)'].strip('%'))
        if latest_adoption < 50:
            recommendations.append("📈 **EARLY STAGE** - Significant room for growth")
        
        for rec in recommendations:
            st.markdown(rec)
        
        # Risk assessment
        st.markdown("### ⚠️ Risk Factors")
        job_elimination = latest_data['Estimated Jobs Eliminated by AI (millions)']
        if job_elimination > 20:
            st.markdown("🔴 High job displacement risk")
        else:
            st.markdown("🟢 Manageable job market impact")

def market_signals_page(market_df, popularity_df):
    """Market Signals Page"""
    st.markdown('<h2 class="section-header">📡 Market Signals</h2>', unsafe_allow_html=True)
    
    st.info("📊 **Real-time Market Indicators & Signals**")
    
    # Market momentum indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Momentum Indicators")
        
        # Calculate momentum (year-over-year change)
        latest_year = market_df['Year'].max()
        current_data = market_df[market_df['Year'] == latest_year].iloc[0]
        previous_data = market_df[market_df['Year'] == latest_year - 1].iloc[0]
        
        revenue_momentum = ((current_data['AI Software Revenue(in Billions)'] / 
                           previous_data['AI Software Revenue(in Billions)'] - 1) * 100)
        
        market_momentum = ((current_data['Global AI Market Value(in Billions)'] / 
                          previous_data['Global AI Market Value(in Billions)'] - 1) * 100)
        
        adoption_momentum = (float(current_data['AI Adoption (%)'].strip('%')) - 
                           float(previous_data['AI Adoption (%)'].strip('%')))
        
        # Display signals
        signals = {
            "Revenue Growth": f"{revenue_momentum:.1f}%",
            "Market Expansion": f"{market_momentum:.1f}%", 
            "Adoption Increase": f"{adoption_momentum:.1f}pp"
        }
        
        for signal, value in signals.items():
            st.metric(signal, value)
    
    with col2:
        st.markdown("### 🎯 Market Sentiment")
        
        # Create sentiment gauge based on growth rates
        avg_growth = (revenue_momentum + market_momentum) / 2
        
        if avg_growth > 30:
            sentiment = "🔥 VERY BULLISH"
            color = "green"
        elif avg_growth > 15:
            sentiment = "📈 BULLISH"
            color = "lightgreen"
        elif avg_growth > 5:
            sentiment = "➡️ NEUTRAL"
            color = "yellow"
        else:
            sentiment = "📉 BEARISH"
            color = "red"
        
        st.markdown(f"**Current Sentiment:** {sentiment}")
        
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = avg_growth,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Growth Rate (%)"},
            delta = {'reference': 20},
            gauge = {
                'axis': {'range': [None, 50]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 25], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30}}))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
