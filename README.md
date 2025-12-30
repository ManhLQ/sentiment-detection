# Multilingual CSV Sentiment Miner

AI-powered sentiment analysis and topic extraction for multilingual customer feedback using **DSPy**.

## Features

- 🌐 **Multilingual Support**: Handles English, Vietnamese, Japanese, and code-switching (mixed languages)
- 🎯 **Aspect-Sentiment Topics**: Extracts actionable tags like "Slow Shipping", "Good Quality"
- 🔄 **Dual LLM Backend**: Switch between OpenAI (GPT-4o-mini) and Ollama (local models)
- 📊 **Structured Output**: Clean CSV with Original Text, Sentiment, and Extracted Topics

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# LLM_BACKEND=openai
# OPENAI_API_KEY=sk-your-key-here

# Optional: Set a custom base URL for OpenAI-compatible servers (e.g. OpenRouter)
# OPENAI_API_BASE=https://api.openai.com/v1
```

### 3. Run Analysis

```bash
# Analyze sample data
python -m sentiment_miner.main --input data/sample_feedback.csv --column Comment

# Or use the installed CLI
sentiment-miner -i data/sample_feedback.csv -c Comment
```

## Using Ollama (Local LLM)

For privacy or offline use, run with Ollama:

```bash
# Start Ollama container
docker-compose up -d

# Pull a model (first time only)
docker exec sentiment-miner-ollama ollama pull llama3.2

# Update .env
# LLM_BACKEND=ollama
# OLLAMA_MODEL=llama3.2

# Run analysis
python -m sentiment_miner.main --input data/sample_feedback.csv --column Comment
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--input, -i` | Path to input CSV file (required) |
| `--column, -c` | Column name containing feedback text (required) |
| `--output, -o` | Output file path (default: `input_analyzed.csv`) |
| `--no-save` | Display results only, don't save to file |
| `--limit, -n` | Limit rows to process (for testing) |
| `--debug` | Show DSPy prompt history for each row |

## Output Format

| Original Text | Sentiment | Extracted Topics |
|---------------|-----------|------------------|
| "Giao hàng chậm" | Negative | Slow Shipping |
| "Sản phẩm ok but giá cao" | Neutral | Good Product, Expensive Price |

## Tech Stack

- **Orchestration**: [DSPy](https://dspy.ai/)
- **Language**: Python 3.9+
- **LLM Backend**: OpenAI (GPT-4o-mini), OpenRouter, or Ollama
- **Data Processing**: Pandas
