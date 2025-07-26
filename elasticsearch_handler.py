from elasticsearch import Elasticsearch
import openai
from langdetect import detect

# Initialize Elasticsearch and OpenAI
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "your-password"),
    verify_certs=False
)
openai.api_key = "your-api-key"

def detect_language(message):
    """
    Detect the language of the message.
    """
    try:
        return detect(message)
    except Exception as e:
        print(f"Language detection error: {e}")
        return "unknown"

def get_language_index(language):
    """
    Get the Elasticsearch index name for a given language.
    """
    return f"scam-texts-{language}"

def search_elasticsearch(message):
    """
    Search for a message in Elasticsearch by language index.
    """
    language = detect_language(message)
    index_name = get_language_index(language)
    query = {"query": {"match": {"message": message}}}
    try:
        response = es.search(index=index_name, body=query)
        return response["hits"]["total"]["value"] > 0
    except Exception as e:
        print(f"Search error: {e}")
        return False

def analyze_with_llm(message):
    """
    Use OpenAI's LLM to check if a message is a scam.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that detects scam messages."},
                {"role": "user", "content": f"Is this message a scam? Message: {message}"}
            ]
        )
        return "scam" in response["choices"][0]["message"]["content"].lower()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return False

def store_in_elasticsearch(message):
    """
    Store a scam message in Elasticsearch, indexed by language.
    """
    language = detect_language(message)
    index_name = get_language_index(language)
    document = {"message": message, "type": "scam", "language": language}
    try:
        es.index(index=index_name, body=document)
        print(f"Message stored in index: {index_name}")
    except Exception as e:
        print(f"Indexing error: {e}")

def process_message(message):
    """
    Process a message through Elasticsearch and OpenAI analysis.
    """
    if search_elasticsearch(message):
        return "scam"
    if analyze_with_llm(message):
        store_in_elasticsearch(message)
        return "scam"
    return "safe"
