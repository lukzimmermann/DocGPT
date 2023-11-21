from dotenv import load_dotenv
from src.utils.openAI import Embedding, createEmbedding, chat

from src.utils.postgres import PostgresDB


load_dotenv()

class Document:
    def __init__(self) -> None:
        self.id = 0
        self.name = ''
        self.page = 0
        self.tags = []
        self.dotProduct = 0
        self.text = 0

class DocumentJson:
    def __init__(self, document: Document) -> None:
        self.title = document.name
        self.tags = document.tags[0]
        self.page = document.page
        self.rating = document.dotProduct
        #self.text = document.text

        #rating = (4.0 - document.dotProduct * 4.0) * 2
        #if rating > 4: rating = 4
        #self.rating = rating
            

class ChatModel:
    def __init__(self, role: str, content: str, documents: list[DocumentJson]) -> None:
        self.role = role
        self.content = content
        self.documents: list[DocumentJson] = documents

def get_tags_by_id(id):
    tags = []
    pg = PostgresDB()
    pg.connect()
    data = (id,)
    response = pg.selectQuery(f"""
                    SELECT tag
                    FROM tag
                    WHERE doc_id = %s""",
                    data)
    pg.disconnect()

    for item in response:
        tags.append(item[0])
    return tags

def get_documents(text: str):

    vector = get_embedding(text).vector.tolist() 

    pg = PostgresDB()
    pg.connect()

    data = (vector,vector)

    response = pg.selectQuery(f"""
                    SELECT doc_id, filename, doc_segment, embedding_ada002 <-> %s::vector AS distance, doc_text
                    FROM embedding
                    JOIN document ON id = doc_id
                    ORDER BY embedding_ada002 <-> %s::vector
                    LIMIT 3;""",
                    data)
    pg.disconnect()

    documents = []
    for item in response:
        document = Document()
        document.id = item[0]
        document.name = item[1]
        document.page = item[2]
        document.dotProduct = item[3]
        document.text = item[4]
        document.tags = get_tags_by_id(document.id)
        documents.append(document)
    
    return documents

def get_embedding(text: str) -> Embedding:
    return createEmbedding(text)

def get_answer(question: str):
    documentsJson: list[DocumentJson] = []
    documents = get_documents(question)

    context = ""
    sourceCounter = 1
    context += """Das sind verschiedene Quellen auf die dich referenzieren sollst. 
    Falls du diese Quellen verwendest, vermerke das am Schluss des Satzes wie folgt:(Quelle: {DOCUMENT}, Seite {PAGE})\n\n"""
    for doc in documents:
        context += f"NUMBER: {sourceCounter}\nDOCUMENT: {doc.name}\nPAGE: {doc.page+1}\nTAGS: {doc.tags}\nTEXT: {doc.text}\n\n\n"
        documentsJson.append(DocumentJson(doc))
        sourceCounter += 1

    prompt = f"""
    Context: {context}
    UserPrompt: {question}
    """
    answer = chat(prompt)
    chat_result = ChatModel('bot', answer,documentsJson)

    return chat_result
