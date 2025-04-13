#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Search Foundation API Demo

This application demonstrates how to use Jina AI Search Foundation APIs for various search and AI-related tasks.

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import json
import base64
import requests
from typing import List, Dict, Any, Union, Optional
from dotenv import load_dotenv
from PIL import Image
import io
import time

# Load environment variables from .env file (if it exists)
load_dotenv()

# Get API key from environment variable
API_KEY = os.environ.get("JINA_API_KEY")
if not API_KEY:
    raise ValueError("JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey")

# Common headers for all API requests
BASE_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds


def handle_request_with_retry(method, url, headers, json_data=None, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    """
    Handle API requests with retry logic for network failures.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: API endpoint URL
        headers: HTTP headers
        json_data: JSON data for the request body
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        Response object
    """
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Request failed after {max_retries} attempts: {e}")
                raise


def get_embeddings(texts: List[str], model: str = "jina-embeddings-v3", normalized: bool = True) -> Dict[str, Any]:
    """
    Generate embeddings for a list of text inputs using Jina AI Embeddings API.
    
    Args:
        texts: List of text inputs to generate embeddings for
        model: Model to use for generating embeddings (default: jina-embeddings-v3)
        normalized: Whether to normalize the embeddings to unit L2 norm
        
    Returns:
        Dictionary containing the embeddings and usage information
    """
    url = "https://api.jina.ai/v1/embeddings"
    
    payload = {
        "model": model,
        "input": texts,
        "normalized": normalized
    }
    
    try:
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return {"error": str(e)}


def rerank_documents(query: str, documents: List[str], model: str = "jina-reranker-v2-base-multilingual", top_n: Optional[int] = None) -> Dict[str, Any]:
    """
    Rerank a list of documents based on relevance to a query using Jina AI Reranker API.
    
    Args:
        query: Search query
        documents: List of documents to rerank
        model: Model to use for reranking (default: jina-reranker-v2-base-multilingual)
        top_n: Number of top results to return (default: all)
        
    Returns:
        Dictionary containing the reranked documents and usage information
    """
    url = "https://api.jina.ai/v1/rerank"
    
    payload = {
        "model": model,
        "query": query,
        "documents": documents
    }
    
    if top_n is not None:
        payload["top_n"] = top_n
    
    try:
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error reranking documents: {e}")
        return {"error": str(e)}


def read_webpage(url: str, with_links: bool = False, with_images: bool = False, no_cache: bool = False) -> Dict[str, Any]:
    """
    Read and parse content from a URL using Jina AI Reader API.
    
    Args:
        url: URL to read and parse
        with_links: Whether to include links in the response
        with_images: Whether to include images in the response
        no_cache: Whether to bypass cache for fresh retrieval
        
    Returns:
        Dictionary containing the parsed content and metadata
    """
    reader_url = "https://r.jina.ai/"
    
    headers = BASE_HEADERS.copy()
    
    if with_links:
        headers["X-With-Links-Summary"] = "true"
    if with_images:
        headers["X-With-Images-Summary"] = "true"
    if no_cache:
        headers["X-No-Cache"] = "true"
    
    payload = {"url": url}
    
    try:
        response = handle_request_with_retry("POST", reader_url, headers, payload)
        return response.json()
    except Exception as e:
        print(f"Error reading webpage: {e}")
        return {"error": str(e)}


def search_web(query: str, site: Optional[str] = None, with_links: bool = False, with_images: bool = False, no_cache: bool = False) -> Dict[str, Any]:
    """
    Search the web for information using Jina AI Search API.
    
    Args:
        query: Search query
        site: Optional domain to limit search to
        with_links: Whether to include links in the response
        with_images: Whether to include images in the response
        no_cache: Whether to bypass cache for fresh retrieval
        
    Returns:
        Dictionary containing the search results
    """
    search_url = "https://s.jina.ai/"
    
    headers = BASE_HEADERS.copy()
    
    if site:
        headers["X-Site"] = site
    if with_links:
        headers["X-With-Links-Summary"] = "true"
    if with_images:
        headers["X-With-Images-Summary"] = "true"
    if no_cache:
        headers["X-No-Cache"] = "true"
    
    payload = {"q": query}
    
    try:
        response = handle_request_with_retry("POST", search_url, headers, payload)
        return response.json()
    except Exception as e:
        print(f"Error searching web: {e}")
        return {"error": str(e)}


def deep_search(query: str, reasoning_effort: str = "medium", stream: bool = False) -> Dict[str, Any]:
    """
    Perform a deep search that combines web searching, reading, and reasoning using Jina AI DeepSearch API.
    
    Args:
        query: Search query
        reasoning_effort: Effort level for reasoning (low, medium, high)
        stream: Whether to stream the response
        
    Returns:
        Dictionary containing the deep search results
    """
    url = "https://deepsearch.jina.ai/v1/chat/completions"
    
    payload = {
        "model": "jina-deepsearch-v1",
        "messages": [
            {"role": "user", "content": query}
        ],
        "reasoning_effort": reasoning_effort,
        "stream": stream
    }
    
    try:
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error performing deep search: {e}")
        return {"error": str(e)}


def segment_text(content: str, tokenizer: str = "cl100k_base", return_tokens: bool = False, return_chunks: bool = True, max_chunk_length: int = 1000) -> Dict[str, Any]:
    """
    Segment text into tokens and chunks using Jina AI Segmenter API.
    
    Args:
        content: Text content to segment
        tokenizer: Tokenizer to use
        return_tokens: Whether to include tokens in the response
        return_chunks: Whether to segment the text into chunks
        max_chunk_length: Maximum characters per chunk
        
    Returns:
        Dictionary containing the segmentation results
    """
    url = "https://segment.jina.ai/"
    
    payload = {
        "content": content,
        "tokenizer": tokenizer,
        "return_tokens": return_tokens,
        "return_chunks": return_chunks,
        "max_chunk_length": max_chunk_length
    }
    
    try:
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error segmenting text: {e}")
        return {"error": str(e)}


def classify_text(texts: List[str], labels: List[str], model: str = "jina-embeddings-v3") -> Dict[str, Any]:
    """
    Classify text into categories using Jina AI Classifier API.
    
    Args:
        texts: List of text inputs to classify
        labels: List of labels to classify into
        model: Model to use for classification
        
    Returns:
        Dictionary containing the classification results
    """
    url = "https://api.jina.ai/v1/classify"
    
    payload = {
        "model": model,
        "input": texts,
        "labels": labels
    }
    
    try:
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error classifying text: {e}")
        return {"error": str(e)}


def classify_image(image_path: str, labels: List[str], model: str = "jina-clip-v2") -> Dict[str, Any]:
    """
    Classify an image into categories using Jina AI Classifier API.
    
    Args:
        image_path: Path to the image file
        labels: List of labels to classify into
        model: Model to use for classification
        
    Returns:
        Dictionary containing the classification results
    """
    url = "https://api.jina.ai/v1/classify"
    
    try:
        # Read and encode the image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        payload = {
            "model": model,
            "input": [{"image": image_data}],
            "labels": labels
        }
        
        response = handle_request_with_retry("POST", url, BASE_HEADERS, payload)
        return response.json()
    except Exception as e:
        print(f"Error classifying image: {e}")
        return {"error": str(e)}


