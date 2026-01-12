# sql_generator.py
import openai
from backend import config

def generate_sql(schema, user_input, chat_history):
    """Generate SQL query using retrieved schema + user input."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert SQL developer specialized in the QNXT schema. "
                "Your task is to generate accurate and optimized SQL queries based on user requests. "
                "Assume the SQL Server version is older than 2022, so do not use syntax that requires SQL Server 2022 or newer. "
                "For example, do not use DISTINCT inside STRING_AGG. Instead, use subqueries or other compatible workarounds. "
                "Return only the SQL query as plain text. "
                "Do not include any explanations, comments, markdown formatting, or wrap the query in quotes or code blocks."
                "Consider ruleid column in claimedit table as edit"
                "Unless or otherwise user not specified anything consider claim as the primary table for claim related sql queries"
            )
        }
    ] + chat_history + [
        {
            "role": "user",
            "content": f"""
Relevant QNXT Schema:
{schema}
User Request: "{user_input}"
Generate the correct and optimized SQL query for the above request.
Only return the SQL query. Do not include any explanation, formatting, or wrap it in quotes or code blocks.
"""
        }
    ]
    try:
        response = openai.ChatCompletion.create(
            engine=config.DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=300,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
 