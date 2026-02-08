
import requests
import wave
import struct
import os
import time

def create_dummy_wav(filename):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        for i in range(16000): # 1 second of silence
            data = struct.pack('<h', 0)
            f.writeframesraw(data)

def test_asr():
    filename = "test_audio.wav"
    create_dummy_wav(filename)
    
    url = "http://127.0.0.1:8001/asr"
    print(f"Sending request to {url}...")
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            start = time.time()
            response = requests.post(url, files=files)
            end = time.time()
            
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Time: {end - start:.2f}s")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_asr()
