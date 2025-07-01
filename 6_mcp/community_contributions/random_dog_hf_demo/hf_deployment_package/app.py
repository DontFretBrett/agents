#!/usr/bin/env python3
"""
🐕 Random Dog MCP Demo - Hugging Face Deployment
A web interface demonstrating Model Context Protocol with random dog images

Created by Brett Sanders (with the help of AI)
Deployable to Hugging Face Spaces
"""

import gradio as gr
import requests
import json
import asyncio
import time
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RandomDogAPI:
    """Simple wrapper for the random.dog API"""
    
    def __init__(self):
        self.base_url = "https://random.dog/woof.json"
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": datetime.now()
        }
    
    def get_random_dog(self) -> Dict[str, Any]:
        """Get a random dog image from the API"""
        self.stats["total_requests"] += 1
        
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            dog_data = response.json()
            self.stats["successful_requests"] += 1
            
            return {
                "success": True,
                "url": dog_data.get("url", ""),
                "fileSizeBytes": dog_data.get("fileSizeBytes", 0),
                "message": "🐕 Successfully retrieved random dog image!",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        except requests.RequestException as e:
            self.stats["failed_requests"] += 1
            logger.error(f"Request failed: {e}")
            return {
                "success": False,
                "error": f"Failed to fetch random dog: {str(e)}",
                "url": "",
                "fileSizeBytes": 0,
                "message": "❌ Error fetching dog image",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        except json.JSONDecodeError as e:
            self.stats["failed_requests"] += 1
            logger.error(f"JSON decode failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse response: {str(e)}",
                "url": "",
                "fileSizeBytes": 0,
                "message": "❌ Error parsing response",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
    
    def get_stats(self) -> str:
        """Get usage statistics"""
        uptime = datetime.now() - self.stats["start_time"]
        success_rate = (self.stats["successful_requests"] / max(self.stats["total_requests"], 1)) * 100
        
        return f"""
📊 **API Statistics**
- Total Requests: {self.stats["total_requests"]}
- Successful: {self.stats["successful_requests"]}
- Failed: {self.stats["failed_requests"]}
- Success Rate: {success_rate:.1f}%
- Uptime: {str(uptime).split('.')[0]}
        """.strip()

# Initialize the API wrapper
dog_api = RandomDogAPI()

def fetch_random_dog() -> Tuple[Optional[str], str, str]:
    """Fetch a random dog image and return image, info, and stats"""
    try:
        result = dog_api.get_random_dog()
        
        if result["success"] and result["url"]:
            # Format file size
            file_size = result["fileSizeBytes"]
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size} bytes"
            
            info = f"""
🐕 **Random Dog Retrieved!**
- **Time**: {result["timestamp"]}
- **File Size**: {size_str}
- **URL**: {result["url"]}
- **Status**: {result["message"]}
            """.strip()
            
            return result["url"], info, dog_api.get_stats()
        else:
            error_info = f"""
❌ **Error Occurred**
- **Time**: {result["timestamp"]}
- **Error**: {result.get("error", "Unknown error")}
- **Status**: {result["message"]}
            """.strip()
            
            return None, error_info, dog_api.get_stats()
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_info = f"""
❌ **Unexpected Error**
- **Time**: {datetime.now().strftime("%H:%M:%S")}
- **Error**: {str(e)}
        """.strip()
        
        return None, error_info, dog_api.get_stats()

def fetch_multiple_dogs(count: int) -> Tuple[str, str]:
    """Fetch multiple random dogs"""
    count = max(1, min(count, 5))  # Limit between 1 and 5
    
    dogs = []
    for i in range(count):
        result = dog_api.get_random_dog()
        if result["success"]:
            file_size = result["fileSizeBytes"]
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size} bytes"
            
            dogs.append(f"🐕 **Dog {i+1}**: [{size_str}]({result['url']})")
        else:
            dogs.append(f"❌ **Dog {i+1}**: Error - {result.get('error', 'Unknown')}")
        
        # Small delay between requests to be nice to the API
        time.sleep(0.5)
    
    batch_info = f"""
📦 **Batch Request Results** ({count} dogs)
{chr(10).join(dogs)}

**Completed at**: {datetime.now().strftime("%H:%M:%S")}
    """.strip()
    
    return batch_info, dog_api.get_stats()

# Create the Gradio interface
def create_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(
        title="🐕 Random Dog MCP Demo",
        theme=gr.themes.Soft(),
        css="""
        .dog-container { border-radius: 15px; padding: 20px; }
        .stats-container { background-color: #f0f9ff; border-radius: 10px; padding: 15px; }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🐕 Random Dog MCP Demo
        
        **Demonstrating Model Context Protocol with Random Dog Images**
        
        This application showcases how MCP (Model Context Protocol) can be used to fetch and display random dog images. 
        Perfect for testing API integrations and bringing joy to your day! 🎉
        
        ---
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 🎲 Single Random Dog")
                
                fetch_btn = gr.Button(
                    "🐕 Get Random Dog!", 
                    variant="primary", 
                    size="lg"
                )
                
                dog_image = gr.Image(
                    label="Random Dog Image",
                    show_label=True,
                    container=True,
                    height=400
                )
                
                dog_info = gr.Markdown(
                    "Click the button above to fetch a random dog! 🐕",
                    elem_classes=["dog-container"]
                )
            
            with gr.Column(scale=1):
                gr.Markdown("## 📊 Statistics")
                
                stats_display = gr.Markdown(
                    dog_api.get_stats(),
                    elem_classes=["stats-container"]
                )
                
                refresh_stats_btn = gr.Button("🔄 Refresh Stats", size="sm")
        
        gr.Markdown("---")
        
        with gr.Row():
            gr.Markdown("## 📦 Batch Fetch")
            
        with gr.Row():
            with gr.Column():
                count_slider = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                    label="Number of dogs to fetch",
                    info="Fetch multiple dogs at once (1-5)"
                )
                
                batch_btn = gr.Button("📦 Fetch Multiple Dogs!", variant="secondary")
                
                batch_info = gr.Markdown(
                    "Use the slider above to select how many dogs to fetch, then click the button! 🐕",
                    elem_classes=["dog-container"]
                )
        
        gr.Markdown("""
        ---
        
        ## 🔧 About This Demo
        
        This application demonstrates:
        - **API Integration**: Fetching data from external APIs
        - **Error Handling**: Graceful handling of network issues
        - **Statistics Tracking**: Monitoring API usage and success rates
        - **Batch Processing**: Handling multiple requests efficiently
        - **MCP Concepts**: Showcasing Model Context Protocol patterns
        
        **Built with**: Python, Gradio, and the [random.dog](https://random.dog/) API
        
        **Ready for Hugging Face Spaces**: This app can be deployed directly to HF Spaces! 🤗
        """)
        
        # Event handlers
        fetch_btn.click(
            fn=fetch_random_dog,
            outputs=[dog_image, dog_info, stats_display]
        )
        
        batch_btn.click(
            fn=fetch_multiple_dogs,
            inputs=[count_slider],
            outputs=[batch_info, stats_display]
        )
        
        refresh_stats_btn.click(
            fn=lambda: dog_api.get_stats(),
            outputs=[stats_display]
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 