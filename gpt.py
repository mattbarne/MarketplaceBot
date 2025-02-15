import openai
import os

# Pulls api key from enviroment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generateItemAssessment(price, description):
    messageContent = f"Price: {price}\nDescription: {description}"

    completion = openai.chat.completions.create(
        model ="gpt-4o-mini",
        messages = [
            {"role": "developer", "content": "You are a buyer trying to lowball for the item given"},
            {"role": "user", "content": messageContent}],
    )

    return completion.choices[0].message