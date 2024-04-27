from groq import Groq
from voice import voice
import requests

client = Groq(
        api_key="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",
    )

key = '3c42ae12-da77-4165-8ff7-29a3227bd666'
ID = 'F2:7B:CC:35:34:37:68:14'
sku = 'H6056'
with open('reference/govee.txt', 'r') as file:
        data = file.read()
func = """

import requests

def turn_off_light():
    url = "https://openapi.api.govee.com/router/api/v1/device/control"
  
    headers = {
    'Content-Type': 'application/json',
    'Govee-API-Key': '3c42ae12-da77-4165-8ff7-29a3227bd666'
    }

    payload = {
    "requestId": "uuid",
    "payload": {
        "sku": "H6056",
        "device": "F2:7B:CC:35:34:37:68:14",
        "capability": {
        "type": "devices.capabilities.on_off",
        "instance": "powerSwitch",
        "value": 0
      }
    }
  }
    
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()['status'])

turn_off_light()

"""

def light_function(command):

    process = "Sure thing, one moment please"
    voice(process, False)

    reference = f"""
    Generate Python code according to the following instructions and the Govee API reference {data}:

    1. Use the Govee API key {key}, device ID {ID}, and device SKU {sku} in the request.
    2. The Python code should perform the action specified by the command {command}.
    3. The function should be named 'govee_function'.
    4. The function should return the response from the API request.
    5. After defining the function, call it and print the result.

    THIS IS REALLY IMPORTANT TO PLEASE FOLLOW INSTRUCTIONS - Note: The output should ONLY contain valid Python code. Do NOT include any explanations, descriptions, strings, or non-executable content.
    inlude the delimeters ''' around the code block. Remember, anythign except for the delimeters and the code should not be generated.

    an example of something you should not include is as the following:

    <<<

    Here is the Python code that meets the requirements:

    >>>

    If you need help or an example, here is an example of a working function that turns off the lights {func}
    """

    chat_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": reference
                }
            ],
            model="Llama3-70b-8192",
            temperature=0,
            max_tokens=1000
        )

    response = chat_response.choices[0].message.content
    govee_function = response.replace("'''", "")
    
    print(govee_function)

    delta = f"""

    convert the code {govee_function} into a verb command as if you are executing it
    for example, if the code contains the code for turning off the lights, your output should be "turning off the lights"
    if you need any help determining what the function was, reference the {data} from Govee

    remember, only return what the verb command is, nothing else.

    if given an RGB value in the function, calculate what color that is and thne use that color in the phrase that u will be responding with
    for example, if given the rgb code 0x0000ff, calculate the color code, which in this case is blue, and respond with:
    "Lights changing to blue"

    only respond with the phrase/verb, anything else such as describing the phrase should not be included.
    """

    feedback = client.chat.completions.create(
          messages=[
                {
                      "role": "user",
                      "content": delta
                }
          ],
          model="Llama3-70b-8192",
          temperature=0
    )
    sent = feedback.choices[0].message.content
    voice(sent, False)
    
    exec(govee_function)

    return sent

# light_function("Change the light color to white")
