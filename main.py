import time
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

gpt4 = ChatOpenAI(model_name="openai/gpt-4o-2024-08-06", temperature=0.1)

if __name__ == "__main__":
    print("telegram bot started...")
    config = {"configurable": {"thread_id": 42}}
    initial_timestamp = int(time.time())