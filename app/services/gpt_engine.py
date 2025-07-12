import openai
import os
from app.core.settings.dev import settings 
openai.api_key = settings.OPENAI_API_KEY

def ask_chatgpt(system_prompt: str, user_query: str, role: str = None, school_id: str = None) -> str:
    user_query = user_query.strip()

    # Add school + role context
    context_lines = []
    if school_id:
        context_lines.append(f"School ID Context: {school_id}")
        context_lines.append(f"NOTE: Always filter all data by school_id = '{school_id}'.")

    if role:
        context_lines.append(f"User Role Context: {role}")
        context_lines.append("NOTE: Always respect this user's role when answering. Do not show unauthorized data.")

    context_lines.append("\nQuery:")
    context_lines.append(user_query)
    user_query = "\n".join(context_lines)

    # Call OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=500,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )

    return response['choices'][0]['message']['content']
