"""DSPy Signatures for sentiment classification and topic extraction."""

from typing import List, Literal

import dspy


class SentimentClassifier(dspy.Signature):
    """
    Classify the sentiment of a customer feedback text.
    
    The text may be in any language (English, Vietnamese, Japanese, etc.)
    or contain code-switching (mixed languages in the same sentence).
    
    Output the overall sentiment as Positive, Negative, or Neutral.
    """
    
    text: str = dspy.InputField(
        desc="Customer feedback text in any language"
    )
    sentiment: Literal["Positive", "Negative", "Neutral"] = dspy.OutputField(
        desc="Overall sentiment classification"
    )


class TopicExtractor(dspy.Signature):
    """
    Extract key topics from customer feedback and translate them to English.
    
    Rules:
    1. Extract 1-3 topics from the text
    2. Each topic MUST follow the format: "Aspect + Sentiment" (e.g., "Slow Shipping", "Good Quality")
    3. ALL topics must be in Standard English, regardless of input language
    4. Topics should be concise (2-4 words maximum)
    
    Examples:
    - Input: "Giao hàng chậm" → ["Slow Shipping"]
    - Input: "Sản phẩm ok but giá hơi cao" → ["Good Product", "Expensive Price"]
    - Input: "配送が速い、品質も良い" → ["Fast Shipping", "Good Quality"]
    """
    
    text: str = dspy.InputField(
        desc="Customer feedback text in any language"
    )
    topics: List[str] = dspy.OutputField(
        desc="List of 1-3 topics in 'Aspect + Sentiment' format, in English"
    )


class FeedbackAnalyzer(dspy.Module):
    """
    Combined module for analyzing customer feedback.
    
    Performs both sentiment classification and topic extraction in a single call.
    """
    
    def __init__(self):
        super().__init__()
        self.classify_sentiment = dspy.ChainOfThought(SentimentClassifier)
        self.extract_topics = dspy.ChainOfThought(TopicExtractor)
    
    def forward(self, text: str) -> dspy.Prediction:
        """
        Analyze a single piece of customer feedback.
        
        Args:
            text: Customer feedback text in any language
            
        Returns:
            dspy.Prediction with 'sentiment' and 'topics' fields
        """
        sentiment_result = self.classify_sentiment(text=text)
        topics_result = self.extract_topics(text=text)
        
        return dspy.Prediction(
            sentiment=sentiment_result.sentiment,
            topics=topics_result.topics
        )
