# Home Assistant PaLM Response Sensor

This is a non-working custom component for Home Assistant intended to allow generation of text responses using Google's PaLM API. PaLM API allows access to the advanced capabilities of Google’s large language models like PaLM 2.

Join [the waitlist](https://developers.generativeai.google/products/palm) for the public preview to get your [API key](https://makersuite.google.com/app/apikey) via MakerSuite.

Development is paused secondary to 2023.7 anticipated implementation of service call responses **conversation.process**.  This service allows you to ask Assist a command or question, and get a response back. "In the morning, you could ask Home Assistant for todays calendar events, add things like weather information, send it to ChatGPT (or PaLM) using the conversation proceess and ask it to summerize it, and send a notification to your phone with the result."

The PaLM Response Sensor project was built parallel to [openai_response](https://github.com/Hassassistant/openai_response) by Hassassistant. Please contribute as able.

## Installation
1. Add the repository to HACS

2. Add the following lines to your Home Assistant **configuration.yaml** file:

```yaml
sensor:
  - platform: palm_response
    api_key: YOUR_PALM_API_KEY
    model: "models/chat-bison-001" # Optional, defaults to "models/chat-bison-001"
    name: "palm_response" # Optional, defaults to "palm_response"
```
Replace YOUR_PALM_API_KEY with your actual MakerSuite PaLM API key.

3. Create an **input_text.palm_input** entity in Home Assistant to serve as the input for the PaLM model. Create this input_text via the device helpers page or add the following lines to your **configuration.yaml** file:

```yaml
input_text:
  palm_input:
    name: PaLM Input
```

4. Restart Home Assistant

## Usage
To generate a response from PaLM, update the **input_text.palm_input** entity with the text you want to send to the model. The generated response will be available as an attribute of the **sensor.palm_response** entity.

## Frontend
Add the following to your **ui-lovelace.yaml** file or create a card in the Lovelace UI:

```yaml
type: grid
square: false
columns: 1
cards:
  - type: entities
    entities:
      - entity: input_text.palm_input
  - type: markdown
    content: '{{ state_attr(''sensor.palm_response'', ''chat_response'') }}'
    title: PaLM Response
```
Now you can type your text in the PaLM Input field, and the generated response will be displayed in the response card.
