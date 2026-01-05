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
    
    # Ideas Generator Subparser
    ideas_parser = subparsers.add_parser(
        "ideas",
        help="Generate app ideas based on domain and constraints"
    )
    ideas_parser.add_argument(
        "--domain", "-d",
        required=True,
        help="Domain or seed idea (e.g., 'project management', 'fitness tracking')"
    )
    ideas_parser.add_argument(
        "--complexity", "-c",
        choices=["low", "medium", "high"],
        default="medium",
        help="Complexity level (default: medium)"
    )
    ideas_parser.add_argument(
        "--requirements", "-r",
        help="Additional requirements or constraints"
    )
    ideas_parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "terminal"],
        default="terminal",
        help="Output format (default: terminal)"
    )
    ideas_parser.add_argument(
        "--output", "-o",
        help="Output file path (optional, default: print to stdout)"
    )
    ideas_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show generation progress and validation details"
    )
    ideas_parser.add_argument(
        "--debug",
        action="store_true",
        help="Show DSPy prompt history for each generation step"
    )
    ideas_parser.add_argument(
        "--mode", "-m",
        choices=["lite", "full"],
        default="lite",
        help="Generation mode: 'lite' (fast, name/description/concepts) or 'full' (detailed with features/complexity) (default: lite)"
    )
    
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

def run_ideas(args) -> int:
    """Import and run the ideas generator."""
    try:
        from ideas import (
            AppIdeaGenerator,
            ComplexityLevel,
            IdeaRequest,
            LiteAppIdeaGenerator,
            format_as_colored_text,
            format_as_json,
            format_as_markdown,
            format_lite_as_colored_text,
            format_lite_as_json,
            format_lite_as_markdown,
            save_to_file,
        )
        
        # Create request from args
        request = IdeaRequest(
            domain=args.domain,
            complexity=ComplexityLevel(args.complexity),
            additional_requirements=args.requirements,
        )
        
        # Generate idea based on mode
        if args.mode == "lite":
            generator = LiteAppIdeaGenerator()
            idea = generator.generate_with_progress(
                request,
                verbose=args.verbose,
                debug=args.debug,
            )
            
            # Format output for lite mode
            if args.format == "json":
                output = format_lite_as_json(idea)
                file_ext = "json"
            elif args.format == "markdown":
                output = format_lite_as_markdown(idea)
                file_ext = "md"
            else:  # terminal
                output = format_lite_as_colored_text(idea)
                file_ext = "md"  # Still save as markdown
            
            # Save markdown version
            markdown_output = format_lite_as_markdown(idea)
        else:  # full mode
            generator = AppIdeaGenerator()
            idea, metadata = generator.generate_with_validation(
                request,
                verbose=args.verbose,
                debug=args.debug,
            )
            
            # Format output for full mode
            if args.format == "json":
                output = format_as_json(idea)
                file_ext = "json"
            elif args.format == "markdown":
                output = format_as_markdown(idea)
                file_ext = "md"
            else:  # terminal
                output = format_as_colored_text(idea)
                file_ext = "md"  # Still save as markdown
            
            # Save markdown version
            markdown_output = format_as_markdown(idea)
        
        # Always save to output folder with app name
        import os
        import re
        from pathlib import Path
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Sanitize app name for filename (remove special chars, replace spaces with underscores)
        safe_name = re.sub(r'[^\w\s-]', '', idea.name)
        safe_name = re.sub(r'[-\s]+', '_', safe_name).strip('_').lower()
        
        # Generate filename
        auto_filename = output_dir / f"{safe_name}.{file_ext}"
        
        # Save markdown version to output folder
        markdown_filename = output_dir / f"{safe_name}.md"
        save_to_file(markdown_output, str(markdown_filename))
        
        # Also save to user-specified output if provided
        if args.output:
            save_to_file(output, args.output)
            print(f"\n✅ Idea saved to: {args.output}")
            print(f"📁 Also saved to: {markdown_filename}")
        else:
            # Just print to terminal
            print(output)
            print(f"\n📁 Idea saved to: {markdown_filename}")
        
        # Show metadata if verbose (only for full mode)
        if args.verbose and args.mode == "full":
            print(f"\n📊 Generation metadata:")
            print(f"  Attempts: {metadata['attempts']}")
            print(f"  Validation passed: {metadata['validation_passed']}")
            if metadata['issues']:
                print(f"  Issues: {metadata['issues']}")
        
        return 0
    except Exception as e:
        print(f"Error generating idea: {e}")
        import traceback
        traceback.print_exc()
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
        elif args.command == "ideas":
            return run_ideas(args)
    except Exception as e:
        print(f"Configuration/Initialization Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
