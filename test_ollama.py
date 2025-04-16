from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")
response = llm.invoke("Tell me about Indian Railways.")
print(response)