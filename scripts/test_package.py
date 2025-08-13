#!/usr/bin/env python3
"""
Test package functionality before publishing
"""

import sys
import subprocess
import tempfile
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """Run command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd
        )
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False, e.stderr

def test_local_install():
    """Test local installation of the package."""
    print("📦 Testing local package installation...\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Install package in development mode
        success, _ = run_command(
            "pip install -e .", 
            "Installing package in development mode"
        )
        if not success:
            return False
        
        # Test Python import
        test_script = temp_path / "test_import.py"
        test_script.write_text("""
import telegram_stars_rates
print(f"Version: {telegram_stars_rates.__version__}")
print(f"Available functions: {telegram_stars_rates.__all__}")

# Test basic functionality (without API calls)
from telegram_stars_rates import get_stars_rate
print("✅ Import successful!")
""")
        
        success, output = run_command(
            f"python {test_script}",
            "Testing Python imports"
        )
        if not success:
            return False
        
        # Test CLI command
        success, output = run_command(
            "telegram-stars-rates --help",
            "Testing CLI command"
        )
        if not success:
            return False
        
        print("✅ Local package test passed!")
        return True

def test_build_package():
    """Test package building process."""
    print("\n🔨 Testing package build...\n")
    
    # Clean previous builds
    run_command("rm -rf build dist *.egg-info", "Cleaning build artifacts")
    
    # Install build dependencies
    success, _ = run_command(
        "pip install --upgrade build twine",
        "Installing build dependencies"
    )
    if not success:
        return False
    
    # Build package
    success, _ = run_command(
        "python -m build",
        "Building package"
    )
    if not success:
        return False
    
    # Check built package
    success, _ = run_command(
        "python -m twine check dist/*",
        "Checking built package"
    )
    if not success:
        return False
    
    # List built files
    dist_files = list(Path('dist').glob('*'))
    print(f"\n📦 Built files:")
    for file in dist_files:
        size_kb = file.stat().st_size / 1024
        print(f"   - {file.name} ({size_kb:.1f} KB)")
    
    print("✅ Package build test passed!")
    return True

def main():
    """Run all tests."""
    print("🧪 Testing telegram-stars-rates package...\n")
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ pyproject.toml not found. Run from project root directory.")
        sys.exit(1)
    
    success = True
    
    # Test local installation
    if not test_local_install():
        success = False
    
    # Test package building
    if not test_build_package():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Package is ready for PyPI upload.")
        print("\n📋 Next steps:")
        print("   1. Run: python scripts/build_and_upload.py")
        print("   2. Or manually: python -m twine upload dist/*")
    else:
        print("\n❌ Some tests failed. Please fix issues before publishing.")
        sys.exit(1)

if __name__ == "__main__":
    main()