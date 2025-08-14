#!/bin/bash
# Company Aider CLI Launcher
# This script runs aider with company OAuth2 authentication for GPT-5

echo "🚀 Starting Aider with Company Authentication..."

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Found .env file - loading company credentials..."
else
    echo "⚠️  Warning: No .env file found. Please create one with your company credentials."
    echo "   See COMPANY_INTEGRATION.md for setup instructions."
fi

# Run aider with company authentication
python -m aider.company_cli --model gpt5 "$@"

# Examples with different models:
# python -m aider.company_cli --model gpt5nano "$@"
# python -m aider.company_cli --model gpt5mini "$@"
# python -m aider.company_cli --model gpt5 "$@"

# Examples with reasoning effort:
# python -m aider.company_cli --model gpt5 --reasoning-effort low "$@"
# python -m aider.company_cli --model gpt5 --reasoning-effort medium "$@"
# python -m aider.company_cli --model gpt5 --reasoning-effort high "$@"
# python -m aider.company_cli --model gpt5nano --reasoning-effort low "$@"
# python -m aider.company_cli --model gpt5mini --reasoning-effort medium "$@"

# Alternative: If you want to run the original aider with environment variables set
# python -m aider --model gpt5 "$@"
