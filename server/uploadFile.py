import os
import json
from huggingface_hub import login
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
import cassio

# Hugging Face and Astra DB setup
def setup_huggingface_and_astra():
    # Hugging Face login for model access
    login(token="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")

    # Initialize Astra DB
    ASTRA_DB_APPLICATION_TOKEN = "AstraCS:cUIKsAZQgdsZUzMlAOJsnxbR:808bfd213aa188fd28cdf20bfda17a3ca87795965057c84e2d53b19cf04fce3c"
    ASTRA_DB_ID = "31282abc-868e-4c75-906e-adf466f86267"
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# Get all PDF file paths from a directory
def get_pdf_paths_from_directory(directory_path):
    return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.pdf')]

# Load PDFs into documents
def load_pdfs(pdf_paths):
    docs = []
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            try:
                loader = PyPDFLoader(pdf_path)
                doc = loader.load()
                docs.append(doc)
            except Exception as e:
                print(f"Failed to load {pdf_path}: {e}")
        else:
            print(f"File not found: {pdf_path}")
    return docs

# Extract metadata from PDF content
def extract_metadata_from_pdfs(pdf_paths):
    paper_metadata = {}
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            try:
                # Load the PDF
                loader = PyPDFLoader(pdf_path)
                doc = loader.load()

                # Split the document into chunks
                text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=350, chunk_overlap=50)
                docs_split = text_splitter.split_documents(doc)

                # Initialize a variable to store content before "Abstract"
                first_chunk_content = ""

                # Process the document chunks individually
                for chunk in docs_split:
                    # If "Abstract" is found, stop and capture content before it
                    if "Abstract" in chunk.page_content:
                        first_chunk_content += chunk.page_content.split("Abstract")[0]
                        break
                    else:
                        first_chunk_content += chunk.page_content

                # Now extract title and authors from the first_chunk_content
                lines = first_chunk_content.split("\n")
                title = lines[0] if lines else "Unknown Title"
                authors = ", ".join([line for line in lines[1:4]])  # Assuming authors are in the next few lines

                # Store in the dictionary with the source as the key
                paper_metadata[pdf_path] = {
                    "title": title.strip(),
                    "authors": authors.strip()
                }

            except Exception as e:
                print(f"Failed to load {pdf_path}: {e}")
        else:
            print(f"File not found: {pdf_path}")
    return paper_metadata

# Save the metadata to a JSON file
def save_metadata_to_json(metadata, filename='paper_metadata.json'):
    with open(filename, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    print(f"Dictionary saved to {filename}")

# Initialize Hugging Face embeddings and Cassandra vector store
def initialize_vector_store(docs_split):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Cassandra vector store initialization
    astra_vector_store = Cassandra(embedding=embeddings, session=None, keyspace=None, table_name="Nurtura")

    # Add documents to Astra vector store
    astra_vector_store.add_documents(docs_split)
    print(f"Inserted {len(docs_split)} documents.")

    # Vector store index wrapper
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
    return astra_vector_index

# Main method
def main():
    # Setup Hugging Face and Astra DB
    setup_huggingface_and_astra()

    # Define the directory where PDF files are stored
    pdf_directory = './pathtopaperfolder'  # Change this to your directory path

    # Get all PDF file paths
    pdf_paths = get_pdf_paths_from_directory(pdf_directory)
    print("PDF files found:", pdf_paths)

    # Load PDFs into documents
    docs = load_pdfs(pdf_paths)

    # Flatten the documents list
    doc_list = [item for sublist in docs for item in sublist] if docs else []

    # Split documents into chunks
    if doc_list:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=350, chunk_overlap=50)
        docs_split = text_splitter.split_documents(doc_list)
    else:
        docs_split = []

    # Extract metadata and save to JSON
    paper_metadata = extract_metadata_from_pdfs(pdf_paths)
    save_metadata_to_json(paper_metadata)

    # Initialize vector store and insert documents
    initialize_vector_store(docs_split)

if __name__ == '_main_':
    main()