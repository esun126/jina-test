#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Document Learning Example

This script demonstrates how to use Jina AI APIs to learn from online documents.
It shows how to:
1. Extract content from online documents using the Reader API
2. Segment the content into chunks using the Segmenter API
3. Generate embeddings for the chunks using the Embeddings API
4. Implement a simple retrieval system to answer questions based on the document content

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import sys
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
import requests

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from app.py, but provide fallback implementations if it fails
try:
    from app import read_webpage, segment_text, get_embeddings
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
    
    def segment_text(content: str, tokenizer: str = "cl100k_base", return_tokens: bool = False, return_chunks: bool = True, max_chunk_length: int = 1000) -> Dict[str, Any]:
        """
        Segment text into tokens and chunks using Jina AI Segmenter API.
        """
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        url = "https://segment.jina.ai/"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "content": content,
            "tokenizer": tokenizer,
            "return_tokens": return_tokens,
            "return_chunks": return_chunks,
            "max_chunk_length": max_chunk_length
        }
        
        try:
            response = handle_request_with_retry("POST", url, headers, payload)
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


class DocumentLearner:
    """
    A class for learning from online documents using Jina AI APIs.
    """
    
    def __init__(self, chunk_size: int = 1000):
        """
        Initialize the DocumentLearner.
        
        Args:
            chunk_size: Maximum characters per chunk when segmenting text
        """
        self.chunk_size = chunk_size
        self.documents = []
        self.chunks = []
        self.embeddings = []
        self.sources = []
    
    def add_document(self, url: str) -> bool:
        """
        Add a document to the learner by reading its content from a URL.
        
        Args:
            url: URL of the document to read
            
        Returns:
            True if the document was successfully added, False otherwise
        """
        print(f"Reading document from: {url}")
        
        # Read the document
        result = read_webpage(url)
        
        if "error" in result:
            print(f"Error reading document: {result['error']}")
            return False
        
        # Extract content from the document
        content = result.get("data", {}).get("content", "")
        title = result.get("data", {}).get("title", "")
        
        if not content:
            print("No content found in the document")
            return False
        
        print(f"Successfully read document: {title}")
        print(f"Content length: {len(content)} characters")
        
        # Segment the content into chunks
        print("Segmenting content into chunks...")
        segmentation_result = segment_text(content, max_chunk_length=self.chunk_size)
        
        if "error" in segmentation_result:
            print(f"Error segmenting content: {segmentation_result['error']}")
            return False
        
        chunks = segmentation_result.get("chunks", [])
        
        if not chunks:
            print("No chunks found in the segmented content")
            return False
        
        print(f"Successfully segmented content into {len(chunks)} chunks")
        
        # Generate embeddings for the chunks
        print("Generating embeddings for chunks...")
        embeddings_result = get_embeddings(chunks)
        
        if "error" in embeddings_result:
            print(f"Error generating embeddings: {embeddings_result['error']}")
            return False
        
        embeddings_data = embeddings_result.get("data", [])
        
        if not embeddings_data:
            print("No embeddings found in the result")
            return False
        
        # Extract embeddings from the result
        chunk_embeddings = [data.get("embedding", []) for data in embeddings_data]
        
        if not all(chunk_embeddings):
            print("Some chunks have no embeddings")
            return False
        
        print(f"Successfully generated embeddings for {len(chunk_embeddings)} chunks")
        
        # Store the document, chunks, and embeddings
        self.documents.append({
            "url": url,
            "title": title,
            "content": content
        })
        
        for i, chunk in enumerate(chunks):
            self.chunks.append(chunk)
            self.embeddings.append(chunk_embeddings[i])
            self.sources.append({
                "document_index": len(self.documents) - 1,
                "url": url,
                "title": title
            })
        
        print(f"Document added successfully. Total chunks: {len(self.chunks)}")
        return True
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on a query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant chunks with their sources and similarity scores
        """
        if not self.chunks:
            print("No documents have been added yet")
            return []
        
        print(f"Searching for: {query}")
        
        # Generate embedding for the query
        query_embedding_result = get_embeddings([query])
        
        if "error" in query_embedding_result:
            print(f"Error generating query embedding: {query_embedding_result['error']}")
            return []
        
        query_embedding_data = query_embedding_result.get("data", [])
        
        if not query_embedding_data:
            print("No query embedding found in the result")
            return []
        
        query_embedding = query_embedding_data[0].get("embedding", [])
        
        if not query_embedding:
            print("Query has no embedding")
            return []
        
        # Calculate similarity scores
        similarities = []
        for chunk_embedding in self.embeddings:
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, chunk_embedding)
            similarities.append(similarity)
        
        # Get top-k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            results.append({
                "chunk": self.chunks[idx],
                "similarity": similarities[idx],
                "source": self.sources[idx]
            })
        
        print(f"Found {len(results)} relevant chunks")
        return results
    
    def answer_question(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Answer a question based on the documents that have been added.
        
        Args:
            question: Question to answer
            top_k: Number of top chunks to consider
            
        Returns:
            Dictionary containing the answer and relevant sources
        """
        if not self.chunks:
            return {"answer": "No documents have been added yet", "sources": []}
        
        print(f"Answering question: {question}")
        
        # Search for relevant chunks
        relevant_chunks = self.search(question, top_k=top_k)
        
        if not relevant_chunks:
            return {"answer": "No relevant information found", "sources": []}
        
        # Combine the relevant chunks into a context
        context = "\n\n".join([result["chunk"] for result in relevant_chunks])
        
        # In a real application, you would use an LLM to generate an answer based on the context
        # Since we don't have access to an LLM in this example, we'll just return the most relevant chunk
        answer = relevant_chunks[0]["chunk"]
        
        # Extract sources
        sources = []
        for result in relevant_chunks:
            source = result["source"]
            if source not in sources:
                sources.append(source)
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Cosine similarity between the vectors
        """
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    """
    Main function to demonstrate document learning.
    """
    # Check if URLs were provided
    if len(sys.argv) < 2:
        print("Usage: python document_learning.py <url1> [<url2> ...]")
        print("Example: python document_learning.py https://jina.ai/blog/embeddings-v3/ https://jina.ai/blog/reranker-v2/")
        return
    
    urls = sys.argv[1:]
    
    print("\n" + "=" * 80)
    print("Jina AI Document Learning Example")
    print("=" * 80)
    
    # Create a document learner
    learner = DocumentLearner(chunk_size=1000)
    
    # Add documents
    for url in urls:
        success = learner.add_document(url)
        if not success:
            print(f"Failed to add document from URL: {url}")
        print()
    
    if not learner.chunks:
        print("No documents were successfully added. Exiting.")
        return
    
    # Interactive question answering
    print("\nDocuments have been processed and indexed.")
    print("You can now ask questions about the documents.")
    print("Type 'exit' to quit.")
    
    while True:
        print("\n" + "-" * 40)
        question = input("Ask a question: ")
        print("-" * 40)
        
        if question.lower() == "exit":
            break
        
        result = learner.answer_question(question)
        
        print("\nAnswer:")
        print(result["answer"])
        
        if result["sources"]:
            print("\nSources:")
            for i, source in enumerate(result["sources"]):
                print(f"  {i+1}. {source['title']} ({source['url']})")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
