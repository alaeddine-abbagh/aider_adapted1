@echo off
REM Company Aider CLI Launcher
REM This script runs aider with company OAuth2 authentication for GPT-5

echo Starting Aider with Company Authentication...

REM Check if .env file exists
if exist .env (
    echo Found .env file - loading company credentials...
) else (
    echo Warning: No .env file found. Please create one with your company credentials.
    echo See COMPANY_INTEGRATION.md for setup instructions.
)

REM Run aider with company authentication
python -m aider.company_cli --model gpt5 %*

REM Examples with different models:
REM python -m aider.company_cli --model gpt5nano %*
REM python -m aider.company_cli --model gpt5mini %*
REM python -m aider.company_cli --model gpt5 %*

REM Examples with reasoning effort:
REM python -m aider.company_cli --model gpt5 --reasoning-effort low %*
REM python -m aider.company_cli --model gpt5 --reasoning-effort medium %*
REM python -m aider.company_cli --model gpt5 --reasoning-effort high %*
REM python -m aider.company_cli --model gpt5nano --reasoning-effort low %*
REM python -m aider.company_cli --model gpt5mini --reasoning-effort medium %*

REM Alternative: If you want to run the original aider with environment variables set
REM python -m aider --model gpt5 %*
