"""
Simple AI Market Intelligence Dashboard
Single-page dashboard with key statistics and visualizations
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
    page_icon="📊",
    layout="wide"
)

# Simple CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load processed data"""
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Load processed data
        processed_dir = project_root / 'data' / 'processed'
        market_df = pd.read_csv(processed_dir / 'ai_market_clean.csv')
        popularity_df = pd.read_csv(processed_dir / 'ai_popularity_clean.csv')
        
        return market_df, popularity_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 AI Market Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    market_df, popularity_df = load_data()
    
    if market_df is None or popularity_df is None:
        st.error("Failed to load data. Please check data files.")
        return
    
    # Latest year data for metrics
    latest_year = market_df['year'].max()
    latest_data = market_df[market_df['year'] == latest_year].iloc[0]
    first_data = market_df.iloc[0]
    
    # Section 1: Key Metrics
    st.markdown("## 📈 Key Market Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        market_value = latest_data['global_ai_market_value_in_billions']
        growth = ((market_value / first_data['global_ai_market_value_in_billions']) - 1) * 100
        st.metric(
            "Global AI Market",
            f"${market_value:.0f}B",
            delta=f"{growth:.0f}% growth"
        )
    
    with col2:
        revenue = latest_data['ai_software_revenue_in_billions']
        revenue_growth = ((revenue / first_data['ai_software_revenue_in_billions']) - 1) * 100
        st.metric(
            "Software Revenue",
            f"${revenue:.1f}B",
            delta=f"{revenue_growth:.0f}% growth"
        )
    
    with col3:
        adoption = latest_data['ai_adoption_%']
        adoption_change = adoption - first_data['ai_adoption_%']
        st.metric(
            "AI Adoption",
            f"{adoption:.0f}%",
            delta=f"+{adoption_change:.0f}pp"
        )
    
    with col4:
        jobs_created = latest_data['estimated_new_jobs_created_by_ai_millions']
        jobs_eliminated = latest_data['estimated_jobs_eliminated_by_ai_millions']
        net_jobs = jobs_created - jobs_eliminated
        st.metric(
            "Net Jobs Impact",
            f"{net_jobs:+.1f}M",
            delta="Created - Eliminated"
        )
    
    with col5:
        competitive = latest_data['organizations_believing_ai_provides_competitive_edge']
        st.metric(
            "Competitive Edge",
            f"{competitive:.0f}%",
            delta="Believe AI critical"
        )
    
    # Section 2: Main Charts
    st.markdown("## 📊 Market Trends")
    
    # Create subplots
    col1, col2 = st.columns(2)
    
    with col1:
        # Market Value Growth
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=market_df['year'],
            y=market_df['global_ai_market_value_in_billions'],
            mode='lines+markers',
            name='Market Value',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8)
        ))
        fig1.update_layout(
            title="Global AI Market Value Growth",
            xaxis_title="Year",
            yaxis_title="Market Value (Billions USD)",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Revenue Growth
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=market_df['year'],
            y=market_df['ai_software_revenue_in_billions'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8)
        ))
        fig2.update_layout(
            title="AI Software Revenue Growth",
            xaxis_title="Year",
            yaxis_title="Revenue (Billions USD)",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Section 3: Adoption and Impact
    st.markdown("## 🚀 Adoption & Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Adoption Rate
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=market_df['year'],
            y=market_df['ai_adoption_%'],
            name='Current Adoption',
            marker_color='#3b82f6'
        ))
        fig3.add_trace(go.Bar(
            x=market_df['year'],
            y=market_df['global_expectation_for_ai_adoption_%'],
            name='Expected Adoption',
            marker_color='#93c5fd',
            opacity=0.7
        ))
        fig3.update_layout(
            title="AI Adoption: Current vs Expected",
            xaxis_title="Year",
            yaxis_title="Adoption Rate (%)",
            height=350,
            barmode='group'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Job Impact
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=market_df['year'],
            y=market_df['estimated_new_jobs_created_by_ai_millions'],
            mode='lines+markers',
            name='Jobs Created',
            line=dict(color='#10b981', width=2),
            marker=dict(size=6)
        ))
        fig4.add_trace(go.Scatter(
            x=market_df['year'],
            y=market_df['estimated_jobs_eliminated_by_ai_millions'],
            mode='lines+markers',
            name='Jobs Eliminated',
            line=dict(color='#ef4444', width=2),
            marker=dict(size=6)
        ))
        fig4.update_layout(
            title="Employment Impact of AI",
            xaxis_title="Year",
            yaxis_title="Jobs (Millions)",
            height=350,
            hovermode='x unified'
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Section 4: Industry Analysis
    st.markdown("## 🏭 Industry Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Automation Risk by Industry
        risk_data = {
            'Industry': ['Transportation & Storage', 'Wholesale & Retail', 'Manufacturing'],
            'Risk %': [
                latest_data['jobs_at_high_risk_of_automation__transportation_&_storage_%'],
                latest_data['jobs_at_high_risk_of_automation__wholesale_&_retail_trade'],
                latest_data['jobs_at_high_risk_of_automation__manufacturing']
            ]
        }
        risk_df = pd.DataFrame(risk_data)
        
        fig5 = px.bar(
            risk_df,
            x='Risk %',
            y='Industry',
            orientation='h',
            title='Jobs at High Risk of Automation by Industry',
            color='Risk %',
            color_continuous_scale='RdYlGn_r'
        )
        fig5.update_layout(height=350)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Strategic Importance
        strategic_data = pd.DataFrame({
            'Year': market_df['year'],
            'Competitive Edge': market_df['organizations_believing_ai_provides_competitive_edge'],
            'Strategic Priority': market_df['companies_prioritizing_ai_in_strategy']
        })
        
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(
            x=strategic_data['Year'],
            y=strategic_data['Competitive Edge'],
            mode='lines+markers',
            name='See Competitive Edge',
            line=dict(color='#7c3aed', width=2)
        ))
        fig6.add_trace(go.Scatter(
            x=strategic_data['Year'],
            y=strategic_data['Strategic Priority'],
            mode='lines+markers',
            name='Prioritize in Strategy',
            line=dict(color='#ec4899', width=2)
        ))
        fig6.update_layout(
            title="Strategic Importance of AI",
            xaxis_title="Year",
            yaxis_title="Percentage of Companies (%)",
            height=350,
            hovermode='x unified'
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Section 5: Regional Analysis (if popularity data is available)
    if 'country' in popularity_df.columns:
        st.markdown("## 🌍 Global AI Interest")
        
        # Get top 20 countries by AI interest (filter out empty countries and use ai_and_ml_popularity)
        country_interest = popularity_df[popularity_df['country'].notna() & (popularity_df['country'] != '')].copy()
        country_interest = country_interest.groupby('country')['ai_and_ml_popularity'].mean().reset_index()
        country_interest = country_interest.sort_values('ai_and_ml_popularity', ascending=False).head(20)
        
        fig7 = px.bar(
            country_interest,
            x='ai_and_ml_popularity',
            y='country',
            orientation='h',
            title='Top 20 Countries by AI Interest Score',
            color='ai_and_ml_popularity',
            color_continuous_scale='Viridis'
        )
        fig7.update_layout(
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    # Section 6: Future Projections
    st.markdown("## 🔮 Market Projections")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Calculate CAGR
        years = len(market_df)
        market_cagr = ((latest_data['global_ai_market_value_in_billions'] / 
                       first_data['global_ai_market_value_in_billions']) ** (1/years) - 1) * 100
        
        st.info(f"""
        **Market CAGR**  
        {market_cagr:.1f}% annual growth
        
        **From ${first_data['global_ai_market_value_in_billions']:.0f}B to ${latest_data['global_ai_market_value_in_billions']:.0f}B**
        """)
    
    with col2:
        revenue_cagr = ((latest_data['ai_software_revenue_in_billions'] / 
                        first_data['ai_software_revenue_in_billions']) ** (1/years) - 1) * 100
        
        st.success(f"""
        **Revenue CAGR**  
        {revenue_cagr:.1f}% annual growth
        
        **From ${first_data['ai_software_revenue_in_billions']:.1f}B to ${latest_data['ai_software_revenue_in_billions']:.1f}B**
        """)
    
    with col3:
        productivity_gain = latest_data['expected_increase_in_employee_productivity_due_to_ai_%']
        revenue_increase = latest_data['estimated_revenue_increase_from_ai_trillions_usd']
        
        st.warning(f"""
        **Expected Impact**  
        {productivity_gain:.0f}% productivity gain
        
        **${revenue_increase:.1f}T revenue increase**
        """)
    
    # Footer statistics
    st.markdown("---")
    st.markdown("### 📊 Quick Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        **Voice Assistants**  
        {latest_data['americans_using_voice_assistants_%']:.0f}% Americans use them  
        {latest_data['digital_voice_assistants_billions_of_devices']:.1f}B devices globally
        """)
    
    with col2:
        st.markdown(f"""
        **Healthcare AI**  
        {latest_data['medical_professionals_using_ai_for_diagnosis']:.0f}% use AI for diagnosis  
        ${latest_data['ai_contribution_to_healthcare_in_billions']:.0f}B market value
        """)
    
    with col3:
        st.markdown(f"""
        **Organizations**  
        {latest_data['organizations_using_ai']:.0f}% using AI  
        {latest_data['organizations_planning_to_implement_ai']:.0f}% planning to implement
        """)
    
    with col4:
        st.markdown(f"""
        **Marketing Impact**  
        {latest_data['marketers_believing_ai_improves_email_revenue']:.0f}% see revenue gains  
        Email marketing boost
        """)

if __name__ == "__main__":
    main()