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

### Command-Line Application

Run the main application:

```bash
python app.py
```

This will demonstrate various use cases of Jina AI APIs.

### Web Application

The repository includes a web application that provides a user-friendly interface for learning from online documents using Jina AI APIs.

To run the web application:

```bash
python web_app.py
```

Then open your browser and navigate to `http://localhost:5000`.

The web application allows you to:
1. Enter a document URL and your Jina API key
2. Process the document using Jina AI APIs
3. Ask questions about the document
4. Get answers based on the document content

For detailed instructions on using the web interface, see the [Web Interface Guide](web_interface_guide.md).

### Test Case

To quickly test the web application with sample documents and questions, run:

```bash
python test_web_app.py
```

This will launch the web application and open it in your browser, along with instructions for testing it with sample documents and questions.

## Examples

The repository includes several example scripts in the `examples` directory:

1. **Image Classification**: Classify images into categories using the Classifier API.
   ```bash
   python examples/image_classification.py sample_image.jpg
   ```

2. **Web Content Processing**: Process web content and generate embeddings using the Reader API and Embeddings API.
   ```bash
   python examples/web_content_processing.py https://jina.ai
   ```

3. **Enhanced Search with Reranking**: Perform enhanced search with reranking using the Search API and Reranker API.
   ```bash
   python examples/enhanced_search.py "Jina AI embeddings models"
   ```

4. **Document Learning**: Learn from online documents and answer questions about them using multiple Jina AI APIs.
   ```bash
   python examples/document_learning.py https://jina.ai/blog/embeddings-v3/ https://jina.ai/blog/reranker-v2/
   ```
   This example creates an interactive question-answering system that allows you to ask questions about the documents you've provided.

See the [examples README](examples/README.md) for more details.

## License

MIT

## Acknowledgements

- [Jina AI](https://jina.ai/) for providing the Search Foundation APIs
- Get your Jina AI API key for free: [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey)
