#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Web Content Processing Example

This script demonstrates how to use Jina AI's Reader API and Embeddings API together
to process web content and generate embeddings for the content.

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import sys
import json
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from app.py, but provide fallback implementations if it fails
try:
    from app import read_webpage, get_embeddings
except ImportError:
    # Fallback implementations if app.py is not available
    def handle_request_with_retry(method, url, headers, json_data=None, max_retries=3, retry_delay=1):
        """
        Handle API requests with retry logic for network failures.
        """
        import time
        
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
    
    def read_webpage(url: str, with_links: bool = False, with_images: bool = False, no_cache: bool = False) -> Dict[str, Any]:
        """
        Read and parse content from a URL using Jina AI Reader API.
        """
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        reader_url = "https://r.jina.ai/"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
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
            return {"error": str(e)}
    
    def get_embeddings(texts: List[str], model: str = "jina-embeddings-v3", normalized: bool = True) -> Dict[str, Any]:
        """
        Generate embeddings for a list of text inputs using Jina AI Embeddings API.
        """
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        url = "https://api.jina.ai/v1/embeddings"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": model,
            "input": texts,
            "normalized": normalized
        }
        
        try:
            response = handle_request_with_retry("POST", url, headers, payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def web_content_processing(url: str) -> Dict[str, Any]:
    """
    Process web content by first reading a webpage and then generating embeddings for its content.
    
    Args:
        url: URL of the webpage to process
        
    Returns:
        Dictionary containing the processed content and embeddings
    """
    # Step 1: Read the webpage
    print(f"Reading webpage: {url}")
    webpage_data = read_webpage(url, with_links=True)
    
    if "error" in webpage_data:
        return {"error": webpage_data["error"]}
    
    # Extract content from the webpage
    content = webpage_data.get("data", {}).get("content", "")
    
    if not content:
        return {"error": "No content found in the webpage"}
    
    print(f"Successfully read webpage. Title: {webpage_data.get('data', {}).get('title', '')}")
    print(f"Content length: {len(content)} characters")
    
    # Step 2: Generate embeddings for the content
    print("\nGenerating embeddings for the webpage content...")
    embeddings_result = get_embeddings([content])
    
    if "error" in embeddings_result:
        return {"error": embeddings_result["error"]}
    
    print("Successfully generated embeddings")
    
    # Return the processed data
    return {
        "webpage": {
            "title": webpage_data.get("data", {}).get("title", ""),
            "description": webpage_data.get("data", {}).get("description", ""),
            "url": url,
            "content_preview": content[:200] + "..." if len(content) > 200 else content,
            "links": webpage_data.get("data", {}).get("links", {})
        },
        "embeddings": {
            "dimensions": len(embeddings_result.get("data", [{}])[0].get("embedding", [])),
            "model": "jina-embeddings-v3",
            "usage": embeddings_result.get("usage", {})
        }
    }


def main():
    """
    Main function to demonstrate web content processing.
    """
    # Check if a URL was provided
    if len(sys.argv) < 2:
        print("Usage: python web_content_processing.py <url>")
        print("Example: python web_content_processing.py https://jina.ai")
        return
    
    url = sys.argv[1]
    
    print("\n" + "=" * 80)
    print("Jina AI Web Content Processing Example")
    print("=" * 80)
    
    # Process the web content
    result = web_content_processing(url)
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    # Display the results
    print("\nResults:")
    print(f"  Title: {result['webpage']['title']}")
    print(f"  Description: {result['webpage']['description']}")
    print(f"  URL: {result['webpage']['url']}")
    print(f"  Content preview: {result['webpage']['content_preview']}")
    print(f"  Number of links: {len(result['webpage']['links'])}")
    print(f"  Embedding dimensions: {result['embeddings']['dimensions']}")
    print(f"  Embedding model: {result['embeddings']['model']}")
    print(f"  Token usage: {result['embeddings']['usage'].get('total_tokens', 0)}")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
