from llama_cpp import Llama

LLM = Llama(model_path="models/llama-2-7b-chat.Q3_K_L.gguf")
while True:
    prompt = input("> ")
    output = LLM(prompt)
    print(output["choices"][0]["text"])
