# Jina AI Search Foundation API Demo

This repository contains a Python application that demonstrates how to use Jina AI Search Foundation APIs for various search and AI-related tasks.

## Overview

Jina AI provides a suite of powerful APIs for search, embeddings, classification, and more. This application demonstrates how to use these APIs for common use cases.

## Features

- **Embeddings API**: Convert text/images to fixed-length vectors for semantic search, similarity matching, clustering, etc.
- **Reranker API**: Find the most relevant search results for a given query.
- **Reader API**: Retrieve/parse content from URLs in a format optimized for downstream tasks.
- **Search API**: Search the web for information and return results in a format optimized for downstream tasks.
- **DeepSearch API**: Combines web searching, reading, and reasoning for comprehensive investigation.
- **Segmenter API**: Tokenize text and divide it into manageable chunks.
- **Classifier API**: Zero-shot classification for text or images.

## Prerequisites

- Python 3.8 or higher
- Required Python packages (install via `pip install -r requirements.txt`)
- Jina AI API key (get it from [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/esun126/jina-test.git
   cd jina-test
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Jina AI API key as an environment variable:
   ```bash
   # On Linux/macOS
   export JINA_API_KEY="your-api-key-here"
   
   # On Windows (Command Prompt)
   set JINA_API_KEY=your-api-key-here
   
   # On Windows (PowerShell)
   $env:JINA_API_KEY="your-api-key-here"
   ```

## Usage

Run the main application:

```bash
python app.py
```

This will demonstrate various use cases of Jina AI APIs.

## Examples

The application includes examples of:

1. Basic search using the Search API
2. Enhanced search with reranking
3. Text and image classification
4. Web content processing
5. Text segmentation and tokenization
6. Generating embeddings for text and images
7. Deep search for comprehensive investigation

## License

MIT

## Acknowledgements

- [Jina AI](https://jina.ai/) for providing the Search Foundation APIs
- Get your Jina AI API key for free: [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey)
