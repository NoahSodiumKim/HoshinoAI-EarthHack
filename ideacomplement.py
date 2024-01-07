from flask import Flask, request, jsonify
import openai
import os

# Given as input 
ideaid = 1
# Retrieved from database
ideas = ["Uber", "...","..."]
resources = ["water", "metal", "gas", "paper"]
values = [[1, 0, 2, 1], [2, 2, 0, 1], [0, 1, 1, 2]]


# Find idea with most complements
idea = values[ideaid]
max_index = ideaid
length = len(values[0])
max_count = 0

for index, ideavals in enumerate(values):
    count = 0
    for i in range(length):
        if (idea[i] == 2 and ideavals[i] == 0) or (idea[i] == 0 and ideavals[i] == 2):
            count += 1
    if count > max_count:
        max_count = count
        max_index = index


# Get that idea
given_idea = ideas[ideaid]
compatible_idea = ideas[max_index]

#prompt? copied format from values.py, see if it works
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/generate_values')
def generate_values():
    message = request.args.get("message")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Explain how the following two solutions to sustainability problems complement each other: Solution 1: "{given_idea}", Solution 2: "{compatible_idea}". For example, one solution could use up the excess materials created in the other solution."
            },
            {
                "role": "user",
                "content": message
            },
        ],
        temperature=0.7,
        max_tokens=128
    )

    return str(response.choices[0].message.content)



