import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


print("Loaded Key:", key[:10], "..." if key else "❌ Not loaded")
async def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful grocery shopping assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        import traceback
        print("LLM Error:", e)
        traceback.print_exc()
        raise e  # Still raise for Swagger/terminal

