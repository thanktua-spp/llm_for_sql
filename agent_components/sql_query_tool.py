from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI
from agent_components.sql_query_engine import sql_response_from_prompt_template


def get_query(question, llm):
    sql_response = sql_response_from_prompt_template(llm=llm)
    return sql_response.invoke(
    {
        "input": question,
        "agent_scratchpad": []}
    )

def gen_sql_query_tool(query: str):
    llm = ChatOpenAI()
    return get_query(question=query, llm=llm)

sql_query_generator_tool = StructuredTool.from_function(
    func=gen_sql_query_tool,
    name="Search",
    description="this tool must be used for queries related to performing sql queries on a database",
)

def main():
    question = """Can you share the total expenses for a given account_id in a given date range. The output
    should include account name and total expense"""

    print(sql_query_generator_tool.run(question))
    
if __name__ == "__main__":
    main()
    
