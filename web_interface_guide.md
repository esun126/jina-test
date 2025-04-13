# Jina AI Document Learning Web Interface Guide

## Overview

The Jina AI Document Learning Web Interface provides a user-friendly way to interact with Jina AI APIs for learning from online documents. This guide explains how to use the web interface.

## Interface Layout

The web interface is divided into several sections:

1. **Document Processing Section** (Left side)
   - Form for entering a document URL and Jina API key
   - Document information display after processing

2. **Question Answering Section** (Right side)
   - Form for asking questions about the processed document
   - Answer display with sources

3. **How It Works Section** (Bottom)
   - Explanation of the document learning process

## How to Use

### Step 1: Process a Document

1. Enter the URL of the document you want to process in the "Document URL" field
2. Enter your Jina API key in the "Jina API Key" field
   - You can get a free API key from [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey)
3. Click the "Process Document" button
4. Wait for the document to be processed
   - The system will extract content from the URL using Jina's Reader API
   - The content will be segmented into chunks using Jina's Segmenter API
   - Embeddings will be generated for the chunks using Jina's Embeddings API
5. Once processing is complete, document information will be displayed
   - Title of the document
   - URL of the document
   - Number of chunks extracted
   - Preview of the document content

### Step 2: Ask Questions

1. After a document has been processed, the question form will appear
2. Enter your question in the "Your Question" field
3. Click the "Ask" button
4. Wait for the system to find the most relevant information
5. The answer will be displayed along with the sources of the information

### Step 3: Clear Session (Optional)

1. If you want to start over or process a different document, click the "Clear Session" button
2. This will remove all processed documents and reset the interface

## Example Use Cases

### Learning from Technical Documentation

1. Process a technical documentation page (e.g., a programming language documentation)
2. Ask questions about specific features, syntax, or usage examples

### Extracting Information from Research Papers

1. Process a research paper or academic article
2. Ask questions about the methodology, results, or conclusions

### Understanding News Articles

1. Process a news article
2. Ask questions about the events, people, or organizations mentioned

## Tips for Best Results

1. **Choose Focused Documents**: The system works best with documents that have a clear focus on a specific topic
2. **Ask Specific Questions**: More specific questions tend to get more accurate answers
3. **Process Multiple Documents**: For comprehensive understanding, process multiple related documents
4. **Check Sources**: Always verify the sources of the information provided in the answers

## Troubleshooting

- **Error Processing Document**: Check that the URL is valid and accessible
- **API Key Issues**: Ensure your Jina API key is correct and has not expired
- **No Answer**: Try rephrasing your question or processing a more relevant document

## Privacy Note

Your Jina API key is only used for making API requests and is not stored permanently. It is kept in the session for the duration of your interaction with the web interface.
