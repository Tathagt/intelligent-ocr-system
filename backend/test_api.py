"""
Test script for the OCR API
Run this to verify the API is working correctly
"""

import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"  # Change this to your deployed URL

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_process_document(image_path):
    """Test document processing with an image"""
    print(f"Testing document processing with {image_path}...")
    
    if not Path(image_path).exists():
        print(f"Error: Image file not found at {image_path}")
        return
    
    with open(image_path, 'rb') as f:
        files = {'file': (Path(image_path).name, f, 'image/jpeg')}
        response = requests.post(
            f"{API_URL}/api/process-document",
            files=files,
            timeout=60
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Processing successful!")
        print(f"\nFilename: {result['filename']}")
        print(f"Word Count: {result['ocr']['word_count']}")
        print(f"Confidence: {result['ocr']['average_confidence']:.2%}")
        print(f"Total Blocks: {result['layout']['total_blocks']}")
        print(f"Has Tables: {result['layout']['has_tables']}")
        print(f"Entities Found: {result['metadata']['total_entities_found']}")
        
        print("\n📝 Extracted Text (first 200 chars):")
        print(result['ocr']['full_text'][:200] + "...")
        
        print("\n🎯 Entities:")
        for entity_type, entities in result['entities'].items():
            if entities:
                print(f"  {entity_type}: {', '.join(entities[:3])}")
    else:
        print(f"❌ Error: {response.text}")
    
    print("-" * 50)

def main():
    """Run all tests"""
    print("=" * 50)
    print("OCR API Test Suite")
    print("=" * 50)
    print()
    
    # Test 1: Health check
    try:
        test_health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("-" * 50)
    
    # Test 2: Root endpoint
    try:
        test_root_endpoint()
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        print("-" * 50)
    
    # Test 3: Document processing
    # Replace with your test image path
    test_image = "test_document.jpg"
    
    print(f"\n⚠️  To test document processing, provide an image path:")
    print(f"   python test_api.py <image_path>")
    print(f"   Or update the 'test_image' variable in this script")
    print()
    
    import sys
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
        try:
            test_process_document(test_image)
        except Exception as e:
            print(f"❌ Document processing failed: {e}")
            print("-" * 50)
    
    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
