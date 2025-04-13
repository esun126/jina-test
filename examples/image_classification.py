#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jina AI Image Classification Example

This script demonstrates how to use Jina AI's Classifier API to classify images.

Get your Jina AI API key for free: https://jina.ai/?sui=apikey
"""

import os
import sys
import base64
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from app.py, but provide a fallback implementation if it fails
try:
    from app import classify_image
except ImportError:
    # Fallback implementation if app.py is not available
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
        # Load environment variables from .env file (if it exists)
        load_dotenv()
        
        # Get API key from environment variable
        API_KEY = os.environ.get("JINA_API_KEY")
        if not API_KEY:
            return {"error": "JINA_API_KEY environment variable is not set. Get your Jina AI API key for free: https://jina.ai/?sui=apikey"}
        
        url = "https://api.jina.ai/v1/classify"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")
            
            payload = {
                "model": model,
                "input": [{"image": image_data}],
                "labels": labels
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def main():
    """
    Main function to demonstrate image classification.
    """
    # Check if an image path was provided
    if len(sys.argv) < 2:
        print("Usage: python image_classification.py <path_to_image>")
        print("Example: python image_classification.py sample_image.jpg")
        return
    
    image_path = sys.argv[1]
    
    # Check if the image file exists
    if not os.path.isfile(image_path):
        print(f"Error: Image file '{image_path}' does not exist.")
        return
    
    print("\n" + "=" * 80)
    print("Jina AI Image Classification Example")
    print("=" * 80)
    
    # Define labels for classification
    labels = [
        "landscape", "portrait", "food", "animal", "building", 
        "vehicle", "plant", "indoor", "outdoor", "text"
    ]
    
    print(f"\nClassifying image: {image_path}")
    print(f"Using labels: {', '.join(labels)}")
    
    # Classify the image
    result = classify_image(image_path, labels)
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    # Display the classification results
    print("\nClassification Results:")
    
    data = result.get("data", [])
    if data:
        prediction = data[0].get("prediction", "")
        score = data[0].get("score", 0)
        print(f"  Predicted category: {prediction} (confidence: {score:.4f})")
        
        # If detailed predictions are available, show them
        predictions = data[0].get("predictions", [])
        if predictions:
            print("\nDetailed predictions:")
            for pred in sorted(predictions, key=lambda x: x.get("score", 0), reverse=True):
                label = pred.get("label", "")
                score = pred.get("score", 0)
                print(f"  - {label}: {score:.4f}")
    else:
        print("  No classification results found.")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("Get your Jina AI API key for free: https://jina.ai/?sui=apikey")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
