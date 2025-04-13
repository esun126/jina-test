#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Document Learning Web Application Test Case

This script demonstrates how to use the web application to learn from online documents.
It launches the web application and provides instructions for testing it.

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import sys
import webbrowser
import time
from threading import Timer
from web_app import app

def open_browser():
    """
    Open the web browser to the application URL.
    """
    webbrowser.open('http://localhost:5000')

def print_test_instructions():
    """
    Print instructions for testing the web application.
    """
    print("\n" + "=" * 80)
    print("Jina AI Document Learning Web Application Test Case")
    print("=" * 80)
    
    print("\nThe web application has been launched and should open in your browser.")
    print("If it doesn't open automatically, go to: http://localhost:5000")
    
    print("\nTest Case Instructions:")
    print("1. Enter a document URL in the 'Document URL' field")
    print("   Example URLs to try:")
    print("   - https://jina.ai/blog/embeddings-v3/")
    print("   - https://jina.ai/blog/reranker-v2/")
    print("   - https://en.wikipedia.org/wiki/Artificial_intelligence")
    
    print("\n2. Enter your Jina API key in the 'Jina API Key' field")
    print("   You can get a free API key from: https://jina.ai/?sui=apikey")
    
    print("\n3. Click the 'Process Document' button and wait for the document to be processed")
    
    print("\n4. Once the document is processed, you can ask questions about it")
    print("   Example questions to try:")
    print("   - What are the key features of Jina embeddings?")
    print("   - How does the reranker work?")
    print("   - What are the applications of AI?")
    
    print("\n5. To process a different document, click the 'Clear Session' button")
    
    print("\nPress Ctrl+C to stop the web application when you're done testing.")
    print("=" * 80 + "\n")

def main():
    """
    Main function to run the test case.
    """
    # Check if the Jina API key is set
    api_key = os.environ.get("JINA_API_KEY")
    if not api_key:
        print("Warning: JINA_API_KEY environment variable is not set.")
        print("You will need to enter your API key in the web interface.")
        print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    
    # Print instructions
    print_test_instructions()
    
    # Open browser after a short delay
    Timer(1.5, open_browser).start()
    
    # Run the Flask application
    app.run(debug=False)

if __name__ == "__main__":
    main()
