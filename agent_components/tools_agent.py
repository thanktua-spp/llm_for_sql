from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from agent_components.document_rag_tool import document_retriever_tool
from agent_components.sql_query_tool import sql_query_generator_tool
from langchain.agents import create_openai_functions_agent
from langchain import hub

class Agent:
    def __init__(self):
        self.llm = ChatOpenAI()
        self.AGENT_PROMPT = hub.pull("hwchase17/openai-functions-agent")
        self.TOOLS = [sql_query_generator_tool, document_retriever_tool]
        self.agent = create_openai_functions_agent(self.llm, self.TOOLS, self.AGENT_PROMPT)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.TOOLS, verbose=True)

    def execute_sql_document_agent(self, query):
        return self.agent_executor.invoke({"input": query})['output']


def main():
    question = """
    write query to fetch all transactions from the database.
    """
    agent = Agent()
    agent.execute_sql_document_agent(question)
    
if __name__ == "__main__":
    main()
