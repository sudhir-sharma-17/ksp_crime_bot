import os
import httpx
import asyncio

async def test():
    api_key = os.getenv("GROQ_API_KEY", "your-api-key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ],
        "temperature": 0.0
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=data,
            headers=headers
        )
        print("Status Code:", response.status_code)
        print("Response:", response.text)

asyncio.run(test())
