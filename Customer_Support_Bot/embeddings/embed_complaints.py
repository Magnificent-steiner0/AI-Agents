import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from sentence_transformers import SentenceTransformer
from Customer_Support_Bot.utils.db_utils import get_connection


model=SentenceTransformer('all-mpnet-base-v2')

def embed_complaints():
    conn=get_connection()
    if not conn:
        return
    
    try:
        cur=conn.cursor()
        
        cur.execute("select id, situation from complaints where embedding is NULL;")
        rows=cur.fetchall()
        
        if not rows:
            print("All rows are embedded")
            return
        
        for row in rows:
            complain_id, situation=row
            emnbedding=model.encode(situation).tolist()
            cur.execute("update complaints set embedding=%s where id=%s", (emnbedding, complain_id))
            print(f"Embedded and updated complaint ID: {complain_id}")
            
        conn.commit()
        cur.close()
        print("All embedding successful")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        
if __name__=="__main__":
    embed_complaints()