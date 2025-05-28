import sys
import os
import numpy as np
import psycopg2
import ollama
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from sentence_transformers import SentenceTransformer
from Customer_Support_Bot.utils.db_utils import get_connection


model=SentenceTransformer('all-mpnet-base-v2')

def similar_complaints(query_embedding, top_k=3, threshold=0.75):
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute(
        """
        SELECT situation, solution, 1 - (embedding <=> %s::vector) AS similarity
        FROM complaints
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (query_embedding, query_embedding, top_k)
    )
    results=cursor.fetchall()
    conn.close()
    return [(r[0], r[1]) for r in results if r[2] >= threshold]


def build_prompt(query, context_results):
    examples = "\n".join([
        f"- Complaint: {r[0]}\n  Solution: {r[1]}" for r in context_results
    ])

    return (
        f"You are a helpful and strict customer support agent.\n"
        f"You must only answer based on the following past complaints and their solutions.\n"
        f"If there is no relevant solution, simply respond with:\n"
        f'  "Sorry, I couldn\'t find a solution for that."\n\n'
        f"DO NOT guess or invent a response.\n\n"
        f"User Issue: {query}\n\n"
        f"Relevant Past Complaints and Solutions:\n{examples}\n\n"
        f"Based ONLY on the above, provide a concise solution to the user's issue:"
    )



def ask_bot(query):
    query_embedding = model.encode(query).tolist()
    similar_complaints_embeddings = similar_complaints(query_embedding)
    
    if not similar_complaints_embeddings:
        return "sorry, I couldn't find a solution for that"
    
    prompt=build_prompt(query, similar_complaints_embeddings)
    
    if not prompt:
        return "Sorry, I couldn't find a solution for that."
    
    response = ollama.chat(
        model="phi",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful **customer support chatbot**. "
                    "You help users with complaints about specific tech products"
                    "You **must not** respond with analysis, assumptions, logical puzzles, or general AI reasoning. "
                    "Always stay in the role of a support agent. Keep answers short, clear, and specific to the complaint."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response['message']['content']


if __name__=="__main__":
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit","quit","stop","end"]:
            break
        answer=ask_bot(user_query)
        print(f"Bot: {answer}")