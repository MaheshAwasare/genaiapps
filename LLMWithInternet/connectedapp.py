from llm_axe import OllamaChat, PdfReader, OnlineAgent

llm = OllamaChat(model="llama3")
print(llm)
online_agent = OnlineAgent(llm)
prompt = "Find out what is latest IPL matches results"
print(prompt)
response = online_agent.search(prompt)

print(response)