def enhanced_search_with_reranking(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform an enhanced search with reranking.
    
    This function first searches the web using the Search API, then reranks the results
    using the Reranker API to find the most relevant results.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of reranked search results
    """
    # Step 1: Search the web
    search_results = search_web(query)
    
    if "error" in search_results:
        return [{"error": search_results["error"]}]
    
    # Extract content from search results
    documents = []
    original_results = []
    
    for result in search_results.get("data", []):
        content = result.get("content", "")
        if content:
            documents.append(content)
            original_results.append(result)
    
    if not documents:
        return [{"message": "No search results found"}]
    
    # Step 2: Rerank the results
    reranked_results = rerank_documents(query, documents, top_n=num_results)
    
    if "error" in reranked_results:
        return [{"error": reranked_results["error"]}]
    
    # Step 3: Combine the reranked results with the original metadata
    final_results = []
    
    for reranked in reranked_results.get("results", []):
        index = reranked.get("index", 0)
        if index < len(original_results):
            result = original_results[index].copy()
            result["relevance_score"] = reranked.get("relevance_score", 0)
            final_results.append(result)
    
    return final_results


def web_content_processing(url: str) -> Dict[str, Any]:
    """
    Process web content by first reading a webpage and then generating embeddings for its content.
    
    Args:
        url: URL of the webpage to process
        
    Returns:
        Dictionary containing the processed content and embeddings
    """
    # Step 1: Read the webpage
    webpage_data = read_webpage(url)
    
    if "error" in webpage_data:
        return {"error": webpage_data["error"]}
    
    # Extract content from the webpage
    content = webpage_data.get("data", {}).get("content", "")
    
    if not content:
        return {"error": "No content found in the webpage"}
    
    # Step 2: Generate embeddings for the content
    embeddings_result = get_embeddings([content])
    
    if "error" in embeddings_result:
        return {"error": embeddings_result["error"]}
    
    # Return the processed data
    return {
        "webpage": {
            "title": webpage_data.get("data", {}).get("title", ""),
            "description": webpage_data.get("data", {}).get("description", ""),
            "url": url,
            "content": content
        },
        "embeddings": embeddings_result
    }


def demonstrate_all_apis():
    """
    Demonstrate all Jina AI Search Foundation APIs.
    """
    print("\n" + "=" * 80)
    print("Jina AI Search Foundation API Demo")
    print("=" * 80)
    
    # 1. Embeddings API
    print("\n1. Embeddings API Example:")
    texts = ["Hello, world!", "Jina AI provides powerful search APIs"]
    embeddings_result = get_embeddings(texts)
    print(f"Generated embeddings for {len(texts)} texts")
    print(f"Embedding dimensions: {len(embeddings_result.get('data', [{}])[0].get('embedding', []))}")
    print(f"Token usage: {embeddings_result.get('usage', {}).get('total_tokens', 0)}")
    
    # 2. Reranker API
    print("\n2. Reranker API Example:")
    query = "What is Jina AI?"
    documents = [
        "Jina AI is a company that provides search foundation models.",
        "Jina AI offers embeddings, rerankers, and other search APIs.",
        "Apple is a fruit that grows on trees."
    ]
    reranker_result = rerank_documents(query, documents)
    print("Reranked documents by relevance:")
    for result in reranker_result.get("results", []):
        print(f"  - Score: {result.get('relevance_score', 0):.4f} | {result.get('document', {}).get('text', '')}")
    
    # 3. Reader API
    print("\n3. Reader API Example:")
    reader_result = read_webpage("https://jina.ai", with_links=True)
    print(f"Read webpage: {reader_result.get('data', {}).get('title', '')}")
    print(f"Description: {reader_result.get('data', {}).get('description', '')}")
    content_preview = reader_result.get('data', {}).get('content', '')[:150] + "..."
    print(f"Content preview: {content_preview}")
    print(f"Number of links: {len(reader_result.get('data', {}).get('links', {}))}")
    
    # 4. Search API
    print("\n4. Search API Example:")
    search_result = search_web("Jina AI embeddings")
    print(f"Found {len(search_result.get('data', []))} search results")
    for i, result in enumerate(search_result.get('data', [])[:3]):
        print(f"  Result {i+1}: {result.get('title', '')}")
        print(f"    URL: {result.get('url', '')}")
    
    # 5. Enhanced Search with Reranking
    print("\n5. Enhanced Search with Reranking Example:")
    enhanced_results = enhanced_search_with_reranking("Jina AI embeddings models")
    print(f"Found {len(enhanced_results)} reranked search results")
    for i, result in enumerate(enhanced_results[:3]):
        print(f"  Result {i+1} (Score: {result.get('relevance_score', 0):.4f}): {result.get('title', '')}")
        print(f"    URL: {result.get('url', '')}")
    
    # 6. Segmenter API
    print("\n6. Segmenter API Example:")
    text_to_segment = """Jina AI provides powerful search foundation models. 
    These models include embeddings, rerankers, and more. 
    They can be used for various search and AI-related tasks."""
    segmenter_result = segment_text(text_to_segment)
    print(f"Segmented text into {segmenter_result.get('num_chunks', 0)} chunks")
    print(f"Number of tokens: {segmenter_result.get('num_tokens', 0)}")
    for i, chunk in enumerate(segmenter_result.get('chunks', [])):
        print(f"  Chunk {i+1}: {chunk}")
    
    # 7. Classifier API (Text)
    print("\n7. Classifier API (Text) Example:")
    texts_to_classify = ["I love this product!", "This product is terrible."]
    labels = ["positive", "negative", "neutral"]
    text_classifier_result = classify_text(texts_to_classify, labels)
    print("Text classification results:")
    for i, result in enumerate(text_classifier_result.get('data', [])):
        print(f"  Text: '{texts_to_classify[i]}'")
        print(f"  Prediction: {result.get('prediction', '')} (Score: {result.get('score', 0):.4f})")
    
    # 8. Web Content Processing
    print("\n8. Web Content Processing Example:")
    print("This example combines Reader API and Embeddings API")
    print("(Skipping actual execution to avoid redundancy)")
    
    # 9. DeepSearch API
    print("\n9. DeepSearch API Example:")
    print("Note: DeepSearch can take some time to complete")
    deep_search_query = "What are the latest developments in AI search technology?"
    print(f"Query: {deep_search_query}")
    print("(Skipping actual execution as it can take time and generate a lot of output)")
    print("In a real application, you would call:")
    print(f"  deep_search_result = deep_search(\"{deep_search_query}\", reasoning_effort=\"medium\")")
    
    print("\n" + "=" * 80)
    print("Demo completed! This demonstrates the basic usage of Jina AI Search Foundation APIs.")
    print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    demonstrate_all_apis()
