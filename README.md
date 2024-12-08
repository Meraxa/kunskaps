# Kunskaps

> Kunskaps is the Scandinavian word for knowledge, skills or expertise.

Kunskaps is planned to enable you to store meeting notes, documents, and other information in a structured way.
Is transcribes audio recordings to text and stores them in a database.
In the long run, it should also enable you to automatically generate minutes of meetings and other documents and use search engines to find information in the stored data.

Possible additions might be clustering of the data and web searches to find related information automatically.

## Installation and Development

To run the application, either install [`uv`](https://docs.astral.sh/uv/) directly on your system or create a virtual environment and install it there.
The required dependencies can be install using the command `uv sync`.

To run the fastapi application use the command `uv run --env-file .env fastapi dev`.

The `.env` file should contain the following environment variables:

~~~bash
MONGODB_DATASET_USERNAME="root"
MONGODB_DATASET_PASSWORD="example"
MONGODB_USERDATA_USERNAME="root"
MONGODB_USERDATA_PASSWORD="example"
MONGODB_DATASET_URL="mongodb://root:example@localhost:27017/"
MONGODB_USERDATA_URL="mongodb://root:example@localhost:27018/"
~~~

> The credentials for the `mongodb express` web ui are `admin:pass`.
