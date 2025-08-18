from fastapi import APIRouter
import jieba
import jieba.posseg as pseg
import re
from sklearn.feature_extraction.text import TfidfVectorizer


from app.models.api import ApiResponse
from app.models.legacy import (
    InformationExtractionRequest,
    IntentClassificationRequest,
    StructuredConversionRequest,
    TextProcessingRequest,
)

router = APIRouter()


@router.post(
    "/text-processing",
    response_model=ApiResponse,
    summary="Process Raw Text",
    tags=["Legacy Processing"],
)
async def text_processing(request: TextProcessingRequest):
    """
    Submits raw text for preprocessing steps like tokenization and TF-IDF vectorization.
    """
    # Tokenize the text using jieba
    tokens = list(jieba.cut(request.text, cut_all=False))

    # Join tokens back to string for vectorizer if the text is not empty
    if tokens:
        processed_text = " ".join(tokens)
        
        # Create TF-IDF vectorizer and transform the text
        vectorizer = TfidfVectorizer()
        tfidf_vector = vectorizer.fit_transform([processed_text])
        
        # Get feature names (words) and their tf-idf scores
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_vector.toarray()[0]
        
        # Create a dictionary of word -> tf-idf score
        tfidf_results = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}
    else:
        tfidf_results = {}

    processed_data = {
        "original_text": request.text,
        "tokens": tokens,
        "tfidf_vector": tfidf_results,
    }
    return ApiResponse(
        status="success", data=processed_data, message="Text processed successfully."
    )


@router.post(
    "/information-extraction",
    response_model=ApiResponse,
    summary="Extract Information",
    tags=["Legacy Processing"],
)
async def information_extraction(request: InformationExtractionRequest):
    """Extracts entities (nouns) and events (verbs) from preprocessed text."""
    words = pseg.cut(request.text)
    entities = []
    events = []
    for word, flag in words:
        if flag.startswith('n'): # Nouns
            entities.append(word)
        elif flag.startswith('v'): # Verbs
            events.append(word)
            
    extracted_data = {"entities": entities, "events": events}
    return ApiResponse(
        status="success",
        data=extracted_data,
        message="Information extracted successfully.",
    )


@router.post(
    "/intent-classification",
    response_model=ApiResponse,
    summary="Classify Intent",
    tags=["Legacy Processing"],
)
async def intent_classification(request: IntentClassificationRequest):
    """Classifies the intent from a conversational snippet based on keywords."""
    intents = {
        "greeting": ["你好", "您好", "嗨", "哈囉"],
        "goodbye": ["再見", "掰掰"],
        "weather_inquiry": ["天氣", "氣溫", "下雨", "晴天"],
    }
    
    classified_intent = "Unknown"
    confidence = 0.0
    
    for intent, keywords in intents.items():
        if any(keyword in request.text for keyword in keywords):
            classified_intent = intent
            confidence = 1.0
            break
            
    classified_data = {"intent": classified_intent, "confidence": confidence}
    return ApiResponse(
        status="success",
        data=classified_data,
        message="Intent classified successfully.",
    )


@router.post(
    "/structured-conversion",
    response_model=ApiResponse,
    summary="Convert to Structured Data",
    tags=["Legacy Processing"],
)
async def structured_conversion(request: StructuredConversionRequest):
    """Converts unstructured text into a structured format based on a schema."""
    # Simple key-value extraction using regex
    # Looks for patterns like "key: value" or "key is value"
    patterns = [
        r"(.*?):\s*(.*)",
        r"(.*?)\s+是\s+(.*)",
    ]
    
    data = {}
    for line in request.text.split('\n'):
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                data[key] = value
                break

    structured_data = {"schema_id": request.schema_id, "data": data}
    return ApiResponse(
        status="success",
        data=structured_data,
        message="Text converted to structured format successfully.",
    )
