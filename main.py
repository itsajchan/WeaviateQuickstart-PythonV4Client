import weaviate
import weaviate.classes as wvc
from weaviate.embedded import EmbeddedOptions
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


client = weaviate.connect_to_embedded(
    # embedded_options=EmbeddedOptions(
    #     additional_env_vars={
    #     "ENABLE_MODULES":
    #     "backup-s3,text2vec-openai,text2vec-cohere,text2vec-huggingface,ref2vec-centroid,generative-openai,qna-openai"}
    # ), 
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
    }
)


questions = client.collections.create(
    name="Question",
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    generative_config=wvc.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
)

resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
data = json.loads(resp.text)  # Load data

question_objs = list()
for i, d in enumerate(data):
    question_objs.append({
        "answer": d["Answer"],
        "question": d["Question"],
        "category": d["Category"],
    })

questions = client.collections.get("Question")
questions.data.insert_many(question_objs)  # This uses batching under the hood



questions = client.collections.get("Question")

response = questions.query.near_text(
    query="biology",
    limit=2
)

print(response.objects[0].properties)  # Inspect the first object


