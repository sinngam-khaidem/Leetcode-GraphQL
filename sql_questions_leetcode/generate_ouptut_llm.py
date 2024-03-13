from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
_ = load_dotenv()

chat_llm = ChatOpenAI(temperature=0.0, openai_api_key = os.getenv("OPENAI_API_KEY"))

sql_solution_schema = ResponseSchema(name="sql_solution",
                                     description="This is the SQL solution of the problem")

response_schemas = [sql_solution_schema]


output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template_string = """You are an SQL expert. You come up with easy to understand solutions to the provided SQL problems.

Take the html snippet of the problem description below (delimited by triple backticks), and the JSON representation of the input test case (delimited by <inp></inp>) and use it to come up with the SQL solution to the problem.

problem description: ```{problem_description}```

input test case: <inp>{input_testcase}</inp>

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template=template_string)

def generate_output(problem_description, input_testcase):
    messages = prompt.format_messages(problem_description=problem_description, input_testcase=input_testcase, format_instructions=format_instructions)
    response = chat_llm(messages)
    return output_parser.parse(response.content)