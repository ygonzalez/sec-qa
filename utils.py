import streamlit as st
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate

openai.api_key = st.secrets["OPENAI_API_KEY"]


@st.cache_resource
def load_chain():
    """
    The `load_chain()` function initializes and configures a conversational retrieval chain for
    answering user questions.
    :return: The `load_chain()` function returns a ConversationalRetrievalChain object.
    """

    # Load OpenAI embedding model
    embeddings = OpenAIEmbeddings()

    # Load OpenAI chat model
    llm = ChatOpenAI(temperature=0)

    # Load our local FAISS index as a retriever
    vector_store = FAISS.load_local("faiss_index", embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Create memory 'chat_history'
    memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history")

    # Create the Conversational Chain
    chain = ConversationalRetrievalChain.from_llm(llm,
                                                  retriever=retriever,
                                                  memory=memory,
                                                  get_chat_history=lambda h: h,
                                                  verbose=True)

    # Create system prompt
    template = """
    You are an AI assistant for answering questions about the most recent 10-K of the top companies in the U.S. including:. 
    Agilent Technologies
Apple Inc.
AbbVie Inc.
Accenture
Amgen Inc.
Amazon.com Inc.
Broadcom Inc.
Bank of America Corp
Comcast Corporation
ConocoPhillips
Costco Wholesale Corporation
Salesforce.com, Inc.
Cisco Systems, Inc.
The Walt Disney Company
Danaher Corporation
Alphabet Inc. (Class C)
Alphabet Inc. (Class A)
Intel Corporation
Intuit Inc.
Johnson & Johnson
JPMorgan Chase & Co.
The Coca-Cola Company
Eli Lilly and Company
Mastercard Incorporated
McDonald's Corporation
Meta Platforms, Inc.
Merck & Co., Inc.
Microsoft Corporation
Oracle Corporation
PepsiCo, Inc.
Pfizer Inc.
Procter & Gamble Co.
Philip Morris International Inc.
Tesla, Inc.
Texas Instruments Incorporated
UnitedHealth Group Incorporated
Visa Inc.
Verizon Communications Inc.
Wells Fargo & Co.
Walmart Inc.
Exxon Mobil Corporation
    The 10-k provides a comprehensive overview of a company's financial health and business performance over the previous year. 
    You are given the following extracted parts of the 10-k and a question. Questions should Provide a conversational answer.
    If you don't know the answer, just say 'Sorry, I don't know... 😔'.
    Don't try to make up an answer.
    If the question is not about the busniess of one of these top companies, politely inform them that you are tuned to only answer questions about the
    top 50 companies by market share.

    {context}
    Question: {question}
    Helpful Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=QA_CHAIN_PROMPT)

    return chain