from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv
import os

# Check if .env file exists
if os.path.exists('.env'):
    load_dotenv() 
    
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_ACCESS_TOKEN")

def load_schema(file_path):
    with open(file_path, 'r') as file:
        db_schema = file.read()
    return db_schema

def get_schema(_):
    db_shema = load_schema("./data/db_schema.txt")
    return db_shema

def sql_response_from_prompt_template(llm):
    sql_prompt = """

    You are an agent designed return correct usable SQL queries.
    Given an input question, create a syntactically correct SQLite query only.
    You DONOT have access for interacting with the database, so ALWAYS REMEMBER to return just the SQL queries.
    You MUST double check your query to ensure it is correct. If you get an error while executing a query, rewrite the query and try again.

    If the question does not seem related to the table schema in the database, just return "I don't know" as the answer.

    Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}

    Question: {input}
    SQL Query:"""

    sql_prompt_template=PromptTemplate.from_template(
        sql_prompt
    )

    full_sql_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=sql_prompt_template),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | full_sql_prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
        )
    
    return sql_response

def main():
    question = """Can you share the total expenses for a given account_id in a given date range. The output
    should include account name and total expense"""

    llm = ChatOpenAI()

    sql_response = sql_response_from_prompt_template(llm)
    print(
        sql_response.invoke(
        {
            "input": question,
            "agent_scratchpad": []}
        )
    )
    
if __name__ == "__main__":
    main()