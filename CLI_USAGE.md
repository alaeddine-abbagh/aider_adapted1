# CLI Usage Guide - Company GPT-5 Model

This guide shows you how to run aider in the CLI with your company's GPT-5 model using OAuth2 authentication.

## Quick Start

### 1. Set up your environment variables

Create a `.env` file in your project directory:

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

### 2. Run aider with company authentication

**Option A: Using the launcher scripts (Recommended)**

**Windows:**
```cmd
# Make the batch file executable and run
aider-company.bat
```

**Linux/Mac:**
```bash
# Make the script executable and run
chmod +x aider-company.sh
./aider-company.sh
```

**Option B: Direct Python execution**
```bash
# Run the company CLI wrapper directly with different models
python -m aider.company_cli --model gpt5
python -m aider.company_cli --model gpt5mini
python -m aider.company_cli --model gpt5nano
```

**Option C: Manual environment setup**
```bash
# Set environment variables and run standard aider
# (Only if you've modified the main aider code to use CompanyModel)
python -m aider --model gpt5
```

## Command Line Options

All standard aider CLI options work with the company authentication:

### Basic Usage
```bash
# Start aider with your company's GPT-5 models
./aider-company.sh --model gpt5          # Standard GPT-5
./aider-company.sh --model gpt5mini      # GPT-5 Mini (faster, balanced)
./aider-company.sh --model gpt5nano      # GPT-5 Nano (fastest, lightweight)

# Specify files to work with
./aider-company.sh --model gpt5mini file1.py file2.py

# Enable verbose mode to see authentication details
./aider-company.sh --model gpt5 --verbose

# Use specific edit format
./aider-company.sh --model gpt5mini --edit-format diff
```

### Advanced Options
```bash
# Set custom temperature
./aider-company.sh --model gpt5mini --temperature 0.2

# Set reasoning effort for GPT-5 models (low, medium, high)
./aider-company.sh --model gpt5 --reasoning-effort low
./aider-company.sh --model gpt5 --reasoning-effort medium
./aider-company.sh --model gpt5 --reasoning-effort high

# Different models with optimal reasoning effort
./aider-company.sh --model gpt5nano --reasoning-effort low     # Fast responses
./aider-company.sh --model gpt5mini --reasoning-effort medium  # Balanced
./aider-company.sh --model gpt5 --reasoning-effort high        # Thorough

# Use reasoning effort with verbose mode to see details
./aider-company.sh --model gpt5 --reasoning-effort high --verbose

# Specify git repository
./aider-company.sh --git-dname /path/to/repo

# Use with specific configuration file
./aider-company.sh --config /path/to/config.yml

# Enable streaming (default for company models)
./aider-company.sh --stream

# Disable streaming if needed
./aider-company.sh --no-stream
```

## Environment Variable Options

You can also set environment variables directly instead of using a `.env` file:

**Windows:**
```cmd
set OIDC_ENDPOINT=your_endpoint
set OIDC_CLIENT_ID=your_client_id
set OIDC_CLIENT_SECRET=your_secret
set OIDC_SCOPE=your_scope
set APIGEE_ENDPOINT=your_apigee_endpoint
python -m aider.company_cli --model gpt5
```

**Linux/Mac:**
```bash
export OIDC_ENDPOINT=your_endpoint
export OIDC_CLIENT_ID=your_client_id
export OIDC_CLIENT_SECRET=your_secret
export OIDC_SCOPE=your_scope
export APIGEE_ENDPOINT=your_apigee_endpoint
python -m aider.company_cli --model gpt5
```

## Examples

### Example 1: Basic Code Assistance
```bash
# Start aider in your project directory
cd /path/to/your/project
./aider-company.sh main.py

# Start with specific reasoning effort for complex tasks
./aider-company.sh --model gpt5 --reasoning-effort high main.py

# In aider, you can now ask:
# "Add error handling to the main function"
# "Refactor this code to use async/await"
# "Add unit tests for the User class"
```

