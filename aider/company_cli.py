#!/usr/bin/env python3
"""
Company CLI wrapper for aider that enables OAuth2 authentication.

This script provides a simple way to run aider with company authentication
by monkey-patching the Model class before aider initializes.
"""

import os
import sys
from pathlib import Path

# Add the aider directory to the path so we can import modules
aider_dir = Path(__file__).parent
sys.path.insert(0, str(aider_dir))

def setup_company_auth():
    """Set up company authentication by monkey-patching the Model class."""
    try:
        from aider.company_models import CompanyModel
        from aider import models
        
        # Check if company authentication is configured
        required_vars = [
            "OIDC_ENDPOINT", "OIDC_CLIENT_ID", "OIDC_CLIENT_SECRET", 
            "OIDC_SCOPE", "APIGEE_ENDPOINT"
        ]
        
        if all(os.environ.get(var) for var in required_vars):
            # Create a wrapper class that passes reasoning_effort from args
            class CompanyModelWrapper(CompanyModel):
                def __init__(self, model, weak_model=None, editor_model=None, editor_edit_format=None, verbose=False):
                    # Get reasoning effort from command line args if available
                    reasoning_effort = None
                    if hasattr(sys, 'argv'):
                        for i, arg in enumerate(sys.argv):
                            if arg == '--reasoning-effort' and i + 1 < len(sys.argv):
                                reasoning_effort = sys.argv[i + 1]
                                break
                    
                    super().__init__(model, weak_model, editor_model, editor_edit_format, verbose, reasoning_effort)
            
            # Replace the Model class with CompanyModelWrapper
            models.Model = CompanyModelWrapper
            print("✅ Company OAuth2 authentication enabled")
            return True
        else:
            missing = [var for var in required_vars if not os.environ.get(var)]
            print(f"⚠️  Company auth not configured. Missing: {', '.join(missing)}")
            print("   Falling back to standard authentication.")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing company modules: {e}")
        return False

def main():
    """Main entry point that sets up company auth and runs aider."""
    print("🚀 Starting aider with company authentication support...")
    
    # Set up company authentication
    setup_company_auth()
    
    # Import and run the main aider function
    from aider.main import main as aider_main
    
    # Run aider with the original arguments
    sys.exit(aider_main())

if __name__ == "__main__":
    main()
