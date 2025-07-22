"""
Visualization Module for AI Progress Tracker

This module provides functionality for creating charts, graphs, and
interactive visualizations of AI development data and trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from typing import Dict, List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class AIDataVisualizer:
    """Class for creating AI data visualizations."""
    
    def __init__(self, output_dir: str = "results/plot"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_trend_analysis(self, data: pd.DataFrame, save: bool = True) -> None:
        """Create trend analysis plots."""
        logger.info("Creating trend analysis visualization...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('AI Progress Trend Analysis', fontsize=16)
        
        # Sample plots (replace with actual data visualization)
        x = range(len(data)) if not data.empty else range(10)
        y = pd.Series(range(len(data))).cumsum() if not data.empty else pd.Series(range(10)).cumsum()
        
        # Plot 1: Line trend
        axes[0, 0].plot(x, y)
        axes[0, 0].set_title('AI Development Timeline')
        axes[0, 0].set_xlabel('Time Period')
        axes[0, 0].set_ylabel('Progress Index')
        
        # Plot 2: Bar chart
        axes[0, 1].bar(x[:10], y[:10])
        axes[0, 1].set_title('Recent AI Milestones')
        axes[0, 1].set_xlabel('Milestone')
        axes[0, 1].set_ylabel('Impact Score')
        
        # Plot 3: Scatter plot
        axes[1, 0].scatter(x, y, alpha=0.6)
        axes[1, 0].set_title('Innovation Distribution')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Innovation Rate')
        
        # Plot 4: Histogram
        axes[1, 1].hist(y, bins=20, alpha=0.7)
        axes[1, 1].set_title('Progress Distribution')
        axes[1, 1].set_xlabel('Progress Value')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / "trend_analysis.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Trend analysis plot saved to {output_path}")
        
        plt.show()
    
    def create_interactive_dashboard(self, data: pd.DataFrame) -> go.Figure:
        """Create interactive dashboard using Plotly."""
        logger.info("Creating interactive dashboard...")
        
        # Sample interactive plot
        if data.empty:
            # Generate sample data for demonstration
            dates = pd.date_range('2020-01-01', periods=50, freq='M')
            values = pd.Series(range(50)).cumsum() + pd.Series(range(50)).apply(lambda x: x**0.5)
        else:
            dates = data.index if hasattr(data, 'index') else range(len(data))
            values = data.iloc[:, 0] if not data.empty else []
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name='AI Progress',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Interactive AI Progress Dashboard',
            xaxis_title='Time Period',
            yaxis_title='Progress Metric',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def generate_report_charts(self, data: pd.DataFrame) -> List[str]:
        """Generate multiple charts for reporting."""
        logger.info("Generating report charts...")
        
        chart_paths = []
        
        # Chart 1: Progress over time
        plt.figure(figsize=(12, 6))
        if not data.empty:
            plt.plot(data.index, data.iloc[:, 0])
        else:
            plt.plot(range(10), range(10))
        plt.title('AI Progress Over Time')
        plt.xlabel('Time')
        plt.ylabel('Progress Metric')
        
        chart_path = self.output_dir / "progress_timeline.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        chart_paths.append(str(chart_path))
        plt.close()
        
        # Chart 2: Distribution analysis
        plt.figure(figsize=(10, 6))
        if not data.empty and len(data.columns) > 0:
            data.iloc[:, 0].hist(bins=20, alpha=0.7)
        else:
            pd.Series(range(20)).hist(bins=10, alpha=0.7)
        plt.title('Progress Distribution')
        plt.xlabel('Progress Value')
        plt.ylabel('Frequency')
        
        chart_path = self.output_dir / "progress_distribution.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        chart_paths.append(str(chart_path))
        plt.close()
        
        logger.info(f"Generated {len(chart_paths)} report charts")
        return chart_paths


def create_visualization_suite(data_path: Optional[str] = None) -> Dict:
    """Create a complete suite of visualizations."""
    logger.info("Creating visualization suite...")
    
    try:
        # Initialize visualizer
        visualizer = AIDataVisualizer()
        
        # Load data
        if data_path and Path(data_path).exists():
            data = pd.read_csv(data_path)
            logger.info(f"Loaded data from {data_path}")
        else:
            # Generate sample data for demonstration
            data = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=100, freq='D'),
                'progress': pd.Series(range(100)).cumsum() + pd.Series(range(100)).apply(lambda x: x**0.5)
            })
            data.set_index('date', inplace=True)
            logger.info("Using sample data for visualization")
        
        # Create visualizations
        visualizer.plot_trend_analysis(data)
        interactive_fig = visualizer.create_interactive_dashboard(data)
        chart_paths = visualizer.generate_report_charts(data)
        
        # Save interactive plot
        interactive_path = visualizer.output_dir / "interactive_dashboard.html"
        interactive_fig.write_html(str(interactive_path))
        
        results = {
            "static_charts": len(chart_paths),
            "chart_paths": chart_paths,
            "interactive_dashboard": str(interactive_path),
            "data_shape": data.shape
        }
        
        logger.info("Visualization suite created successfully!")
        return results
        
    except Exception as e:
        logger.error(f"Error creating visualization suite: {e}")
        raise


def main():
    """Main entry point for visualization module."""
    logger.info("Starting AI data visualization process...")
    
    try:
        results = create_visualization_suite()
        
        print("Visualization module initialized.")
        print(f"Created {results['static_charts']} static charts")
        print(f"Interactive dashboard: {results['interactive_dashboard']}")
        print(f"Data shape: {results['data_shape']}")
        
        logger.info("Visualization process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during visualization: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()