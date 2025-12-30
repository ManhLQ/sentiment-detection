"""Main processing pipeline for sentiment analysis."""

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple

import dspy
from tqdm import tqdm

from .signatures import FeedbackAnalyzer


@dataclass
class AnalysisResult:
    """Result of analyzing a single piece of feedback."""
    
    original_text: str
    sentiment: str
    topics: List[str]


def analyze_feedback_batch(
    texts: List[str],
    show_progress: bool = True,
    debug: bool = False
) -> List[AnalysisResult]:
    """
    Analyze a batch of customer feedback texts.
    
    Args:
        texts: List of feedback texts to analyze
        show_progress: Whether to show a progress bar (default: True)
        debug: Whether to show DSPy prompt history (default: False)
        
    Returns:
        List of AnalysisResult objects
    """
    analyzer = FeedbackAnalyzer()
    results = []
    
    iterator = tqdm(
        enumerate(texts),
        total=len(texts),
        desc="Processing feedback",
        disable=not show_progress
    )
    
    for idx, text in iterator:
        if show_progress:
            iterator.set_postfix_str(f"Row {idx + 1}/{len(texts)}")
        
        try:
            prediction = analyzer(text=text)
            
            if debug:
                dspy.inspect_history(n=1)
                
            result = AnalysisResult(
                original_text=text,
                sentiment=prediction.sentiment,
                topics=prediction.topics if isinstance(prediction.topics, list) else [prediction.topics]
            )
        except Exception as e:
            # Handle LLM errors gracefully
            result = AnalysisResult(
                original_text=text,
                sentiment="Error",
                topics=[f"Analysis failed: {str(e)[:50]}"]
            )
        
        results.append(result)
    
    return results


def aggregate_topics(results: List[AnalysisResult]) -> List[Tuple[str, int, str]]:
    """
    Aggregate topics across all results with frequency counts.
    
    Creates a "word cloud in table format" showing each unique topic,
    how many times it appears, and sentiment distribution.
    
    Args:
        results: List of AnalysisResult objects
        
    Returns:
        List of tuples (topic, count, dominant_sentiment) sorted by count descending
    """
    topic_counts: Counter = Counter()
    topic_sentiments: Dict[str, Counter] = {}
    
    for result in results:
        if result.sentiment == "Error":
            continue
            
        for topic in result.topics:
            topic_normalized = topic.strip()
            if not topic_normalized:
                continue
                
            topic_counts[topic_normalized] += 1
            
            if topic_normalized not in topic_sentiments:
                topic_sentiments[topic_normalized] = Counter()
            topic_sentiments[topic_normalized][result.sentiment] += 1
    
    # Build result with dominant sentiment for each topic
    aggregated = []
    for topic, count in topic_counts.most_common():
        dominant_sentiment = topic_sentiments[topic].most_common(1)[0][0]
        aggregated.append((topic, count, dominant_sentiment))
    
    return aggregated