### Example 2: Working with Multiple Files
```bash
# Work with multiple files at once
./aider-company.sh src/*.py tests/*.py

# Or add files interactively in aider:
# /add new_file.py
# /drop old_file.py
```

### Example 3: Image Analysis (if your model supports it)
```bash
# Start aider and add an image
./aider-company.sh --model gpt5
# In aider: /add image.png
# Then ask: "What's in this image and how can I process it in Python?"
```

### Example 4: Configuration File Usage
Create `.aider.conf.yml`:
```yaml
model: gpt5
edit-format: diff
auto-commits: true
dirty-commits: true
```

Then run:
```bash
./aider-company.sh  # Will use settings from config file
```

## Troubleshooting

### Authentication Issues
```bash
# Run with verbose mode to see authentication details
./aider-company.sh --verbose

# Check if environment variables are set
./aider-company.sh --help  # Will show if company auth is detected
```

### Model Issues
```bash
# List available models (may not work with company auth)
./aider-company.sh --models

# Try with explicit model specification
./aider-company.sh --model gpt5 --verbose
```

### Network Issues
```bash
# If you have SSL certificate issues, you can disable verification
# (Not recommended for production)
export SSL_VERIFY=false
./aider-company.sh --no-verify-ssl
```

## Integration with IDEs

### VS Code
Add to your VS Code tasks.json:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Aider Company",
            "type": "shell",
            "command": "./aider-company.sh",
            "args": ["${file}"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        }
    ]
}
```

### PyCharm
Create an external tool:
- Program: `python`
- Arguments: `-m aider.company_cli --model gpt5 $FilePath$`
- Working directory: `$ProjectFileDir$`

## Performance Tips

1. **Use .env files**: Faster than setting environment variables each time
2. **Enable streaming**: Better user experience (enabled by default)
3. **Use specific files**: Don't add entire large codebases at once
4. **Configure git**: Aider works best with git repositories

## Security Notes

1. **Never commit .env files** - Add `.env` to your `.gitignore`
2. **Use proper SSL verification** in production environments
3. **Rotate credentials regularly** as per company policy
4. **Monitor API usage** through your company's monitoring tools

## GPT-5 Model Variants

Your company provides access to different GPT-5 model variants optimized for different use cases:

### Available Models

- **`gpt5`**: Standard GPT-5 - Full capabilities, balanced performance
- **`gpt5mini`**: GPT-5 Mini - Faster responses, good for most coding tasks
- **`gpt5nano`**: GPT-5 Nano - Fastest responses, optimized for simple tasks

### Model Selection Guide

- **Use `gpt5nano`** for: Quick fixes, simple refactoring, basic questions
- **Use `gpt5mini`** for: Most coding tasks, documentation, moderate complexity
- **Use `gpt5`** for: Complex algorithms, architecture decisions, thorough analysis

## Reasoning Effort Levels

The `--reasoning-effort` parameter controls how much computational effort GPT-5 puts into reasoning:

- **`low`**: Fast responses, minimal reasoning overhead (default for gpt5nano)
- **`medium`**: Balanced reasoning and speed (default for gpt5mini and gpt5)
- **`high`**: Maximum reasoning effort, slower but more thorough responses

### When to Use Different Reasoning Efforts

- **Low**: Simple tasks, quick iterations, debugging
- **Medium**: General coding tasks, refactoring, documentation
- **High**: Complex algorithms, architecture decisions, difficult debugging

### Examples by Reasoning Effort

```bash
# Quick fixes and simple tasks
./aider-company.sh --model gpt5 --reasoning-effort low

# Most coding tasks (default)
./aider-company.sh --model gpt5 --reasoning-effort medium

# Complex problem solving
./aider-company.sh --model gpt5 --reasoning-effort high --verbose
```

## Getting Help

- Run `./aider-company.sh --help` for all available options
- Check `COMPANY_INTEGRATION.md` for detailed setup instructions
- Run `python examples/company_usage_example.py` to test your setup
