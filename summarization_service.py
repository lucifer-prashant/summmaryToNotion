import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

def summarize_text_openrouter(text, model="meta-llama/llama-4-maverick:free", api_key=openrouter_api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  
    }

    prompt = f"""Please summarize the following text:

    {text}

    Summary in bullet points:"""
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3  
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)  
        )
        
        if response.status_code == 200:
            result = response.json()  
            print("Response received successfully.")
            
            formatted_summary = result['choices'][0]['message']['content']
            return formatted_summary
        else:
            print(f"Error: Received response with status code {response.status_code}")
            print(f"Response body: {response.text}")
            return None
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        return None

if __name__ == '__main__':
    sample_text = """The Industrial Revolution was a period of major industrialization 
    that occurred during the late 1700s and early 1800s. This period saw the mechanization 
    of agriculture and textile manufacturing and a revolution in power, including steam 
    ships and railroads, that affected social, cultural and economic conditions."""
    
    summary = summarize_text_openrouter(sample_text)
    if summary:
        print("Generated Summary:")
        print(summary)
    else:
        print("Failed to generate summary.")
