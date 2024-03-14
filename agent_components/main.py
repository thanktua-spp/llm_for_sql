from sql_query_tool import sql_query_generator_tool

def main():
    question = """Can you share the total expenses for a given account_id in a given date range. The output
    should include account name and total expense"""

    print(sql_query_generator_tool.run(question))
    
if __name__ == "__main__":
    pass
