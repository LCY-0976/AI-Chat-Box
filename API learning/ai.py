import json
from openai import OpenAI

def ai_response(message, role):
    client = OpenAI(
        api_key="", #add your api key here
        base_url="https://api.deepseek.com",
    )

    system_prompt = role
    user_prompt = message

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )
        
        # Return JSON object for API data transfer
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        # Return error info as JSON format
        return {"error": f"AI Error: {str(e)}"}



