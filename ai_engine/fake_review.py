"""AI-powered fake review detection using Groq."""
import json
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)


def detect_fake_review(review):
    """Analyze a review for authenticity.
    
    Returns:
        dict: {is_fake: bool, confidence: 0-1, reasons: [str], analysis: str}
    """
    prompt = f"""Analyze this product review for authenticity. Check for signs of fake reviews:

Product: {review.product.name}
Rating: {review.rating}/5
Title: {review.title}
Review: {review.content}
Pros: {review.pros}
Cons: {review.cons}
Verified Purchase: {review.is_verified_purchase}

Common fake review indicators:
1. Generic/vague language without specific product details
2. Excessive superlatives or extreme negativity
3. Grammar patterns typical of generated reviews
4. Mismatched rating and content tone
5. No mention of actual product usage
6. Suspiciously short or copy-paste feel

Return JSON:
{{"is_fake": true/false, "confidence": 0.0-1.0, "reasons": ["reason1"], "analysis": "detailed analysis"}}"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a review authenticity detector. Analyze reviews for fake/spam indicators. Be balanced - legitimate reviews come in many forms. Respond with JSON only."},
        {"role": "user", "content": prompt}
    ])

    if result:
        return {
            'is_fake': result.get('is_fake', False),
            'confidence': result.get('confidence', 0.5),
            'reasons': result.get('reasons', []),
            'analysis': result.get('analysis', ''),
        }

    return {
        'is_fake': False,
        'confidence': 0.5,
        'reasons': ['Analysis unavailable'],
        'analysis': 'Unable to analyze review authenticity.',
    }


def batch_detect_fake_reviews(reviews):
    """Detect fake reviews in batch."""
    results = []
    for review in reviews:
        result = detect_fake_review(review)
        review.is_fake = result['is_fake']
        review.fake_confidence = result['confidence']
        review.save(update_fields=['is_fake', 'fake_confidence'])
        results.append({'review_id': str(review.id), **result})
    return results
