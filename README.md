# llm_for_sql

## Dependencies:
- I used poetry to manage dependencies.
Download poetry with curl: curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1

- Activate poetry shell and install dependencies from pyproject.toml file.

- Run app server with uvicorn fastapi: uvicorn app_server.app:app --port 8001 --reload

## Remark:
- use my pinecone api key to enable app connection with RAG document storage here: 997a4e62-01df-4260-9b10-94346a24f48c

- This is a prof of concept research mechanism to enable me demostrate RAG document + SQL query Engine, it is not production ready yet.

## Challenges:
- Using the SQL schema alone can not guarantee full sql_agent capabilities, I tried to create a dummy database based on the SQL schema with few entries but SQL engine had problems reading and running the records.
