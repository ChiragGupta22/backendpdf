# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from src.utils.constant.embedding_utils import get_embedding_model
# from langchain_community.vectorstores import Chroma
# from dotenv import load_dotenv
# import os

# load_dotenv()





# def create_vector_db(pdf_path, user_id):

#     embedding_model = get_embedding_model()

#     loader = PyPDFLoader(pdf_path)
#     docs = loader.load()

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=100
#     )

#     chunks = splitter.split_documents(docs)

#     persist_directory = f"chromafiledbs/{user_id}"
#     os.makedirs(persist_directory, exist_ok=True)

#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embedding_model,
#         persist_directory=persist_directory
#     )

#     return vectorstore