import os
import streamlit as st
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

# LLM
llm = ChatOpenAI(temperature=0.1, max_tokens= 500)

#TITLES
st.title("News Article Analyser")
st.sidebar.title("News Article URLs")

url = st.sidebar.text_input(f"URL")

#RAG part of the project
process_url_clicked = st.sidebar.button("Process Articles")
main_placeholder = st.empty()
if process_url_clicked:
    # load data
    loader = UnstructuredURLLoader(urls=[url])
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    

    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)
   
    # create embeddings and save it to FAISS index
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # # Save the vectorstore object locally
    vectorstore_openai.save_local("vectorindex_openai")
    main_placeholder.text("Embedding Vector Saved...✅✅✅")

    from pathlib import Path
    vectorstore_path = Path(r"C:\Users\Ivana\Desktop\CODEProjects\LLM.ArticleAnalyser\vectorindex_openai")
    

    main_placeholder.text("Embedding Vector Loading...✅✅✅")
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    #vectorstore = FAISS.load_local("vectorstore_openai", embeddings, allow_dangerous_deserialization=True)
    time.sleep(2)


query = main_placeholder.text_input("Questions about Article: ")
if query:
    
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())

    result = chain.invoke({"question": query}, return_only_outputs=True)

    st.subheader("Answer")
    st.write(result["answer"])

    # Display sources, if available
    sources = result.get("sources", "")
    if sources:
        st.subheader("Sources:")
        sources_list = sources.split("\n")  # Split the sources by newline
        for source in sources_list:
            st.write(source)