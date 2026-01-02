"""Unified CLI entry point for the DSPy Agent project."""

import argparse
import sys
from typing import Optional

# These imports will be local to the functions to avoid unnecessary loading
# if a specific command is not used.

def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="dspy-agent",
        description="DSPy Agent Toolkit - Multilingual Sentiment Analysis and Interactive QA."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Sentiment Miner Subparser
    miner_parser = subparsers.add_parser(
        "sentiment", 
        help="Run multilingual sentiment analysis on CSV data"
    )
    miner_parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input CSV file"
    )
    miner_parser.add_argument(
        "--column", "-c",
        required=True,
        help="Name of the column containing feedback text"
    )
    miner_parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path for output CSV file (default: input_analyzed.csv)"
    )
    miner_parser.add_argument(
        "--no-save",
        action="store_true",
        help="Display results in console only, don't save to file"
    )
    miner_parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Limit number of rows to process (for testing)"
    )
    miner_parser.add_argument(
        "--debug",
        action="store_true",
        help="Show DSPy prompt history for each processed row"
    )
    
    # Conversation/QA Subparser
    qa_parser = subparsers.add_parser(
        "chat", 
        help="Start an interactive QA session"
    )
    # No specific args for chat for now, but we can add model override later
    
    return parser

def run_sentiment_miner(args) -> int:
    """Import and run the sentiment miner pipeline."""
    from sentiment_miner.main import run_analysis_pipeline
    return run_analysis_pipeline(args)


def run_chat() -> int:
    """Import and run the conversation QA."""
    try:
        from conversation.qa import run_interactive_chat
        
        print("Starting chat...\n")
        run_interactive_chat()
        return 0
    except Exception as e:
        print(f"Error in chat: {e}")
        return 1

def main() -> int:
    """Main entry point for unified CLI."""
    parser = create_main_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0

    try:
        # Global configuration
        from sentiment_miner.config import configure_dspy, get_llm_backend
        print(f"Using LLM backend: {get_llm_backend()}")
        configure_dspy()
        print("DSPy configured successfully\n")
        
        if args.command == "sentiment":
            return run_sentiment_miner(args)
        elif args.command == "chat":
            return run_chat()
    except Exception as e:
        print(f"Configuration/Initialization Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
