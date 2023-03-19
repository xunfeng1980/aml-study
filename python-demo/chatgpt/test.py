import openai
import os

openai.api_key = 'xx'


def generate_response(prompt):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.1,
    )
    message = completion.choices[0].text
    return message


if __name__ == '__main__':
    print(generate_response("Q: 1+1="))
