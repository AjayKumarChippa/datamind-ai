from google import genai
from google.genai import types

from config import load_config


# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

config = load_config()

api_key = config.get("GOOGLE_API_KEY")
model = config.get("GOOGLE_MODEL")

client = genai.Client(api_key=api_key)


# ----------------------------------------------------
# Our Tool
# ----------------------------------------------------

def get_leave_balance(employee_name: str) -> int:

    leave_balances = {
        "Ajay": 18,
        "Ravi": 12,
        "Priya": 20,
    }

    return leave_balances.get(
        employee_name,
        0
    )


# ----------------------------------------------------
# Tool Declaration
# ----------------------------------------------------

tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_leave_balance",
            description="Get the remaining annual leave balance for an employee.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "employee_name": types.Schema(
                        type="STRING",
                        description="Name of the employee"
                    )
                },
                required=["employee_name"],
            ),
        )
    ]
)


# ----------------------------------------------------
# Model Configuration
# ----------------------------------------------------

generation_config = types.GenerateContentConfig(
    tools=[tool]
)


# ----------------------------------------------------
# User Question
# ----------------------------------------------------

question = "How many leave days does Ajay have remaining?"


response = client.models.generate_content(
    model=model,
    contents=question,
    config=generation_config,
)

# ----------------------------------------------------
# Handle Tool Call
# ---------------------------------------------------

function_call = (
    response
    .candidates[0]
    .content
    .parts[0]
    .function_call
)

if function_call:

    print("Tool requested:", function_call.name)
    print("Arguments:", function_call.args)

    if function_call.name == "get_leave_balance":

        employee_name = function_call.args["employee_name"]

        # Execute our Python function
        result = get_leave_balance(employee_name)

        print("Tool result:", result)

        # ------------------------------------------------
        # Send Tool Result Back To Gemini
        # ------------------------------------------------

        tool_response = types.Part.from_function_response(
            name=function_call.name,
            response={
                "result": result
            },
        )

        final_response = client.models.generate_content(
            model=model,
            contents=[
                question,
                response.candidates[0].content,
                tool_response,
            ],
            config=generation_config,
        )

        print("\nFinal Answer:")
        print(final_response.text)