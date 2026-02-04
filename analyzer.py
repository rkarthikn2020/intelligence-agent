"""
Content analyzer using Claude API for summarization and topic extraction
"""
from anthropic import Anthropic
import config

def analyze_article(title, content, url):
    """
    Analyze an article to:
    1. Determine if it's relevant to user's topics
    2. Generate a 1-2 sentence summary
    3. Extract relevant topics
    """
    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        prompt = f"""Analyze this article and determine its relevance:

Article Title: {title}
Article URL: {url}
Content: {content[:3000]}

User's Topics of Interest:
- AI
- Digital Transformation  
- Koch Industries
- Guardian Industries

Tasks:
1. Is this article relevant to ANY of the user's topics? (Yes/No)
2. If yes, which topics does it relate to? (list them)
3. Generate a concise 1-2 sentence summary highlighting why this matters
4. Rate relevance from 1-10

Respond in this exact format:
RELEVANT: [Yes/No]
TOPICS: [comma-separated list or "None"]
SUMMARY: [your 1-2 sentence summary]
RELEVANCE_SCORE: [1-10]
"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse the response
        result = {
            'is_relevant': False,
            'topics': [],
            'summary': '',
            'score': 0
        }
        
        for line in response_text.split('\n'):
            if line.startswith('RELEVANT:'):
                result['is_relevant'] = 'yes' in line.lower()
            elif line.startswith('TOPICS:'):
                topics_text = line.replace('TOPICS:', '').strip()
                if topics_text and topics_text.lower() != 'none':
                    result['topics'] = [t.strip() for t in topics_text.split(',')]
            elif line.startswith('SUMMARY:'):
                result['summary'] = line.replace('SUMMARY:', '').strip()
            elif line.startswith('RELEVANCE_SCORE:'):
                try:
                    result['score'] = int(line.replace('RELEVANCE_SCORE:', '').strip())
                except:
                    result['score'] = 5
        
        return result
        
    except Exception as e:
        print(f"❌ Error analyzing article: {str(e)}")
        return {
            'is_relevant': True,  # Default to keeping it
            'topics': [],
            'summary': f"{title}",
            'score': 5
        }

def get_chatbot_response(user_question, articles_context):
    """
    Get chatbot response based on user's question and article context
    """
    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        # Prepare context from recent articles
        context = "Recent articles and summaries:\n\n"
        for article in articles_context[:20]:  # Use last 20 articles for context
            # Handle datetime fields safely
            scraped_date = article.get('scraped_date', 'Unknown date')
            if hasattr(scraped_date, 'strftime'):
                scraped_date = scraped_date.strftime('%Y-%m-%d')
            
            context += f"- {article['title']} ({article['source']}, {scraped_date})\n"
            context += f"  Summary: {article.get('summary', 'No summary')}\n"
            context += f"  URL: {article['url']}\n\n"
        
        prompt = f"""You are a helpful assistant that answers questions about recent articles on AI, Digital Transformation, Koch Industries, and Guardian Industries.

Context from recent articles:
{context}

User Question: {user_question}

Please provide a helpful, concise answer based on the articles above. If the question is not related to the articles, politely indicate that and offer to help with questions about the monitored topics. Include relevant article titles or sources when referencing information."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"❌ Error getting chatbot response: {str(e)}")
        return "I apologize, but I'm having trouble processing your question right now. Please try again."

if __name__ == "__main__":
    # Test analysis
    test_title = "Google DeepMind announces new AI breakthrough"
    test_content = "Google DeepMind has announced a major breakthrough in artificial intelligence..."
    result = analyze_article(test_title, test_content, "https://example.com")
    print(result)
