"""CLI entry point for the Sentiment Miner."""

import argparse
import sys


from .config import configure_dspy, get_llm_backend
from .io_handlers import generate_output_path, read_csv_column, save_results_csv
from .pipeline import aggregate_topics, analyze_feedback_batch


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sentiment-miner",
        description="Analyze sentiment and extract topics from multilingual CSV feedback data."
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input CSV file"
    )
    
    parser.add_argument(
        "--column", "-c",
        required=True,
        help="Name of the column containing feedback text"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path for output CSV file (default: input_analyzed.csv)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Display results in console only, don't save to file"
    )
    
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Limit number of rows to process (for testing)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show DSPy prompt history for each processed row"
    )
    
    return parser


def display_results_table(results) -> None:
    """Display results in a simple format."""
    print("\n--- Sentiment Analysis Results ---")
    for result in results:
        text = result.original_text
        if len(text) > 47:
            text = text[:47] + "..."
        print(f"[{result.sentiment}] {text} | Topics: {', '.join(result.topics)}")


def display_topic_cloud_table(results) -> None:
    """Display aggregated topics in a simple format."""
    aggregated = aggregate_topics(results)
    
    if not aggregated:
        print("\nNo topics extracted")
        return
    
    print("\n--- Topic Frequency ---")
    print(f"{'Topic':<25} | {'Count':<7} | {'Sentiment'}")
    print("-" * 50)
    for topic, count, sentiment in aggregated:
        print(f"{topic[:25]:<25} | {count:<7} | {sentiment}")


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Configure DSPy
        print(f"Using LLM backend: {get_llm_backend()}")
        configure_dspy()
        print("DSPy configured successfully\n")
        
        # Read input
        print(f"Reading: {args.input}")
        texts = read_csv_column(args.input, args.column)
        
        if args.limit:
            texts = texts[:args.limit]
            print(f"Limited to {args.limit} rows")
        
        print(f"Loaded {len(texts)} rows from column '{args.column}'\n")
        
        # Process
        results = analyze_feedback_batch(
            texts, 
            show_progress=not args.debug,  # Hide progress bar if debugging to avoid mess
            debug=args.debug
        )
        print()  # New line after progress bar or debug output
        
        # Display detailed results table
        display_results_table(results)
        
        # Display word cloud table (topic frequency)
        print()
        display_topic_cloud_table(results)
        
        # Save if requested
        if not args.no_save:
            output_path = args.output or generate_output_path(args.input)
            save_results_csv(results, output_path)
            print(f"\nResults saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except KeyError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130


if __name__ == "__main__":
    sys.exit(main())
