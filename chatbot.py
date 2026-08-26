import ollama

history=[]

while True :
    input_text = input("You : ")

    if input_text.lower() == "quit" :
        print("Thank you for using the chat. Goodbye!")
        break

    history.append({'role' : 'user' , 'content' : input_text})

    output_text = ollama.chat(model="qwen2.5-coder:7b" , messages=history)

    reply=output_text['message']['content']

    history.append({'role' : 'assistant' , 'content' : reply})

    print("AI : " + reply)