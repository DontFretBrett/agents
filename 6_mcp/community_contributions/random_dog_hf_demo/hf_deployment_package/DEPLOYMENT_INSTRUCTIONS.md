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