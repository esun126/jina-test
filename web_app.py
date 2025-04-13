#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Document Learning Web Application

This web application provides a user interface for learning from online documents using Jina AI APIs.
Users can enter a URL and their Jina API key to extract and process information from online documents.

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session
from examples.document_learning import DocumentLearner

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Store document learners for each session
document_learners = {}

@app.route('/')
def index():
    """
    Render the main page of the web application.
    """
    return render_template('index.html')

@app.route('/process_document', methods=['POST'])
def process_document():
    """
    Process a document URL using Jina AI APIs.
    """
    data = request.json
    url = data.get('url')
    api_key = data.get('api_key')
    
    if not url or not api_key:
        return jsonify({
            'success': False,
            'message': 'URL and API key are required'
        })
    
    # Set the API key as an environment variable
    os.environ['JINA_API_KEY'] = api_key
    
    # Get or create a document learner for this session
    session_id = session.get('session_id')
    if not session_id:
        session_id = os.urandom(24).hex()
        session['session_id'] = session_id
        document_learners[session_id] = DocumentLearner(chunk_size=1000)
    
    learner = document_learners[session_id]
    
    # Process the document
    try:
        success = learner.add_document(url)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Failed to process the document. Please check the URL and API key.'
            })
        
        # Get document information
        document_info = learner.documents[-1]
        
        return jsonify({
            'success': True,
            'message': 'Document processed successfully',
            'document': {
                'title': document_info['title'],
                'url': document_info['url'],
                'content_preview': document_info['content'][:200] + '...' if len(document_info['content']) > 200 else document_info['content'],
                'num_chunks': len(learner.chunks)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing document: {str(e)}'
        })

@app.route('/ask_question', methods=['POST'])
def ask_question():
    """
    Answer a question based on the processed documents.
    """
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({
            'success': False,
            'message': 'Question is required'
        })
    
    # Get the document learner for this session
    session_id = session.get('session_id')
    if not session_id or session_id not in document_learners:
        return jsonify({
            'success': False,
            'message': 'No documents have been processed yet. Please add a document first.'
        })
    
    learner = document_learners[session_id]
    
    # Answer the question
    try:
        result = learner.answer_question(question)
        
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'sources': result['sources']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error answering question: {str(e)}'
        })

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """
    Clear the current session and remove all processed documents.
    """
    session_id = session.get('session_id')
    if session_id and session_id in document_learners:
        del document_learners[session_id]
    
    session.clear()
    
    return jsonify({
        'success': True,
        'message': 'Session cleared successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)
