#!/usr/bin/env python3
"""
Test script to isolate Deepgram API issues
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from deepgram import DeepgramClient, PrerecordedOptions
    print("✅ Deepgram imports successful")
except Exception as e:
    print(f"❌ Deepgram import failed: {e}")
    sys.exit(1)

def test_deepgram_with_file(file_path: str):
    """Test Deepgram transcription with a file"""
    api_key = os.getenv('DEEPGRAM_API_KEY')
    if not api_key:
        print("❌ DEEPGRAM_API_KEY not set")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    try:
        # Initialize client
        dg = DeepgramClient(api_key)
        print("✅ DeepgramClient initialized")
        
        # Configure options
        options = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
            channels=1
        )
        print("✅ PrerecordedOptions configured")
        
        # Test different approaches
        print(f"📁 Testing file: {file_path}")
        
        # Approach 1: File handle
        print("🧪 Testing approach 1: File handle")
        try:
            with open(file_path, "rb") as f:
                response = dg.listen.rest.v("1").transcribe_file(source=f, options=options)
                print(f"✅ Approach 1 success: {response}")
                return True
        except Exception as e:
            print(f"❌ Approach 1 failed: {e}")
        
        # Approach 2: File content
        print("🧪 Testing approach 2: File content")
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            response = dg.listen.rest.v("1").transcribe_file(source=content, options=options)
            print(f"✅ Approach 2 success: {response}")
            return True
        except Exception as e:
            print(f"❌ Approach 2 failed: {e}")
        
        # Approach 3: Different method name
        print("🧪 Testing approach 3: transcribe_prerecorded")
        try:
            with open(file_path, "rb") as f:
                response = dg.listen.rest.v("1").transcribe_prerecorded(source=f, options=options)
                print(f"✅ Approach 3 success: {response}")
                return True
        except Exception as e:
            print(f"❌ Approach 3 failed: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    # Create a test file if none exists
    test_file = "/tmp/test_audio.ogg"
    if not os.path.exists(test_file):
        print(f"⚠️  Test file {test_file} not found")
        print("Please create a small audio file or use an existing one")
        sys.exit(1)
    
    success = test_deepgram_with_file(test_file)
    if success:
        print("🎉 Deepgram test successful!")
    else:
        print("💥 All Deepgram approaches failed")
