import chainlit as cl
import requests


@cl.on_chat_start
async def start():
    files = None

    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a pdf file to begin!", accept={"text/plain":[".pdf"]}
        ).send()
    global text_file
    text_file = files[0]
    actions = [
        cl.Action(name="Summarize_the_document", value="summarize", description="summarize!")
    ]

    await cl.Message(
        content=f"`{text_file.name}` uploaded", actions=actions
    ).send()


@cl.on_message
async def main(message: cl.Message):
    url = "http://localhost:8000/query" 
    headers = {'Content-Type': 'application/json'}
    payload = {
        "file_name": f"{text_file.name}",  
    }
    query = f"{message.content}" + "keep your answer confined to the domain of the content provided to you"
    response = requests.post(url, json=payload, params={'query': query}, headers=headers)
    if response.status_code == 200:
        answer = response.json()
        output = answer["message"].split('(')[0]
        await cl.Message(
        content=f"{output}").send()
        #print("Success:", response.json())
    else:
        await cl.Message(
        content=f"Error:").send()
        print("Error:", response.status_code, response.json())


@cl.action_callback("Summarize_the_document")
async def on_action(action: cl.Action):
    url = "http://localhost:8000/summarize"  
    headers = {'Content-Type': 'application/json'}
    payload = {
        "file_name": f"{text_file.name}",  
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        answer = response.json()
        await cl.Message(
        content=f"The summary is {answer["message"]}").send()
    else:
        await cl.Message(
        content=f"Error:").send()
        print("Error:", response.status_code, response.json())
    