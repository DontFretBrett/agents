# 🔍 Image Validator

An intelligent image validation application powered by AutoGen and OpenAI's vision models, with a user-friendly Gradio web interface.

## 📋 Overview

This application allows users to upload images and validate them against custom criteria using AI-powered image analysis. Whether you need to verify that an image contains a driver's license, passport, business card, or any other specific content, this tool provides structured validation with detailed feedback.

## ✨ Features

- **🤖 AI-Powered Validation**: Uses AutoGen with GPT-4o-mini vision model for intelligent image analysis
- **📝 Custom Criteria**: Define your own validation requirements in natural language
- **🖼️ Easy Upload**: Drag-and-drop image upload interface
- **📊 Structured Output**: Returns Pydantic-structured results with:
  - Brief description of what was observed
  - Boolean pass/fail validation result
- **🎨 Modern UI**: Clean, responsive Gradio interface
- **⚡ Real-time Processing**: Fast validation with immediate feedback
- **🔧 Error Handling**: Graceful error handling for invalid inputs or processing issues

## 🛠️ Technical Stack

- **AutoGen**: Multi-agent framework for AI validation
- **OpenAI GPT-4o-mini**: Vision-language model for image analysis
- **Gradio**: Web interface framework
- **Pydantic**: Data validation and structured output
- **PIL (Pillow)**: Image processing

## 📦 Requirements

- Python 3.8+
- OpenAI API key
- Dependencies managed via `uv` or `pip`

### Required Environment Variables

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Installation & Setup

### Using UV (Recommended)

1. **Clone/Navigate to the project directory**:
   ```bash
   cd 5_autogen
   ```

2. **Ensure you have your `.env` file** with your OpenAI API key

3. **Run the application**:
   ```bash
   uv run lab2-image-validator.py
   ```

### Using Pip

1. **Install dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Run the application**:
   ```bash
   python lab2-image-validator.py
   ```

## 💻 Usage

1. **Start the application**:
   ```bash
   uv run lab2-image-validator.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://127.0.0.1:7860
   ```

3. **Use the interface**:
   - **Enter validation criteria**: Describe what the image should contain (e.g., "It should be a driver's license")
   - **Upload an image**: Click or drag-and-drop your image file
   - **Click "🔍 Validate Image"**: Process the validation
   - **View results**: See the validation status and detailed analysis

## 📝 Example Validation Criteria

- `"It should be a driver's license"`
- `"It should be a passport"`
- `"It should contain a person's face"`
- `"It should be a business card"`
- `"It should be a receipt or invoice"`
- `"It should show a government-issued ID"`
- `"It should contain text in English"`
- `"It should be a medical prescription"`

## 🏗️ Code Structure

```python
# Core Components:
├── ValidationResult (Pydantic Model)
│   ├── brief_description: str
│   └── passes_validation: bool
├── validator_agent (AutoGen AssistantAgent)
├── validate_image_async() (AI Processing)
├── validate_image() (Gradio Wrapper)
└── create_interface() (UI Setup)
```

### Key Functions

- **`validate_image_async()`**: Core validation logic using AutoGen
- **`validate_image()`**: Synchronous wrapper for Gradio integration  
- **`create_interface()`**: Gradio UI setup and configuration
- **`main()`**: Application entry point and server launch

## 🔧 Configuration

### Model Configuration
The application uses GPT-4o-mini by default. You can modify the model in the code:

```python
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
```

### Server Configuration
Modify the server settings in the `main()` function:

```python
demo.launch(
    server_name="127.0.0.1",  # Change for external access
    server_port=7860,         # Change port if needed
    share=False,              # Set True for public URL
    show_api=False           # Set True to show API docs
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**:
   ```
   Make sure OPENAI_API_KEY is set in your .env file
   ```

2. **Port Already in Use**:
   ```bash
   # Change the port in main() function or kill existing process
   pkill -f "lab2-image-validator.py"
   ```

3. **Dependencies Not Found**:
   ```bash
   # Ensure all dependencies are installed
   uv sync  # or pip install -r ../requirements.txt
   ```

4. **Image Upload Issues**:
   - Ensure image is in supported format (PNG, JPEG, etc.)
   - Check image file size (very large images may cause issues)

### Error Messages

- **"Please provide validation criteria"**: Enter text in the validation criteria field
- **"Please upload an image"**: Select and upload an image file
- **"Error processing image"**: Check your OpenAI API key and internet connection

## 📊 Output Format

The application returns structured validation results:

```json
{
  "brief_description": "The image shows a rectangular ID card with text fields, a photo, and official markings typical of a driver's license.",
  "passes_validation": true
}
```

## 🔒 Security Considerations

- **API Keys**: Keep your OpenAI API key secure and never commit it to version control
- **Image Privacy**: Images are processed through OpenAI's API - ensure compliance with your privacy requirements
- **Local Access**: By default, the server only accepts connections from localhost

## 🤝 Contributing

This is an educational project based on AutoGen examples. Feel free to:

- Add new validation criteria examples
- Improve the UI/UX
- Add support for additional image formats
- Enhance error handling
- Add batch processing capabilities

## 📄 License

This project is part of the AutoGen learning materials and follows the same licensing terms.

## 🙏 Acknowledgments

- Built using [AutoGen](https://github.com/microsoft/autogen) framework
- UI powered by [Gradio](https://gradio.app/)
- Vision capabilities provided by OpenAI's GPT-4o-mini model

---

**Happy Validating! 🎯**

# Image Validator with OpenAI Tracing

An enhanced AutoGen-powered image validation application with comprehensive OpenAI tracing and observability features.

## Features

- **🔍 Image Validation**: Upload images and validate them against custom criteria using AutoGen agents
- **📊 OpenAI Tracing**: Full observability with OpenTelemetry integration
- **🎯 Structured Outputs**: Uses Pydantic models for consistent response formatting
- **🌐 Web Interface**: Clean Gradio interface for easy interaction
- **🔗 Multi-Modal**: Supports both text and image inputs

## OpenAI Tracing Capabilities

This application integrates OpenTelemetry tracing to provide comprehensive observability:

### What Gets Traced

1. **Complete Validation Process**: Each image validation gets a unique trace ID
2. **Agent Interactions**: All AutoGen agent communications and decisions
3. **Model Calls**: OpenAI API calls with request/response details
4. **Performance Metrics**: Execution times, token usage, and resource consumption
5. **Error Tracking**: Detailed error logs with context

### Where to View Traces

- **OpenAI Platform**: Visit [https://platform.openai.com/traces](https://platform.openai.com/traces)
- **Console Logs**: Real-time trace information in your terminal
- **External Services**: Optional integration with Jaeger, Zipkin, or other observability platforms

## Installation

1. **Install Dependencies**:
   ```bash
   uv add autogen-agentchat autogen-ext gradio opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc python-dotenv pillow pydantic
   ```

2. **Environment Setup**:
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python lab2-image-validator.py
   ```

