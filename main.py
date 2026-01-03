import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the API key from the .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 2. Initialize the DeepSeek Client
client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com"
)

def run_chatbot():
    print("!S!P!E!E!D!Y! DeepSeek Chatbot Active! (Type 'exit' to stop)")
    
    # This list keeps track of the context so the AI remembers your name/topic
    messages = [
        {"role": "system", "content": "You are a helpful programming assistant. Keep answers concise."}
    ]

    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        print("DeepSeek: ", end="", flush=True)
        
        try:
            # 3. Requesting a streaming response
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True
            )

            full_reply = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_reply += content
            
            print() # Print a newline at the end

            # Add the assistant's reply to history
            messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            print(f"\n Error: {e}")

if __name__ == "__main__":
    if not api_key:
        print("Error: No API key found. Check your .env file!")
    else:
        run_chatbot()
