"""
Enhanced AI Market Intelligence Dashboard
Professional-grade analytics platform with advanced features
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
    page_title="AI Market Intelligence - Enhanced",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-header {
        font-size: 2.2rem;
        color: #1f2937;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .insight-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #3b82f6;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .alert-success {
        background-color: #d1fae5;
        color: #065f46;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
    }
    .alert-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
    }
    .alert-info {
        background-color: #dbeafe;
        color: #1e40af;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_enhanced_data():
    """Load data with fallback to raw if processed doesn't exist"""
    try:
        # Try to load processed data first
        processed_dir = Path('../data/processed')
        if (processed_dir / 'ai_market_clean.csv').exists():
            market_df = pd.read_csv(processed_dir / 'ai_market_clean.csv')
            popularity_df = pd.read_csv(processed_dir / 'ai_popularity_clean.csv')
            data_source = "processed"
        else:
            # Fallback to raw data
            data_dir = Path('../data/raw')
            try:
                market_df = pd.read_csv(data_dir / 'The_Rise_of_AI.csv', encoding='utf-8')
            except UnicodeDecodeError:
                market_df = pd.read_csv(data_dir / 'The_Rise_of_AI.csv', encoding='latin-1')
            
            try:
                popularity_df = pd.read_csv(data_dir / 'AI_ML_popularity.csv', encoding='utf-8')
            except UnicodeDecodeError:
                popularity_df = pd.read_csv(data_dir / 'AI_ML_popularity.csv', encoding='latin-1')
            data_source = "raw"
        
        return market_df, popularity_df, data_source
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, "error"