## Usage

### Basic Image Validation

1. Open the web interface at `http://localhost:7860`
2. Enter validation criteria (e.g., "It should be a driver's license")
3. Upload an image
4. Click "🔍 Validate Image (with Tracing)"
5. View results and check console for trace information

### Monitoring Traces

#### OpenAI Platform Traces
- Navigate to [https://platform.openai.com/traces](https://platform.openai.com/traces)
- Filter by your API key and time range
- View detailed execution flows, token usage, and performance metrics

#### Console Monitoring
Watch the console output for:
```
🔍 Starting image validation with trace ID: a1b2c3d4
📊 View traces at: https://platform.openai.com/traces
✅ Validation completed for trace: a1b2c3d4
```

## Advanced Configuration

### External Tracing Backends

To send traces to external services like Jaeger:

1. **Start Jaeger** (using Docker):
   ```bash
   docker run -d --name jaeger \
     -e COLLECTOR_OTLP_ENABLED=true \
     -p 16686:16686 \
     -p 4317:4317 \
     -p 4318:4318 \
     jaegertracing/all-in-one:latest
   ```

2. **Enable OTLP Export** in the code:
   ```python
   # Uncomment these lines in setup_tracing()
   otel_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
   span_processor = BatchSpanProcessor(otel_exporter)
   tracer_provider.add_span_processor(span_processor)
   ```

3. **View Traces** at `http://localhost:16686`

### Custom Span Attributes

The application automatically adds these trace attributes:
- `validation.criteria`: The validation criteria text
- `validation.trace_id`: Unique identifier for tracking
- `image.format`: Image file format
- `image.size`: Image dimensions
- `agent.name`: AutoGen agent identifier
- `agent.model`: LLM model being used
- `validation.result`: Pass/fail result
- `validation.description`: Brief description (truncated)

## Trace Analysis

### Performance Monitoring
- **Latency**: Track how long validations take
- **Token Usage**: Monitor OpenAI API consumption
- **Error Rates**: Identify common failure patterns
- **Agent Decision Paths**: Understand how agents reason

### Debugging Workflows
- **Step-by-Step Execution**: See exactly what the agent is doing
- **Error Context**: Full stack traces with validation context
- **Input/Output Tracking**: Monitor what data flows through the system
- **Resource Usage**: Track memory and CPU consumption

### Business Intelligence
- **Usage Patterns**: Understand how users interact with the system
- **Validation Success Rates**: Track accuracy over time
- **Common Criteria**: Identify frequently used validation patterns
- **Performance Trends**: Monitor system performance changes

## Architecture

```
User Interface (Gradio)
    ↓
Validation Controller
    ↓
AutoGen Agent (with tracing)
    ↓
OpenAI API (GPT-4o-mini)
    ↓
OpenTelemetry Tracing
    ↓
Multiple Backends:
- OpenAI Platform
- Console Logs  
- Jaeger (optional)
- Custom OTLP endpoints
```

## Troubleshooting

### Common Issues

1. **Missing Traces in OpenAI Platform**:
   - Verify your `OPENAI_API_KEY` is correct
   - Ensure you're using an OpenAI model (not local/other providers)
   - Check that API calls are actually being made

2. **Console Logging Not Working**:
   - Check that logging is properly configured
   - Verify `TRACE_LOGGER_NAME` import is correct
   - Ensure log level is set to DEBUG

3. **External Tracing Not Working**:
   - Verify OTLP endpoint is accessible
   - Check firewall settings
   - Ensure the external service is running

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tracing for new features following OpenTelemetry conventions
4. Test with multiple tracing backends
5. Submit a pull request

## License

This project follows the same license as the AutoGen agents repository.

## Related Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [OpenAI Platform Traces](https://platform.openai.com/docs/guides/observability)
- [Gradio Documentation](https://gradio.app/docs/) 