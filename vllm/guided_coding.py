import json

import jsonschema
import openai

client = openai.OpenAI(
        base_url="http://gpu:8000/v1",
        api_key="token-abc123",
    )

MODEL_NAME = '/model/Qwen-14B-Chat-Int4'
TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "age": {
            "type": "integer"
        },
        "skills": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 10
            },
            "minItems": 3
        },
        "work history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string"
                    },
                    "duration": {
                        "type": "string"
                    },
                    "position": {
                        "type": "string"
                    }
                },
                "required": ["company", "position"]
            }
        }
    },
    "required": ["name", "age", "skills", "work history"]
}
completion =  client.completions.create(
    model=MODEL_NAME,
    prompt=f"Give an example JSON for an employee profile "
           f"that fits this schema: {TEST_SCHEMA}",
    n=3,
    temperature=1.0,
    max_tokens=500,
    extra_body=dict(guided_json=TEST_SCHEMA))

assert completion.id is not None
assert completion.choices is not None and len(completion.choices) == 3
for i in range(3):
    assert completion.choices[i].text is not None
    print(completion.choices[i].text)
    output_json = json.loads(completion.choices[i].text)
    jsonschema.validate(instance=output_json, schema=TEST_SCHEMA)