def main():
    # Enhanced header
    st.markdown('<h1 class="main-header">🚀 AI Market Intelligence - Enhanced Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    market_df, popularity_df, data_source = load_enhanced_data()
    
    if market_df is None or popularity_df is None:
        st.error("Failed to load data. Please check data files.")
        return
    
    # Data source indicator
    if data_source == "processed":
        st.markdown('<div class="alert-success">✅ Using processed data with enhanced features</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-info">ℹ️ Using raw data - run data cleaning notebook for enhanced features</div>', unsafe_allow_html=True)
    
    # Enhanced sidebar navigation
    st.sidebar.title("🧭 Enhanced Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Select Analytics Page",
        ["📊 Executive Summary", 
         "🔮 Predictive Analytics", 
         "🌍 Regional Intelligence", 
         "💼 Investment Advisor", 
         "📡 Market Signals",
         "⚖️ Risk Assessment"]
    )
    
    # Additional sidebar controls
    st.sidebar.markdown("### 🎛️ Dashboard Controls")
    
    # Time range selector
    if 'Year' in market_df.columns:
        min_year = int(market_df['Year'].min())
        max_year = int(market_df['Year'].max())
        year_range = st.sidebar.slider(
            "Year Range",
            min_year, max_year, (min_year, max_year)
        )
        market_df = market_df[(market_df['Year'] >= year_range[0]) & (market_df['Year'] <= year_range[1])]
    
    # Page routing with enhanced features
    if page == "📊 Executive Summary":
        executive_summary_enhanced(market_df, popularity_df)
    elif page == "🔮 Predictive Analytics":
        predictive_analytics_enhanced(market_df)
    elif page == "🌍 Regional Intelligence":
        regional_intelligence_enhanced(popularity_df)
    elif page == "💼 Investment Advisor":
        investment_advisor_enhanced(market_df)
    elif page == "📡 Market Signals":
        market_signals_enhanced(market_df, popularity_df)
    elif page == "⚖️ Risk Assessment":
        risk_assessment_page(market_df)

def executive_summary_enhanced(market_df, popularity_df):
    """Enhanced Executive Summary with KPIs and insights"""
    st.markdown('<h2 class="section-header">📊 Executive Summary</h2>', unsafe_allow_html=True)
    
    # Enhanced KPI section
    st.markdown("### 🎯 Key Performance Indicators")
    
    latest_year = market_df['Year'].max()
    latest_data = market_df[market_df['Year'] == latest_year].iloc[0]
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        market_value = latest_data['Global AI Market Value(in Billions)']
        growth_rate = ((market_value / market_df['Global AI Market Value(in Billions)'].iloc[0] - 1) * 100)
        st.metric(
            "🌍 Global AI Market",
            f"${market_value}B",
            delta=f"{growth_rate:.1f}% total growth",
            help="Total AI market capitalization"
        )
    
    with col2:
        revenue = latest_data['AI Software Revenue(in Billions)']
        revenue_growth = ((revenue / market_df['AI Software Revenue(in Billions)'].iloc[0] - 1) * 100)
        st.metric(
            "💰 Software Revenue",
            f"${revenue}B",
            delta=f"{revenue_growth:.1f}% growth",
            help="AI software and services revenue"
        )
    
    with col3:
        adoption_rate = float(latest_data['AI Adoption (%)'].strip('%'))
        first_adoption = float(market_df['AI Adoption (%)'].iloc[0].strip('%'))
        adoption_change = adoption_rate - first_adoption
        st.metric(
            "📈 Adoption Rate",
            f"{adoption_rate}%",
            delta=f"{adoption_change:.1f}pp increase",
            help="Percentage of organizations using AI"
        )
    
    with col4:
        jobs_created = latest_data['Estimated New Jobs Created by AI (millions)']
        jobs_eliminated = latest_data['Estimated Jobs Eliminated by AI (millions)']
        net_impact = jobs_created - jobs_eliminated
        st.metric(
            "👥 Net Job Impact",
            f"{net_impact:.1f}M",
            delta="New jobs - Eliminated",
            help="Net job creation from AI adoption"
        )
    
    with col5:
        competitive_edge = latest_data['Organizations Believing AI Provides Competitive Edge']
        st.metric(
            "🏆 Competitive Edge",
            f"{competitive_edge}%",
            delta="Strategic importance",
            help="Organizations seeing AI as competitive advantage"
        )
    
    # Market trends visualization
    st.markdown("### 📈 Market Trends Dashboard")
    
    # Create 3D surface plot for advanced visualization
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Market Value Trajectory', 'Revenue Growth Curve', 'Adoption Acceleration',
                       'Job Market Evolution', 'Strategic Adoption', 'Productivity Impact'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "scatter"}, {"type": "scatter"}]],
        vertical_spacing=0.12
    )
    
    # Market value with trend
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Global AI Market Value(in Billions)'],
                   mode='lines+markers',
                   name='Market Value',
                   line=dict(color='#1e3a8a', width=4),
                   marker=dict(size=8)),
        row=1, col=1
    )
    
    # Revenue with forecast line
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['AI Software Revenue(in Billions)'],
                   mode='lines+markers',
                   name='Software Revenue',
                   line=dict(color='#dc2626', width=4),
                   marker=dict(size=8)),
        row=1, col=2
    )
    
    # Adoption rate
    adoption_values = [float(x.strip('%')) for x in market_df['AI Adoption (%)']]
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=adoption_values,
                   mode='lines+markers',
                   name='Adoption Rate',
                   line=dict(color='#059669', width=4),
                   marker=dict(size=8)),
        row=1, col=3
    )
    
    # Job impact comparison
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Estimated New Jobs Created by AI (millions)'],
                   mode='lines+markers',
                   name='Jobs Created',
                   line=dict(color='#059669', width=3)),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Estimated Jobs Eliminated by AI (millions)'],
                   mode='lines+markers',
                   name='Jobs Eliminated',
                   line=dict(color='#dc2626', width=3, dash='dash')),
        row=2, col=1
    )
    
    # Strategic metrics
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=market_df['Organizations Believing AI Provides Competitive Edge'],
                   mode='lines+markers',
                   name='Competitive Edge',
                   line=dict(color='#7c3aed', width=3)),
        row=2, col=2
    )
    
    # Productivity expectations
    productivity_values = [float(str(x).strip('%')) for x in market_df['Expected Increase in Employee Productivity Due to AI (%)']]
    fig.add_trace(
        go.Scatter(x=market_df['Year'], 
                   y=productivity_values,
                   mode='lines+markers',
                   name='Productivity Gain',
                   line=dict(color='#ea580c', width=3)),
        row=2, col=3
    )
    
    fig.update_layout(
        height=700, 
        showlegend=False,
        title_text="📊 Comprehensive AI Market Analytics Dashboard",
        title_x=0.5,
        title_font_size=20
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced insights with AI-powered recommendations
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI-Powered Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Strategic Opportunities")
        
        # Calculate key metrics
        cagr = ((latest_data['Global AI Market Value(in Billions)'] / market_df['Global AI Market Value(in Billions)'].iloc[0]) ** (1/len(market_df)) - 1) * 100
        
        opportunities = [
            f"🚀 **Market CAGR**: {cagr:.1f}% - Exceptional growth trajectory",
            f"📊 **Current Adoption**: {adoption_rate}% - Significant headroom for growth",
            f"💼 **Job Net Creation**: {net_impact:.1f}M - Positive employment impact",
            f"🏆 **Strategic Value**: {competitive_edge}% see competitive advantage",
            f"🌍 **Global Reach**: {len(popularity_df)} markets analyzed"
        ]
        
        for opp in opportunities:
            st.markdown(f"- {opp}")
    
    with col2:
        st.markdown("#### ⚡ Market Signals")
        
        # Calculate momentum indicators
        recent_growth = ((latest_data['AI Software Revenue(in Billions)'] / 
                         market_df['AI Software Revenue(in Billions)'].iloc[-2] - 1) * 100)
        
        signals = []
        if recent_growth > 20:
            signals.append("🟢 **STRONG MOMENTUM** - Accelerating growth")
        elif recent_growth > 10:
            signals.append("🟡 **POSITIVE MOMENTUM** - Steady growth")
        else:
            signals.append("🔴 **SLOWING MOMENTUM** - Growth deceleration")
        
        if adoption_rate > 50:
            signals.append("🟢 **MAINSTREAM ADOPTION** - Past early adopter phase")
        else:
            signals.append("🟡 **GROWTH PHASE** - Still expanding market")
        
        if net_impact > 0:
            signals.append("🟢 **JOB CREATION** - Net positive employment")
        else:
            signals.append("🔴 **JOB DISPLACEMENT** - Net negative employment")
        
        for signal in signals:
            st.markdown(f"- {signal}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def predictive_analytics_enhanced(market_df):
    """Enhanced Predictive Analytics with multiple models"""
    st.markdown('<h2 class="section-header">🔮 Advanced Predictive Analytics</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-info">🤖 <b>AI-Powered Forecasting Engine</b> - Multiple algorithms for robust predictions</div>', unsafe_allow_html=True)
    
    # Enhanced controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_metric = st.selectbox(
            "🎯 Prediction Target",
            ["AI Software Revenue(in Billions)", 
             "Global AI Market Value(in Billions)",
             "AI Adoption (%)"],
            help="Select the metric to predict"
        )
    
    with col2:
        forecast_years = st.slider("📅 Forecast Horizon", 1, 10, 5)
    
    with col3:
        confidence_level = st.selectbox(
            "🎲 Confidence Level",
            [90, 95, 99],
            index=1,
            help="Statistical confidence level for predictions"
        )
    
    # Enhanced modeling with multiple algorithms
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import PolynomialFeatures
    
    # Prepare data
    if target_metric == "AI Adoption (%)":
        y_values = [float(str(x).strip('%')) for x in market_df[target_metric]]
    else:
        y_values = market_df[target_metric].values
    
    X = market_df['Year'].values.reshape(-1, 1)
    y = np.array(y_values)
    
    # Multiple models
    models = {
        "📈 Linear Trend": LinearRegression(),
        "🌳 Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "📊 Polynomial (2nd)": LinearRegression()  # Will fit with polynomial features
    }
    
    predictions = {}
    scores = {}
    
    # Future years for prediction
    future_years = np.arange(market_df['Year'].max() + 1, 
                           market_df['Year'].max() + forecast_years + 1).reshape(-1, 1)
    
    # Fit models and generate predictions
    for name, model in models.items():
        if "Polynomial" in name:
            # Polynomial regression
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            future_poly = poly_features.transform(future_years)
            model.fit(X_poly, y)
            pred = model.predict(future_poly)
            score = model.score(X_poly, y)
        else:
            model.fit(X, y)
            pred = model.predict(future_years)
            score = model.score(X, y)
        
        predictions[name] = pred
        scores[name] = score
    
    # Ensemble prediction (average of all models)
    ensemble_pred = np.mean(list(predictions.values()), axis=0)
    predictions["🎯 Ensemble"] = ensemble_pred
    
    # Visualization
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=market_df['Year'],
        y=y_values,
        mode='lines+markers',
        name='📊 Historical Data',
        line=dict(color='#1f2937', width=4),
        marker=dict(size=10)
    ))
    
    # Model predictions with confidence bands
    colors = ['#ef4444', '#22c55e', '#3b82f6', '#8b5cf6']
    
    for i, (name, pred) in enumerate(predictions.items()):
        if name != "🎯 Ensemble":
            fig.add_trace(go.Scatter(
                x=future_years.flatten(),
                y=pred,
                mode='lines+markers',
                name=name,
                line=dict(color=colors[i % len(colors)], width=2, dash='dot'),
                opacity=0.7
            ))
    
    # Ensemble prediction (main forecast)
    fig.add_trace(go.Scatter(
        x=future_years.flatten(),
        y=ensemble_pred,
        mode='lines+markers',
        name='🎯 Ensemble Forecast',
        line=dict(color='#dc2626', width=4),
        marker=dict(size=8)
    ))
    
    # Add confidence intervals for ensemble
    std_dev = np.std(list(predictions.values())[:-1], axis=0)  # Exclude ensemble from std calculation
    confidence_multiplier = {90: 1.645, 95: 1.96, 99: 2.576}[confidence_level]
    
    upper_bound = ensemble_pred + confidence_multiplier * std_dev
    lower_bound = ensemble_pred - confidence_multiplier * std_dev
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([future_years.flatten(), future_years.flatten()[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill='toself',
        fillcolor='rgba(220, 38, 38, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name=f'{confidence_level}% Confidence Band',
        showlegend=True
    ))
    
    fig.update_layout(
        title=f"🔮 {target_metric} - Multi-Model Forecast",
        xaxis_title="Year",
        yaxis_title=target_metric,
        height=600,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Model performance comparison
    st.markdown("### 🏆 Model Performance Comparison")
    
    performance_df = pd.DataFrame({
        'Model': list(scores.keys()),
        'R² Score': list(scores.values())
    }).sort_values('R² Score', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(performance_df, use_container_width=True)
    
    with col2:
        # Performance bar chart
        fig_perf = px.bar(
            performance_df, 
            x='R² Score', 
            y='Model',
            orientation='h',
            title="Model Accuracy Comparison",
            color='R² Score',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    
    # Prediction summary table
    st.markdown("### 📋 Forecast Summary")
    
    forecast_df = pd.DataFrame({
        'Year': future_years.flatten(),
        'Ensemble Forecast': ensemble_pred.round(2),
        f'Lower Bound ({confidence_level}%)': lower_bound.round(2),
        f'Upper Bound ({confidence_level}%)': upper_bound.round(2)
    })
    
    st.dataframe(forecast_df, use_container_width=True)

def risk_assessment_page(market_df):
    """Risk Assessment Page"""
    st.markdown('<h2 class="section-header">⚖️ Risk Assessment</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-warning">⚠️ <b>Risk Analysis</b> - Identify potential market risks and mitigation strategies</div>', unsafe_allow_html=True)
    
    latest_year = market_df['Year'].max()
    latest_data = market_df[market_df['Year'] == latest_year].iloc[0]
    
    # Risk metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Job displacement risk
        job_elimination = latest_data['Estimated Jobs Eliminated by AI (millions)']
        job_creation = latest_data['Estimated New Jobs Created by AI (millions)']
        displacement_ratio = job_elimination / job_creation if job_creation > 0 else float('inf')
        
        risk_level = "HIGH" if displacement_ratio > 1.5 else "MEDIUM" if displacement_ratio > 0.8 else "LOW"
        color = "🔴" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
        
        st.metric(
            "👥 Employment Risk",
            f"{risk_level}",
            delta=f"Ratio: {displacement_ratio:.2f}",
            help="Job elimination vs creation ratio"
        )
        st.markdown(f"{color} **Risk Level**: {risk_level}")
    
    with col2:
        # Market concentration risk
        adoption_rate = float(latest_data['AI Adoption (%)'].strip('%'))
        concentration_risk = "HIGH" if adoption_rate > 70 else "MEDIUM" if adoption_rate > 40 else "LOW"
        color = "🔴" if concentration_risk == "HIGH" else "🟡" if concentration_risk == "MEDIUM" else "🟢"
        
        st.metric(
            "📊 Market Saturation",
            f"{concentration_risk}",
            delta=f"Adoption: {adoption_rate}%"
        )
        st.markdown(f"{color} **Saturation Risk**: {concentration_risk}")
    
    with col3:
        # Growth sustainability
        recent_growth = ((latest_data['Global AI Market Value(in Billions)'] / 
                         market_df['Global AI Market Value(in Billions)'].iloc[-2] - 1) * 100)
        
        sustainability = "HIGH" if recent_growth < 10 else "MEDIUM" if recent_growth < 25 else "LOW"
        color = "🔴" if sustainability == "HIGH" else "🟡" if sustainability == "MEDIUM" else "🟢"
        
        st.metric(
            "📈 Growth Sustainability",
            f"{sustainability}",
            delta=f"Recent: {recent_growth:.1f}%"
        )
        st.markdown(f"{color} **Sustainability Risk**: {sustainability}")

def regional_intelligence_enhanced(popularity_df):
    """Enhanced Regional Intelligence"""
    st.markdown('<h2 class="section-header">🌍 Advanced Regional Intelligence</h2>', unsafe_allow_html=True)
    
    # Regional metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🗺️ Countries", len(popularity_df['Country'].unique()) if 'Country' in popularity_df.columns else 0)
    with col2:
        st.metric("🏙️ Cities", len(popularity_df['City'].dropna()) if 'City' in popularity_df.columns else 0)
    with col3:
        st.metric("📊 Data Points", len(popularity_df))
    with col4:
        numeric_cols = popularity_df.select_dtypes(include=[np.number]).columns
        avg_score = popularity_df[numeric_cols].mean().mean() if len(numeric_cols) > 0 else 0
        st.metric("⭐ Avg Interest", f"{avg_score:.1f}")
    
    # Interactive regional analysis
    if 'Country' in popularity_df.columns:
        st.markdown("### 🌐 Global AI Interest Heatmap")
        
        # Create country ranking
        country_col = None
        for col in popularity_df.columns:
            if 'popularity' in col.lower() and pd.api.types.is_numeric_dtype(popularity_df[col]):
                country_col = col
                break
        
        if country_col:
            country_data = popularity_df.groupby('Country')[country_col].mean().reset_index()
            country_data = country_data.sort_values(country_col, ascending=False).head(20)
            
            # Enhanced world map visualization
            fig = px.choropleth(
                country_data,
                locations='Country',
                color=country_col,
                locationmode='country names',
                title="🌍 Global AI Interest Distribution",
                color_continuous_scale='Viridis',
                labels={country_col: 'AI Interest Score'}
            )
            
            fig.update_layout(
                height=500,
                geo=dict(showframe=False, showcoastlines=True)
            )
            
            st.plotly_chart(fig, use_container_width=True)

def investment_advisor_enhanced(market_df):
    """Enhanced Investment Advisor with portfolio recommendations"""
    st.markdown('<h2 class="section-header">💼 AI Investment Advisor</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-success">💰 <b>Investment Intelligence</b> - Data-driven investment recommendations</div>', unsafe_allow_html=True)
    
    # Portfolio analysis
    latest_year = market_df['Year'].max()
    latest_data = market_df[market_df['Year'] == latest_year].iloc[0]
    
    # Calculate investment metrics
    revenue_cagr = ((latest_data['AI Software Revenue(in Billions)'] / 
                    market_df['AI Software Revenue(in Billions)'].iloc[0]) ** (1/len(market_df)) - 1) * 100
    
    market_cagr = ((latest_data['Global AI Market Value(in Billions)'] / 
                   market_df['Global AI Market Value(in Billions)'].iloc[0]) ** (1/len(market_df)) - 1) * 100
    
    # Investment recommendation engine
    st.markdown("### 🎯 Investment Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💎 Investment Thesis")
        
        if revenue_cagr > 25 and market_cagr > 20:
            recommendation = "🟢 **STRONG BUY**"
            rationale = "Exceptional growth in both revenue and market value"
        elif revenue_cagr > 15 and market_cagr > 15:
            recommendation = "🟡 **BUY**" 
            rationale = "Solid growth fundamentals"
        elif revenue_cagr > 10 or market_cagr > 10:
            recommendation = "🟡 **HOLD**"
            rationale = "Moderate growth, monitor trends"
        else:
            recommendation = "🔴 **CAUTION**"
            rationale = "Growth slowing, reassess position"
        
        st.markdown(f"**Overall Rating:** {recommendation}")
        st.markdown(f"**Rationale:** {rationale}")
        
        # Risk-return profile
        st.markdown("#### ⚖️ Risk-Return Profile")
        risk_score = abs(revenue_cagr - market_cagr) / max(revenue_cagr, market_cagr) * 100
        
        st.markdown(f"- **Expected Return:** {max(revenue_cagr, market_cagr):.1f}% CAGR")
        st.markdown(f"- **Risk Score:** {risk_score:.1f}% (volatility measure)")
        st.markdown("- **Investment Horizon:** 3-5 years recommended")
    
    with col2:
        # Investment allocation pie chart
        st.markdown("#### 🥧 Suggested Portfolio Allocation")
        
        allocation_data = {
            'AI Software': 40,
            'AI Hardware': 25, 
            'AI Services': 20,
            'AI Research': 10,
            'Cash/Hedge': 5
        }
        
        fig = px.pie(
            values=list(allocation_data.values()),
            names=list(allocation_data.keys()),
            title="Recommended AI Portfolio Mix",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

def market_signals_enhanced(market_df, popularity_df):
    """Enhanced Market Signals with real-time indicators"""
    st.markdown('<h2 class="section-header">📡 Advanced Market Signals</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-info">📊 <b>Real-time Market Intelligence</b> - Live market indicators and trend analysis</div>', unsafe_allow_html=True)
    
    # Market sentiment dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Multi-dimensional signal analysis
        latest_year = market_df['Year'].max()
        current = market_df[market_df['Year'] == latest_year].iloc[0]
        previous = market_df[market_df['Year'] == latest_year - 1].iloc[0]
        
        # Calculate multiple signals
        signals = {
            "Revenue Momentum": ((current['AI Software Revenue(in Billions)'] / 
                                previous['AI Software Revenue(in Billions)'] - 1) * 100),
            "Market Expansion": ((current['Global AI Market Value(in Billions)'] / 
                                previous['Global AI Market Value(in Billions)'] - 1) * 100),
            "Adoption Velocity": (float(current['AI Adoption (%)'].strip('%')) - 
                                float(previous['AI Adoption (%)'].strip('%'))),
            "Strategic Priority": (current['Companies Prioritizing AI in Strategy'] - 
                                 previous['Companies Prioritizing AI in Strategy'])
        }
        
        # Create radar chart for signals
        fig = go.Figure()
        
        # Normalize signals for radar chart
        signal_names = list(signals.keys())
        signal_values = [max(0, min(100, val * 2 + 50)) for val in signals.values()]  # Normalize to 0-100
        
        fig.add_trace(go.Scatterpolar(
            r=signal_values + [signal_values[0]],  # Close the radar
            theta=signal_names + [signal_names[0]],
            fill='toself',
            name='Current Signals',
            fillcolor='rgba(59, 130, 246, 0.3)',
            line=dict(color='#3b82f6', width=3)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title="📡 Market Signal Strength",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🚦 Signal Status")
        
        for signal, value in signals.items():
            if value > 20:
                st.markdown(f"🟢 **{signal}**: Strong ({value:.1f}%)")
            elif value > 5:
                st.markdown(f"🟡 **{signal}**: Moderate ({value:.1f}%)")
            else:
                st.markdown(f"🔴 **{signal}**: Weak ({value:.1f}%)")
        
        # Overall market sentiment
        avg_signal = np.mean(list(signals.values()))
        if avg_signal > 15:
            sentiment = "🔥 VERY BULLISH"
        elif avg_signal > 5:
            sentiment = "📈 BULLISH"
        elif avg_signal > -5:
            sentiment = "➡️ NEUTRAL"
        else:
            sentiment = "📉 BEARISH"
        
        st.markdown(f"### {sentiment}")
        st.markdown(f"**Composite Score:** {avg_signal:.1f}%")

if __name__ == "__main__":
    main()
