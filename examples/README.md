# Jina AI Search Foundation API Examples

This directory contains example scripts that demonstrate how to use Jina AI Search Foundation APIs for various use cases.

## Prerequisites

Before running these examples, make sure you have:

1. Installed the required packages:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Set your Jina AI API key as an environment variable:
   ```bash
   # On Linux/macOS
   export JINA_API_KEY="your-api-key-here"
   
   # On Windows (Command Prompt)
   set JINA_API_KEY=your-api-key-here
   
   # On Windows (PowerShell)
   $env:JINA_API_KEY="your-api-key-here"
   ```

   Alternatively, you can create a `.env` file in the root directory with the following content:
   ```
   JINA_API_KEY=your-api-key-here
   ```

## Examples

### 1. Image Classification

This example demonstrates how to use Jina AI's Classifier API to classify images into categories.

**Usage:**
```bash
python image_classification.py <path_to_image>
```

**Example:**
```bash
python image_classification.py sample_image.jpg
```

### 2. Web Content Processing

This example demonstrates how to use Jina AI's Reader API and Embeddings API together to process web content and generate embeddings for the content.

**Usage:**
```bash
python web_content_processing.py <url>
```

**Example:**
```bash
python web_content_processing.py https://jina.ai
```

### 3. Enhanced Search with Reranking

This example demonstrates how to use Jina AI's Search API and Reranker API together to perform enhanced search with reranking for more relevant results.

**Usage:**
```bash
python enhanced_search.py "<search_query>"
```

**Example:**
```bash
python enhanced_search.py "Jina AI embeddings models"
```

### 4. Document Learning

This example demonstrates how to use Jina AI APIs to learn from online documents. It shows how to extract content from documents, process them, and answer questions based on their content.

**Usage:**
```bash
python document_learning.py <url1> [<url2> ...]
```

**Example:**
```bash
python document_learning.py https://jina.ai/blog/embeddings-v3/ https://jina.ai/blog/reranker-v2/
```

This example creates an interactive question-answering system that allows you to ask questions about the documents you've provided. The system will:
1. Extract content from the provided URLs using the Reader API
2. Segment the content into chunks using the Segmenter API
3. Generate embeddings for the chunks using the Embeddings API
4. Find relevant chunks for your questions using semantic search
5. Present the most relevant information as answers

## Additional Examples

For more examples and comprehensive demonstrations of all Jina AI Search Foundation APIs, check out the main application file (`app.py`) in the root directory.

## Get Your API Key

Get your Jina AI API key for free: [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey)
