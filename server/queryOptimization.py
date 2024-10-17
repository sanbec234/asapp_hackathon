import json
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

# Function to load and concatenate JSON data
def load_json_data_to_string(json_file_path):
    with open(json_file_path, 'r') as file:
        auth_data = json.load(file)
    
    # Use list comprehension and join for efficient string building
    json_string = ' '.join([f"{key}: {value}" for key, value in auth_data.items()])
    
    return json_string.strip()


with open(json_file_path, 'r') as file:
        look_ups = json.load(file)
# Load JSON data and prepare concatenated string

print(type(look_ups))
json_file_path = 'paper_metadata.json'

json_string = load_json_data_to_string(json_file_path)

# Setup retriever for Astra DB
retriever = astra_vector_index.vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.55, 'k': 10}
)

# User query
question = "How does Mistral 7B compare to Llama?"

# Retrieve relevant documents
retrieved_docs = retriever.invoke(question)

# Format retrieved content
rag_content = ' '.join([f"Content: {doc.page_content} Source: {doc.metadata['source']}" for doc in retrieved_docs])
# Extract unique strings starting with "/content" from retrieved_docs
content_sources_set = set()

# Iterate over the retrieved documents
for doc in retrieved_docs:
    source = doc.metadata.get('source')
    if source and source.startswith('/content'):
        content_sources_set.add(source)  # Add to the set for uniqueness

# Print the unique results
print("Unique content sources:")
for content in content_sources_set:
    print(content)








author_title_string = ""

# Iterate over the unique content sources and look up the author and title in the dictionary
for content in content_sources_set:
    if content in look_ups:
        title = look_ups[content].get('title', 'Unknown Title')
        authors = look_ups[content].get('authors', 'Unknown Authors')
        # Append to the result string
        author_title_string += f"Source: {content}, Title: {title}, Authors: {authors}\n"

# The final string containing all the title and author info
# print(author_title_string)





print(json_string.count)

# LLM setup and response generation
api_key = "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"
llm = ChatGroq(groq_api_key=api_key, model_name="Llama-3.1-70b-Versatile")

# Define the system prompt with the combined input
system_prompt = f"""
You are an expert in answering questions based on provided documents.
Here is the user's question: {question}.
Use the following relevant content: {rag_content} to provide a precise and well-structured response.
Your response should:
1. Extract only the most relevant information from the content.
2. Cite the author and title of the papers using this reference data (use this only to identify author names and paper titles, not for content comparison): {json_string}.
3. Start the response by mentioning the source and title of the paper, followed by a clear explanation of the relevant content.
Ensure your response is concise, accurate, and thoroughly answers the question based on the provided documents.
"""


# Create a list of messages for the model
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=question)
]

# Generate the response using the LLM
generated_response = llm.invoke(messages)

# Output the final response
print("Generated Response:\n", generated_response)