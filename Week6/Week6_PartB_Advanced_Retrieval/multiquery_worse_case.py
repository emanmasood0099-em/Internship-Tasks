import logging

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers.multi_query import MultiQueryRetriever

load_dotenv()

print("=" * 70)
print("PART B - MULTIQUERY WORSE-CASE CHALLENGE")
print("=" * 70)

documents = [
    "Python is widely used for web development, automation, and artificial intelligence.",
    "JavaScript is widely used for interactive web pages and browser applications.",
    "Java is used for enterprise software and Android application development.",
    "Basketball requires dribbling, passing, shooting, and rebounding.",
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.create_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="week6_partb_worse_case_v3",
)

base_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 1}
)

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
)

logging.basicConfig(level=logging.INFO)

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=model,
)

question = "Which language is useful for programming?"

print("\nQUESTION:")
print(question)

print("\n--- PLAIN RETRIEVER ---")

plain_results = base_retriever.invoke(question)

for i, doc in enumerate(plain_results, 1):
    print(f"Result {i}:")
    print(doc.page_content)

print("\n--- MULTIQUERY RETRIEVER ---")

multi_results = multi_retriever.invoke(question)

for i, doc in enumerate(multi_results, 1):
    print(f"Result {i}:")
    print(doc.page_content)

print("\n--- TRADE-OFF ANALYSIS ---")
print("Plain retrieval performs one similarity search.")
print("MultiQueryRetriever generates multiple alternative queries.")
print("The additional queries can improve recall.")
print("However, broader alternative queries can also retrieve documents")
print("that are less relevant to the original question.")
print("Therefore, MultiQueryRetriever trades extra LLM calls and possible")
print("noise for potentially better retrieval coverage.")

print("\nMultiQuery worse-case challenge completed.")