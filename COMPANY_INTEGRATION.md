# Company Integration Guide

This guide explains how to use the adapted aider package with your company's OAuth2 authentication system for Azure OpenAI.

## Overview

The aider package has been adapted to work with your company's authentication infrastructure, which uses:
- OAuth2 client credentials flow
- Azure OpenAI through APIGEE endpoint
- httpx-auth for authentication
- Environment variables for configuration

## Installation

1. Install the required dependencies:
```bash
pip install httpx-auth python-dotenv
```

2. The package already includes the necessary OpenAI and httpx dependencies.

## Environment Setup

Create a `.env` file in your project root with the following variables:

```env
# Company OAuth2 Authentication
OIDC_ENDPOINT=your_oidc_endpoint_here
OIDC_CLIENT_ID=your_client_id_here
OIDC_CLIENT_SECRET=your_client_secret_here
OIDC_SCOPE=your_scope_here
APIGEE_ENDPOINT=your_apigee_endpoint_here

# Azure OpenAI Configuration
AZURE_AOAI_API_VERSION=2025-04-01-preview
AZURE_AOAI_DEPLOYMENT=gpt5
```

**Important**: Replace the placeholder values with your actual company credentials.

## Usage Options

### Option 1: Drop-in Replacement (Recommended)

Use `CompanyModel` as a drop-in replacement for the standard `Model` class:

```python
from aider.company_models import CompanyModel

# Create a model instance that automatically uses company auth
model = CompanyModel("gpt5", verbose=True)

# Use it exactly like the standard Model class
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Help me write a Python function."}
]

hash_obj, response = model.send_completion(
    messages=messages,
    functions=None,
    stream=False
)

print(response.choices[0].message.content)
```

### Option 2: Direct API Calls

Use the convenience functions for direct API calls:

```python
from aider.company_models import simple_api_call_high_reasoning

# Simple API call with reasoning
response = simple_api_call_high_reasoning(
    prompt="Explain how quicksort works",
    model="gpt5",
    max_tokens=800
)
print(response)
```

### Option 3: Image Processing

Process images with text prompts:

```python
from aider.company_models import process_image_with_text

# Analyze an image
response = process_image_with_text(
    image_path="./document.jpg",
    prompt="Extract all text from this document",
    model="gpt5"
)
print(response)
```

### Option 4: Direct Authentication

Use the authentication module directly:

```python
from aider.company_auth import authenticate, simple_api_call_high_reasoning

# Get authenticated client
client = authenticate()

# Use client directly
response = client.chat.completions.create(
    model="gpt5",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    reasoning_effort="medium"
)
```

## Integration with Existing Aider Workflow

### Method 1: Modify Main Entry Point

To use company authentication throughout aider, you can modify the main entry point:

```python
# In your main script or aider configuration
import os
from aider.company_models import CompanyModel
from aider import main

# Set environment variables if not in .env
os.environ["OIDC_ENDPOINT"] = "your_endpoint"
# ... other variables

# Use CompanyModel instead of standard Model
# This requires modifying aider's model creation logic
```

### Method 2: Environment Variable Detection

The `CompanyModel` automatically detects if company authentication is configured:

```python
from aider.company_models import CompanyModel

# This will use company auth if env vars are set, otherwise standard auth
model = CompanyModel("gpt-4o")
```

## Features

### Automatic Fallback
- If company environment variables are not set, the model falls back to standard authentication
- No code changes needed when switching between environments

### Reasoning Support
- Automatic reasoning effort configuration for GPT-5 models
- Support for `max_completion_tokens` parameter

### Error Handling
- Automatic client reset and retry on authentication failures
- Comprehensive error messages for missing configuration

### Structured Outputs
- Full support for Pydantic models and function calling
- Compatible with existing aider structured output features

## Example: Complete Workflow

```python
import os
from aider.company_models import CompanyModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Create company model
    model = CompanyModel("gpt5", verbose=True)
    
    # Check if company auth is configured
    if not model.use_company_auth:
        print("Company auth not configured, using standard auth")
        return
    
    # Use for code assistance
    messages = [
        {"role": "system", "content": "You are an expert Python developer."},
        {"role": "user", "content": "Write a function to parse CSV files with error handling."}
    ]
    
    hash_obj, response = model.send_completion(
        messages=messages,
        functions=None,
        stream=False,
        temperature=0.1
    )
    
    print("Generated code:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

## Testing

Run the provided example to test your setup:

```bash
python examples/company_usage_example.py
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Ensure all required variables are set in your `.env` file
   - Check variable names match exactly (case-sensitive)

2. **Authentication Failures**
   - Verify your OAuth2 credentials are correct
   - Check network connectivity to OIDC and APIGEE endpoints
   - Ensure your client has the necessary scopes

3. **SSL Certificate Issues**
   - The current configuration uses `verify=False` for development
   - For production, set `verify=True` and ensure proper certificates

4. **Model Not Found**
   - Verify your `AZURE_AOAI_DEPLOYMENT` matches your actual deployment name
   - Check that the deployment is available in your Azure OpenAI instance

### Debug Mode

Enable verbose logging to troubleshoot issues:

```python
model = CompanyModel("gpt5", verbose=True)
```

This will print detailed information about API calls and authentication.

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **SSL Verification**: Enable SSL verification in production environments
3. **Credential Rotation**: Regularly rotate OAuth2 client credentials
4. **Network Security**: Ensure secure connections to company endpoints

## Migration from Standard Aider

To migrate existing aider code to use company authentication:

1. Replace `Model` imports with `CompanyModel`
2. Set up environment variables
3. Test with a simple example
4. Gradually migrate existing workflows

The adapted package maintains full compatibility with existing aider APIs, making migration straightforward.
