#!/usr/bin/env python3
"""
AI Progress Tracker - Main Application Entry Point

This module provides the main entry point for the AI Progress Tracker application.
It orchestrates data collection, analysis, prediction, and visualization components.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path and import config
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    import config
except ImportError:
    # Fallback config if module doesn't exist
    class config:
        PROJECT_NAME = "AI Progress Tracker"
        VERSION = "1.0.0"


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('ai_tracker.log')
        ]
    )


def main() -> None:
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="AI Progress Tracker - Analyze and visualize AI development trends"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--mode",
        choices=["collect", "analyze", "predict", "visualize", "all"],
        default="all",
        help="Operation mode (default: all)"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting {config.PROJECT_NAME} v{config.VERSION}")
    
    try:
        if args.mode in ["collect", "all"]:
            logger.info("Starting data collection...")
            # Import and run data collection
            try:
                from data_collector import main as collect_main  # type: ignore
                collect_main()
                logger.info("Data collection completed successfully")
            except ImportError:
                logger.warning("Data collector module not found")
        
        if args.mode in ["analyze", "all"]:
            logger.info("Starting data analysis...")
            try:
                from analyzer import main as analyze_main  # type: ignore
                analyze_main()
                logger.info("Data analysis completed successfully")
            except ImportError:
                logger.warning("Analyzer module not found")
        
        if args.mode in ["predict", "all"]:
            logger.info("Starting prediction...")
            try:
                from predictor import main as predict_main  # type: ignore
                predict_main()
                logger.info("Prediction completed successfully")
            except ImportError:
                logger.warning("Predictor module not found")
        
        if args.mode in ["visualize", "all"]:
            logger.info("Starting visualization...")
            try:
                from visualizations import main as viz_main  # type: ignore
                viz_main()
                logger.info("Visualization completed successfully")
            except ImportError:
                logger.warning("Visualizations module not found")
        
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()