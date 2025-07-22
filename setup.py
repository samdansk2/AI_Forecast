#!/usr/bin/env python3
"""
UV Setup Script for AI Progress Tracker

This script helps set up the project using UV best practices.
Run this script to initialize the project with UV.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a shell command and return success status."""
    print(f"🔄 {description}...")
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:  # Unix-like systems
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command.split()[0]}")
        return False


def check_uv_installation() -> bool:
    """Check if UV is installed."""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✅ UV is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ UV is not installed")
        return False


def install_uv():
    """Install UV package manager."""
    print("📦 Installing UV...")
    
    if os.name == 'nt':  # Windows
        install_cmd = 'powershell -c "irm https://astral.sh/uv/install.ps1 | iex"'
    else:  # Unix-like systems
        install_cmd = 'curl -LsSf https://astral.sh/uv/install.sh | sh'
    
    print(f"Running: {install_cmd}")
    print("Please follow the installation prompts...")
    
    try:
        subprocess.run(install_cmd, shell=True, check=True)
        print("✅ UV installation completed")
        print("📝 Please restart your terminal and run this script again")
        return True
    except subprocess.CalledProcessError:
        print("❌ UV installation failed")
        print("Please install UV manually: https://docs.astral.sh/uv/getting-started/installation/")
        return False


def setup_project():
    """Set up the project with UV."""
    print("🚀 Setting up AI Progress Tracker with UV...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        return False
    
    commands = [
        ("uv sync", "Installing project dependencies"),
        ("uv sync --extra dev", "Installing development dependencies"),
        ("uv sync --extra notebook", "Installing notebook dependencies"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    if success_count == len(commands):
        print("\n🎉 Project setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Activate the virtual environment:")
        if os.name == 'nt':
            print("   .venv\\Scripts\\activate")
        else:
            print("   source .venv/bin/activate")
        print("\n2. Run the application:")
        print("   uv run ai-tracker")
        print("\n3. Start the dashboard:")
        print("   uv run streamlit run dashboard/streamlit_app.py")
        print("\n4. Start Jupyter for notebooks:")
        print("   uv run jupyter lab")
        
        return True
    else:
        print(f"\n⚠️  Setup partially completed ({success_count}/{len(commands)} commands succeeded)")
        return False


def setup_pre_commit():
    """Set up pre-commit hooks."""
    if not Path(".pre-commit-config.yaml").exists():
        print("⚠️  Pre-commit configuration not found, skipping...")
        return True
    
    return run_command("uv run pre-commit install", "Setting up pre-commit hooks")


def main():
    """Main setup function."""
    print("🔧 AI Progress Tracker - UV Setup")
    print("=" * 40)
    
    # Check UV installation
    if not check_uv_installation():
        print("\n📦 UV not found. Installing UV...")
        if install_uv():
            print("\n⚠️  Please restart your terminal and run this script again.")
            return
        else:
            print("\n❌ Setup failed. Please install UV manually and try again.")
            return
    
    # Setup project
    if setup_project():
        # Setup pre-commit hooks
        setup_pre_commit()
        
        print("\n✨ Setup completed! You're ready to start developing.")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
