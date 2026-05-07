"""AI-powered sentiment analysis for product reviews."""
import json
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)


def analyze_sentiment(review_text, review_title=""):
    """Analyze the sentiment of a review.
    
    Returns:
        dict: {score: -1 to 1, label: positive/negative/neutral, summary: str}
    """
    prompt = f"""Analyze the sentiment of this product review.

Title: {review_title}
Review: {review_text}

Return JSON:
{{"score": -1.0 to 1.0, "label": "positive/negative/neutral", "summary": "brief sentiment summary", "key_points": ["point1", "point2"]}}

Score guidelines:
- -1.0 to -0.3: Negative
- -0.3 to 0.3: Neutral
- 0.3 to 1.0: Positive"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a sentiment analysis AI. Respond with JSON only."},
        {"role": "user", "content": prompt}
    ])

    if result:
        return {
            'score': result.get('score', 0),
            'label': result.get('label', 'neutral'),
            'summary': result.get('summary', ''),
            'key_points': result.get('key_points', []),
        }

    return {'score': 0, 'label': 'neutral', 'summary': 'Analysis unavailable', 'key_points': []}


def batch_analyze_sentiments(reviews):
    """Analyze sentiment for multiple reviews."""
    results = []
    for review in reviews:
        result = analyze_sentiment(review.content, review.title)
        review.sentiment_score = result['score']
        review.sentiment_label = result['label']
        review.save(update_fields=['sentiment_score', 'sentiment_label'])
        results.append({'review_id': str(review.id), **result})
    return results
