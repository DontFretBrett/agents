#!/usr/bin/env python3
"""
Deployment helper script for Random Dog MCP Demo
Helps prepare and validate files for Hugging Face Spaces deployment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    try:
        import gradio
        print(f"✅ Gradio {gradio.__version__} installed")
    except ImportError:
        print("❌ Gradio not installed. Run: pip install gradio")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__} installed")
    except ImportError:
        print("❌ Requests not installed. Run: pip install requests")
        return False
    
    return True

def validate_files():
    """Validate that all required files exist"""
    print("\n📂 Validating files...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_app():
    """Test the application locally"""
    print("\n🧪 Testing application...")
    
    try:
        # Import and test the app without running the interface
        from app import RandomDogAPI, fetch_random_dog
        
        # Quick API test
        api = RandomDogAPI()
        result = api.get_random_dog()
        
        if result['success']:
            print("✅ App test passed - API working correctly")
            return True
        else:
            print(f"❌ App test failed - API error: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ App test failed - Import error: {e}")
        return False

def create_hf_space_files():
    """Create additional files needed for Hugging Face Spaces"""
    print("\n📝 Creating Hugging Face Space files...")
    
    # Create .gitignore if it doesn't exist
    gitignore_content = """
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

.DS_Store
""".strip()
    
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")
    else:
        print("✅ .gitignore already exists")
    
    # Create app_header.md for Hugging Face Space description
    header_content = """---
title: Random Dog MCP Demo
emoji: 🐕
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
"""
    
    if not os.path.exists("app_header.md"):
        with open("app_header.md", "w") as f:
            f.write(header_content)
        print("✅ Created app_header.md (copy this to your Space's README front matter)")
    else:
        print("✅ app_header.md already exists")

def create_deployment_package():
    """Create a deployment package"""
    print("\n📦 Creating deployment package...")
    
    package_dir = "hf_deployment_package"
    
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copy essential files
    files_to_copy = [
        "app.py",
        "requirements.txt", 
        "README.md",
        ".gitattributes"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✅ Copied {file}")
    
    # Create deployment instructions
    instructions = """
# Deployment Instructions

1. Create a new Space on Hugging Face: https://huggingface.co/spaces
2. Choose "Gradio" as the SDK
3. Upload all files from this package to your Space
4. Your Space will automatically build and deploy!

Files in this package:
- app.py: Main application
- requirements.txt: Dependencies
- README.md: Documentation
- .gitattributes: Git LFS configuration (for HF Spaces)

## Testing Locally

Before deploying, you can test locally:

```bash
pip install -r requirements.txt
python app.py
```

Then visit http://localhost:7860

## Troubleshooting

If deployment fails:
1. Check the logs in your Hugging Face Space
2. Ensure all files were uploaded correctly
3. Verify requirements.txt has correct package versions
"""
    
    with open(os.path.join(package_dir, "DEPLOYMENT_INSTRUCTIONS.md"), "w") as f:
        f.write(instructions.strip())
    
    print(f"✅ Created deployment package in '{package_dir}' directory")
    print(f"📂 Package contains {len(os.listdir(package_dir))} files")

def main():
    """Main deployment preparation function"""
    print("🐕 Random Dog MCP Demo - Deployment Helper")
    print("=" * 50)
    
    steps = [
        ("Dependencies Check", check_dependencies),
        ("File Validation", validate_files),
        ("App Testing", test_app),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ {step_name} failed. Please fix the issues and try again.")
            return False
        
    # Create additional files
    create_hf_space_files()
    create_deployment_package()
    
    print("\n" + "=" * 50)
    print("🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Check the 'hf_deployment_package' directory")
    print("2. Create a new Hugging Face Space")
    print("3. Upload the files from the package")
    print("4. Watch your app deploy automatically! 🚀")
    print("\n🔗 Create a Space: https://huggingface.co/spaces")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 