"""
Example usage of the adapted aider package with company OAuth2 authentication.

This example demonstrates how to use the aider package with your company's
Azure OpenAI authentication system using OAuth2 client credentials.
"""

import os
from aider.company_models import CompanyModel, simple_api_call_high_reasoning, process_image_with_text
from aider.company_auth import PersonProfile, CalendarEvent

# Example 1: Using the CompanyModel class directly
def example_company_model():
    """Example of using CompanyModel for code assistance."""
    print("=== Example 1: Using CompanyModel ===")
    
    # Create a company model instance
    model = CompanyModel("gpt5", verbose=True)  # Uses your company's GPT-5 deployment
    
    # Example messages for code assistance
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
    ]
    
    # Send completion request
    hash_obj, response = model.send_completion(
        messages=messages,
        functions=None,
        stream=False,
        temperature=0.1
    )
    
    print("Response:", response.choices[0].message.content)
    print()


# Example 2: Simple API call with high reasoning
def example_simple_reasoning():
    """Example of simple API call with reasoning."""
    print("=== Example 2: Simple API Call with High Reasoning ===")
    
    prompt = "Explain in 5 steps why the sum of the first n odd numbers equals n^2."
    model = "gpt5"  # Your company's deployment name
    
    response = simple_api_call_high_reasoning(prompt, model, max_tokens=800)
    print("Response:", response)
    print()


# Example 3: Image processing
def example_image_processing():
    """Example of processing an image with text."""
    print("=== Example 3: Image Processing ===")
    
    # Note: Make sure you have an image file at this path
    image_path = "./example_image.jpg"
    
    if os.path.exists(image_path):
        prompt = "Extract the information in plain text"
        model = "gpt5"
        
        response = process_image_with_text(image_path, prompt, model)
        print("Image analysis:", response)
    else:
        print(f"Image file not found at {image_path}")
    print()


# Example 4: Using structured outputs with Pydantic models
def example_structured_output():
    """Example of using structured outputs with company authentication."""
    print("=== Example 4: Structured Output ===")
    
    model = CompanyModel("gpt5", verbose=True)
    
    # Example prompt for structured data extraction
    messages = [
        {"role": "system", "content": "Extract person information from the text."},
        {"role": "user", "content": "John Doe is a 25-year-old student who enjoys programming, reading, and hiking."}
    ]
    
    # You can extend this to use function calling for structured outputs
    hash_obj, response = model.send_completion(
        messages=messages,
        functions=None,
        stream=False
    )
    
    print("Structured response:", response.choices[0].message.content)
    print()


# Example 5: Environment variable setup guide
def print_environment_setup():
    """Print the required environment variables for company authentication."""
    print("=== Environment Variables Setup ===")
    print("Create a .env file in your project root with the following variables:")
    print()
    print("# Company OAuth2 Authentication")
    print("OIDC_ENDPOINT=your_oidc_endpoint_here")
    print("OIDC_CLIENT_ID=your_client_id_here")
    print("OIDC_CLIENT_SECRET=your_client_secret_here")
    print("OIDC_SCOPE=your_scope_here")
    print("APIGEE_ENDPOINT=your_apigee_endpoint_here")
    print("AZURE_AOAI_API_VERSION=2025-04-01-preview")
    print("AZURE_AOAI_DEPLOYMENT=gpt5")
    print()
    print("Make sure to replace the placeholder values with your actual company credentials.")
    print()


def main():
    """Main function to run all examples."""
    print("Company Aider Package Usage Examples")
    print("=" * 50)
    print()
    
    # Check if environment variables are set
    required_vars = ["OIDC_ENDPOINT", "OIDC_CLIENT_ID", "OIDC_CLIENT_SECRET", "OIDC_SCOPE", "APIGEE_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("⚠️  Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print_environment_setup()
        return
    
    print("✅ All required environment variables are set!")
    print()
    
    try:
        # Run examples
        example_company_model()
        example_simple_reasoning()
        example_image_processing()
        example_structured_output()
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Please check your environment variables and network connectivity.")


if __name__ == "__main__":
    main()
