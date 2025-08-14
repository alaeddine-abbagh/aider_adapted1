"""
Company-specific model wrapper that integrates with the existing aider Model class.
This module provides a drop-in replacement for the standard Model class that uses
company OAuth2 authentication.
"""

import os
import json
import hashlib
from typing import Optional, Dict, Any

from aider.models import Model as BaseModel
from aider.company_auth import get_authenticated_client, reset_client
from aider.sendchat import ensure_alternating_roles, sanity_check_messages
from aider import __version__


class CompanyModel(BaseModel):
    """
    Company-specific model that uses OAuth2 authentication for Azure OpenAI.
    
    This class extends the base Model class to use company authentication
    instead of standard API key authentication.
    """
    
    def __init__(self, model, weak_model=None, editor_model=None, editor_edit_format=None, verbose=False, reasoning_effort=None):
        """
        Initialize the company model with OAuth2 authentication.
        
        Args:
            model: Model name/deployment
            weak_model: Optional weak model name
            editor_model: Optional editor model name
            editor_edit_format: Optional editor edit format
            verbose: Enable verbose logging
            reasoning_effort: Optional reasoning effort level (low, medium, high)
        """
        # Initialize the base model
        super().__init__(model, weak_model, editor_model, editor_edit_format, verbose)
        
        # Store reasoning effort setting
        self.reasoning_effort = reasoning_effort
        
        # Check if company authentication is configured
        self.use_company_auth = self._is_company_auth_configured()
        
        if self.use_company_auth and self.verbose:
            print("Using company OAuth2 authentication for Azure OpenAI")
            if self.reasoning_effort:
                print(f"Reasoning effort set to: {self.reasoning_effort}")
    
    def _is_company_auth_configured(self) -> bool:
        """
        Check if company authentication environment variables are configured.
        
        Returns:
            bool: True if company auth is configured, False otherwise
        """
        required_vars = [
            "OIDC_ENDPOINT",
            "OIDC_CLIENT_ID", 
            "OIDC_CLIENT_SECRET",
            "OIDC_SCOPE",
            "APIGEE_ENDPOINT"
        ]
        return all(os.environ.get(var) for var in required_vars)
    
    def _is_gpt5_model(self) -> bool:
        """
        Check if this is a GPT-5 model variant.
        
        Returns:
            bool: True if this is a GPT-5 model (including mini, nano variants)
        """
        model_name = self.name.lower()
        return ("gpt5" in model_name or 
                "gpt-5" in model_name or 
                model_name in ["gpt5mini", "gpt5nano"])
    
    def send_completion(self, messages, functions, stream, temperature=None):
        """
        Send completion request using company authentication if configured,
        otherwise fall back to standard authentication.
        
        Args:
            messages: List of messages for the conversation
            functions: Optional function definitions
            stream: Whether to stream the response
            temperature: Optional temperature setting
            
        Returns:
            Tuple of (hash_object, response)
        """
        if not self.use_company_auth:
            # Fall back to standard authentication
            return super().send_completion(messages, functions, stream, temperature)
        
        # Use company authentication
        return self._send_completion_with_company_auth(messages, functions, stream, temperature)
    
    def _send_completion_with_company_auth(self, messages, functions, stream, temperature=None):
        """
        Send completion using company OAuth2 authentication.
        
        Args:
            messages: List of messages for the conversation
            functions: Optional function definitions
            stream: Whether to stream the response
            temperature: Optional temperature setting
            
        Returns:
            Tuple of (hash_object, response)
        """
        if os.environ.get("AIDER_SANITY_CHECK_TURNS"):
            sanity_check_messages(messages)

        if self.is_deepseek_r1():
            messages = ensure_alternating_roles(messages)

        # Get authenticated client
        client = get_authenticated_client()
        
        # Prepare kwargs for the API call
        kwargs = dict(
            model=self.name,
            stream=stream,
            messages=messages,
        )

        # Handle temperature
        if self.use_temperature is not False:
            if temperature is None:
                if isinstance(self.use_temperature, bool):
                    temperature = 0
                else:
                    temperature = float(self.use_temperature)
            kwargs["temperature"] = temperature

        # Handle functions/tools
        if functions is not None:
            function = functions[0]
            kwargs["tools"] = [dict(type="function", function=function)]
            kwargs["tool_choice"] = {"type": "function", "function": {"name": function["name"]}}

        # Add extra parameters
        if self.extra_params:
            kwargs.update(self.extra_params)

        # Handle reasoning effort for supported models
        if self.reasoning_effort:
            kwargs["reasoning_effort"] = self.reasoning_effort
        elif self._is_gpt5_model():
            # Default reasoning effort for GPT-5 models based on variant
            if "nano" in self.name.lower():
                kwargs["reasoning_effort"] = "low"  # Nano optimized for speed
            elif "mini" in self.name.lower():
                kwargs["reasoning_effort"] = "medium"  # Mini balanced
            else:
                kwargs["reasoning_effort"] = "medium"  # Standard GPT-5

        # Handle max completion tokens for reasoning models
        if "reasoning_effort" in kwargs and "max_completion_tokens" not in kwargs:
            kwargs["max_completion_tokens"] = 800

        # Create hash for caching
        key = json.dumps({k: v for k, v in kwargs.items() if k != "messages"}, sort_keys=True).encode()
        hash_object = hashlib.sha1(key)

        if self.verbose:
            print(f"Company auth API call kwargs: {kwargs}")

        try:
            # Make the API call using the authenticated client
            response = client.chat.completions.create(**kwargs)
            return hash_object, response
            
        except Exception as e:
            if self.verbose:
                print(f"Company auth API call failed: {e}")
            # Reset client and try once more
            reset_client()
            client = get_authenticated_client()
            response = client.chat.completions.create(**kwargs)
            return hash_object, response
    
    def simple_send_with_retries(self, messages):
        """
        Simple send with retries using company authentication.
        
        Args:
            messages: List of messages for the conversation
            
        Returns:
            Response content
        """
        if not self.use_company_auth:
            return super().simple_send_with_retries(messages)
        
        # Use company authentication
        hash_object, response = self._send_completion_with_company_auth(
            messages, functions=None, stream=False, temperature=0
        )
        
        if hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content
        return ""


def create_company_model(model_name: str, **kwargs) -> CompanyModel:
    """
    Factory function to create a company model instance.
    
    Args:
        model_name: Name of the model/deployment
        **kwargs: Additional arguments for model initialization
        
    Returns:
        CompanyModel: Configured company model instance
    """
    return CompanyModel(model_name, **kwargs)


# Convenience functions matching the company code style
def simple_api_call_high_reasoning(prompt: str, model: str, max_tokens: int = 800) -> str:
    """
    Simple API call with high reasoning effort using company authentication.
    
    Args:
        prompt: The user prompt
        model: The model deployment name
        max_tokens: Maximum completion tokens
        
    Returns:
        str: The model's response content
    """
    from aider.company_auth import simple_api_call_high_reasoning as company_call
    return company_call(prompt, model, max_tokens)


def process_image_with_text(image_path: str, prompt: str, model: str) -> str:
    """
    Process an image with text prompt using company authentication.
    
    Args:
        image_path: Path to the image file
        prompt: Text prompt for image analysis
        model: The model deployment name
        
    Returns:
        str: The model's response content
    """
    from aider.company_auth import process_image_with_text as company_process
    return company_process(image_path, prompt, model)
