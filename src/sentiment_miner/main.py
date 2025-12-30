"""CLI entry point for the Sentiment Miner."""

import argparse
import sys

from rich.console import Console
from rich.table import Table

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


def display_results_table(results, console: Console) -> None:
    """Display results as a rich table in the console."""
    table = Table(
        title="Sentiment Analysis Results",
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Original Text", style="dim", max_width=50)
    table.add_column("Sentiment", justify="center")
    table.add_column("Extracted Topics", style="cyan")
    
    # Color mapping for sentiment
    sentiment_colors = {
        "Positive": "[green]Positive[/green]",
        "Negative": "[red]Negative[/red]",
        "Neutral": "[yellow]Neutral[/yellow]",
        "Error": "[bold red]Error[/bold red]"
    }
    
    for result in results:
        # Truncate long text
        text = result.original_text
        if len(text) > 47:
            text = text[:47] + "..."
        
        sentiment_display = sentiment_colors.get(
            result.sentiment, 
            result.sentiment
        )
        topics_display = ", ".join(result.topics)
        
        table.add_row(text, sentiment_display, topics_display)
    
    console.print(table)


def display_topic_cloud_table(results, console: Console) -> None:
    """Display aggregated topics as a word cloud in table format."""
    aggregated = aggregate_topics(results)
    
    if not aggregated:
        console.print("[yellow]No topics extracted[/yellow]")
        return
    
    table = Table(
        title="📊 Topic Cloud (Word Frequency Table)",
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Topic", style="bold")
    table.add_column("Appearances", justify="center")
    table.add_column("Dominant Sentiment", justify="center")
    table.add_column("Visual", justify="left")
    
    # Find max count for visual bar scaling
    max_count = max(count for _, count, _ in aggregated) if aggregated else 1
    
    # Color mapping for sentiment
    sentiment_styles = {
        "Positive": "green",
        "Negative": "red",
        "Neutral": "yellow"
    }
    
    for topic, count, sentiment in aggregated:
        style = sentiment_styles.get(sentiment, "white")
        sentiment_display = f"[{style}]{sentiment}[/{style}]"
        
        # Visual bar (like word cloud size)
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        bar_display = f"[{style}]{bar}[/{style}]"
        
        table.add_row(topic, str(count), sentiment_display, bar_display)
    
    console.print(table)


def main() -> int:
    """Main entry point."""
    console = Console()
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Configure DSPy
        console.print(f"[bold blue]Using LLM backend:[/bold blue] {get_llm_backend()}")
        configure_dspy()
        console.print("[green]✓[/green] DSPy configured successfully\n")
        
        # Read input
        console.print(f"[bold blue]Reading:[/bold blue] {args.input}")
        texts = read_csv_column(args.input, args.column)
        
        if args.limit:
            texts = texts[:args.limit]
            console.print(f"[yellow]Limited to {args.limit} rows[/yellow]")
        
        console.print(f"[green]✓[/green] Loaded {len(texts)} rows from column '{args.column}'\n")
        
        # Process
        results = analyze_feedback_batch(
            texts, 
            show_progress=not args.debug,  # Hide progress bar if debugging to avoid mess
            debug=args.debug
        )
        console.print()  # New line after progress bar or debug output
        
        # Display detailed results table
        display_results_table(results, console)
        
        # Display word cloud table (topic frequency)
        console.print()
        display_topic_cloud_table(results, console)
        
        # Save if requested
        if not args.no_save:
            output_path = args.output or generate_output_path(args.input)
            save_results_csv(results, output_path)
            console.print(f"\n[green]✓[/green] Results saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1
    except KeyError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
