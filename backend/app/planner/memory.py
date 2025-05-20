from langchain.memory import ConversationBufferMemory

def get_memory():
    """
    Initialize and return a conversation buffer memory for agents.
    """
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)
