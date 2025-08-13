#!/usr/bin/env python3
"""
Build and upload script for PyPI distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def clean_build():
    """Clean previous build artifacts."""
    build_dirs = ['build', 'dist', '*.egg-info']
    for pattern in build_dirs:
        for path in Path('.').glob(pattern):
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"   Removed directory: {path}")
                else:
                    path.unlink()
                    print(f"   Removed file: {path}")

def main():
    """Main build and upload process."""
    print("🚀 Starting PyPI build and upload process...\n")
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ pyproject.toml not found. Run from project root directory.")
        sys.exit(1)
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    clean_build()
    
    # Install/upgrade build dependencies
    if not run_command("python -m pip install --upgrade pip build twine", "Installing/upgrading build tools"):
        sys.exit(1)
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        sys.exit(1)
    
    # Check the built package
    if not run_command("python -m twine check dist/*", "Checking built package"):
        sys.exit(1)
    
    print("\n✅ Package built successfully!")
    
    # List built files
    dist_files = list(Path('dist').glob('*'))
    print(f"📦 Built files:")
    for file in dist_files:
        print(f"   - {file.name} ({file.stat().st_size} bytes)")
    
    # Ask for upload confirmation
    response = input("\n🚀 Upload to PyPI? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Upload cancelled. Files are ready in dist/ directory.")
        print("To upload manually: python -m twine upload dist/*")
        return
    
    # Upload to PyPI
    print("\n📤 Uploading to PyPI...")
    if not run_command("python -m twine upload dist/*", "Uploading to PyPI"):
        print("\n❌ Upload failed!")
        print("Make sure you have:")
        print("  1. PyPI account with permissions")
        print("  2. API token configured: pip install keyring, then twine upload")
        print("  3. Or use: python -m twine upload dist/* --username __token__ --password <your-token>")
        sys.exit(1)
    
    print("\n🎉 Package uploaded successfully to PyPI!")
    print("🔗 Check it out: https://pypi.org/project/telegram-stars-rates/")

if __name__ == "__main__":
    main()