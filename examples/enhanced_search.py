#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Enhanced Search Example

This script demonstrates how to use Jina AI's Search API and Reranker API together
to perform enhanced search with reranking for more relevant results.

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
    from app import search_web, rerank_documents
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
    
    def search_web(query: str, site: str = None, with_links: bool = False, with_images: bool = False, no_cache: bool = False) -> Dict[str, Any]:
        """
        Search the web for information using Jina AI Search API.
        """
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        search_url = "https://s.jina.ai/"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
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
            return {"error": str(e)}
    
    def rerank_documents(query: str, documents: List[str], model: str = "jina-reranker-v2-base-multilingual", top_n: int = None) -> Dict[str, Any]:
        """
        Rerank a list of documents based on relevance to a query using Jina AI Reranker API.
        """
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        url = "https://api.jina.ai/v1/rerank"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": model,
            "query": query,
            "documents": documents
        }
        
        if top_n is not None:
            payload["top_n"] = top_n
        
        try:
            response = handle_request_with_retry("POST", url, headers, payload)
            return response.json()
        except Exception as e:
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
    print(f"Searching for: {query}")
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
    
    print(f"Found {len(documents)} search results")
    
    # Step 2: Rerank the results
    print("\nReranking search results...")
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
    
    print(f"Successfully reranked results. Returning top {len(final_results)} results")
    
    return final_results


def main():
    """
    Main function to demonstrate enhanced search with reranking.
    """
    # Check if a search query was provided
    if len(sys.argv) < 2:
        print("Usage: python enhanced_search.py <search_query>")
        print("Example: python enhanced_search.py \"Jina AI embeddings models\"")
        return
    
    query = sys.argv[1]
    
    print("\n" + "=" * 80)
    print("Jina AI Enhanced Search Example")
    print("=" * 80)
    
    # Perform enhanced search with reranking
    results = enhanced_search_with_reranking(query)
    
    if results and "error" in results[0]:
        print(f"\nError: {results[0]['error']}")
        return
    
    if results and "message" in results[0]:
        print(f"\n{results[0]['message']}")
        return
    
    # Display the results
    print("\nSearch Results (ranked by relevance):")
    for i, result in enumerate(results):
        print(f"\nResult {i+1} (Relevance Score: {result.get('relevance_score', 0):.4f})")
        print(f"  Title: {result.get('title', '')}")
        print(f"  URL: {result.get('url', '')}")
        description = result.get('description', '')
        if description:
            print(f"  Description: {description}")
        content_preview = result.get('content', '')[:200] + "..." if len(result.get('content', '')) > 200 else result.get('content', '')
        if content_preview:
            print(f"  Content preview: {content_preview}")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
