---
title: Random Dog MCP Demo
emoji: 🐕
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
license: mit
---

# 🐕 Random Dog MCP Demo - Hugging Face Deployment

**A web interface demonstrating Model Context Protocol (MCP) with random dog images**

*Created by [Brett Sanders](https://brettsanders.com) (with the help of AI)*

[![Deploy to Hugging Face](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-sm.svg)](https://huggingface.co/spaces)

## 🎯 Overview

This application demonstrates the concepts of Model Context Protocol (MCP) through a fun and interactive web interface that fetches random dog images. While the original MCP implementation uses separate server/client processes, this version adapts the concepts for web deployment.

## ✨ Features

- 🐕 **Single Dog Fetch**: Get one random dog image with detailed metadata
- 📦 **Batch Processing**: Fetch multiple dogs at once (1-5 dogs)
- 📊 **Real-time Statistics**: Track API usage, success rates, and uptime
- 🎨 **Beautiful UI**: Modern Gradio interface with custom styling
- ⚡ **Error Handling**: Graceful handling of network issues and API failures
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Deploy to Hugging Face Spaces

### Option 1: Direct Deployment

1. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
2. **Choose Gradio as the SDK**
3. **Upload these files**:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. **Your Space will automatically build and deploy!**

### Option 2: Clone and Deploy

```bash
# Clone your space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy the files
cp /path/to/this/demo/* .

# Commit and push
git add .
git commit -m "Add Random Dog MCP Demo"
git push
```

## 🏃‍♂️ Local Development

### Prerequisites

- Python 3.8+
- pip or conda

### Setup

```bash
# Clone or download this directory
cd random_dog_hf_demo

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at `http://localhost:7860`

## 📂 Project Structure

```
random_dog_hf_demo/
├── app.py              # Main Gradio application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

### Architecture

- **Frontend**: Gradio web interface
- **Backend**: Python with requests for API calls
- **API**: [random.dog](https://random.dog/) public API
- **Deployment**: Hugging Face Spaces compatible

### Key Components

1. **RandomDogAPI Class**: Wrapper for the random.dog API with error handling and statistics
2. **Gradio Interface**: Interactive web UI with multiple fetch modes
3. **Statistics Tracking**: Real-time monitoring of API usage
4. **Error Handling**: Comprehensive error management for robust operation

### MCP Concepts Demonstrated

- **Tool-like Functions**: `get_random_dog()` mimics MCP tool patterns
- **Structured Responses**: Consistent data format with metadata
- **Error Handling**: Graceful failure management
- **Batch Operations**: Multiple tool calls in sequence
- **Statistics**: Monitoring and observability

## 🎨 Customization

### Styling

The app uses custom CSS for enhanced visual appeal:

```css
.dog-container { border-radius: 15px; padding: 20px; }
.stats-container { background-color: #f0f9ff; border-radius: 10px; padding: 15px; }
```

### Adding Features

You can easily extend the app by:

- Adding more API endpoints (cats, other animals)
- Implementing image filters or processing
- Adding user favorites or history
- Integrating with other MCP servers

## 📊 API Usage

The app uses the free [random.dog API](https://random.dog/):

- **Endpoint**: `https://random.dog/woof.json`
- **Rate Limiting**: Be respectful, includes small delays for batch requests
- **Response Format**: JSON with `url` and `fileSizeBytes`

## 🐛 Troubleshooting

### Common Issues

1. **App won't start**: Check that all dependencies are installed
2. **Images not loading**: Check internet connection and API status
3. **Deploy fails**: Ensure all files are uploaded and requirements.txt is correct

### Logs

Check the Hugging Face Spaces logs for detailed error information.

## 🤝 Contributing

Want to improve this demo? Feel free to:

- Add new features
- Improve the UI/UX
- Add more APIs
- Enhance error handling
- Add tests

## 📜 License

This project is open source and available under the MIT License.

## 🔗 Related Projects

- [Original MCP Implementation](../random_dog_mcp_server_client/) - Full MCP server/client
- [MCP Tutorial Notebook](../random_dog_mcp_server_client/random_dog_tutorial.ipynb) - Interactive tutorial

## 🎉 Acknowledgments

- [random.dog](https://random.dog/) for the amazing API
- [Gradio](https://gradio.app/) for the fantastic web framework
- [Hugging Face](https://huggingface.co/) for free hosting
- The AI community for inspiration and feedback

---

**Ready to deploy? Click the badge at the top to get started! 🚀** 