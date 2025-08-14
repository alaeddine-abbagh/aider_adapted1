"""
Company-specific authentication module for Azure OpenAI with OAuth2 client credentials.
This module provides authentication functionality compatible with the company's API infrastructure.
"""

import os
import httpx
import json
import base64
from typing import Optional, List
from openai import AzureOpenAI
from dotenv import load_dotenv
from httpx_auth import OAuth2ClientCredentials
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Company-specific environment variables
OIDC_ENDPOINT = os.environ.get("OIDC_ENDPOINT")
OIDC_CLIENT_ID = os.environ.get("OIDC_CLIENT_ID")
OIDC_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET")
OIDC_SCOPE = os.environ.get("OIDC_SCOPE")
APIGEE_ENDPOINT = os.environ.get("APIGEE_ENDPOINT")
AZURE_AOAI_API_VERSION = os.environ.get("AZURE_AOAI_API_VERSION", "2025-04-01-preview")
AZURE_AOAI_DEPLOYMENT = os.environ.get("AZURE_AOAI_DEPLOYMENT", "gpt5")
AZURE_AOAI_DEPLOYMENT_MINI = os.environ.get("AZURE_AOAI_DEPLOYMENT_MINI", "gpt5mini")
AZURE_AOAI_DEPLOYMENT_NANO = os.environ.get("AZURE_AOAI_DEPLOYMENT_NANO", "gpt5nano")


class PersonProfile(BaseModel):
    """Example structured model for person profiles."""
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    interests: List[str] = Field(description="List of the person's interests")
    is_student: bool = Field(description="Whether the person is currently a student")


class CalendarEvent(BaseModel):
    """Example structured model for calendar events."""
    name: str
    date: str
    participants: List[str]


def authenticate() -> AzureOpenAI:
    """
    Authenticate using OAuth2 client credentials and return an Azure OpenAI client.
    
    Returns:
        AzureOpenAI: Authenticated Azure OpenAI client
        
    Raises:
        ValueError: If required environment variables are missing
    """
    # Validate required environment variables
    required_vars = {
        "OIDC_ENDPOINT": OIDC_ENDPOINT,
        "OIDC_CLIENT_ID": OIDC_CLIENT_ID,
        "OIDC_CLIENT_SECRET": OIDC_CLIENT_SECRET,
        "OIDC_SCOPE": OIDC_SCOPE,
        "APIGEE_ENDPOINT": APIGEE_ENDPOINT,
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Create OAuth2 HTTP client
    oauth2_httpclient = httpx.Client(
        verify=False  # NOTE: consider verify=True in production
    )
    
    # Set up OAuth2 client credentials authentication
    auth = OAuth2ClientCredentials(
        OIDC_ENDPOINT,
        client_id=OIDC_CLIENT_ID,
        client_secret=OIDC_CLIENT_SECRET,
        scope=OIDC_SCOPE,
        client=oauth2_httpclient,
    )
    
    # Fetch token now (httpx_auth attaches it automatically)
    auth.request_new_token()
    
    # Create Azure OpenAI client with OAuth2 authentication
    client = AzureOpenAI(
        api_version=AZURE_AOAI_API_VERSION,
        azure_endpoint=APIGEE_ENDPOINT,
        api_key="FAKE_KEY",  # placeholder; OAuth2 via httpx_auth is used
        http_client=httpx.Client(auth=auth, verify=False),
    )
    
    return client


def simple_api_call_high_reasoning(
    prompt: str, model: str, max_tokens: int = 800
) -> str:
    """
    Simple chat call to GPT-5 with high reasoning effort.
    
    Args:
        prompt: The user prompt
        model: The model deployment name
        max_tokens: Maximum completion tokens
        
    Returns:
        str: The model's response content
    """
    client = authenticate()
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Think step-by-step and be precise.",
        },
        {"role": "user", "content": prompt},
    ]
    
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        reasoning_effort="medium",  # key setting for reasoning
        max_completion_tokens=max_tokens,  # Chat Completions uses *completion* tokens
    )
    
    return resp.choices[0].message.content


def encode_image(image_path: str) -> str:
    """
    Encode an image file to base64 string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Base64 encoded image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def process_image_with_text(image_path: str, prompt: str, model: str) -> str:
    """
    Process an image with text prompt using the authenticated client.
    
    Args:
        image_path: Path to the image file
        prompt: Text prompt for image analysis
        model: The model deployment name
        
    Returns:
        str: The model's response content
    """
    client = authenticate()
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in information retrieval from images",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpg;base64,{base64_image}"},
                    },
                ],
            },
        ],
    )
    
    return response.choices[0].message.content


# Global client instance for reuse
_global_client: Optional[AzureOpenAI] = None


def get_authenticated_client() -> AzureOpenAI:
    """
    Get or create a global authenticated Azure OpenAI client.
    
    Returns:
        AzureOpenAI: Authenticated Azure OpenAI client
    """
    global _global_client
    if _global_client is None:
        _global_client = authenticate()
    return _global_client


def reset_client():
    """Reset the global client (useful for testing or credential refresh)."""
    global _global_client
    _global_client = None
