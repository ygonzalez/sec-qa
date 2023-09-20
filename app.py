import time
import streamlit as st
from utils import load_chain

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://www.sec.gov/files/sec-logo.png'

# Configure streamlit page
st.set_page_config(
    page_title="Your SEC 10-K Chatbot",
    page_icon=company_logo
)

# Display company logo and title
st.image(company_logo, width=150)  # Adjust width as needed
st.title("Welcome to the SEC 10-K AI Chatbot")
st.write("""
The **10-K** is an annual report filed by companies to the U.S. Securities and Exchange Commission (SEC). 
It provides a comprehensive summary of a company's performance and includes details such as its organizational structure, financial statements, 
earnings per share, and benefits plans. This document can also cover a company's history, 
equity, holdings, subsidiaries, executive compensation, and any other relevant data.

Sample questions you can ask about a 10-K include:
- Can you provide a detailed overview of [company]'s core business operations, including its main products or services and target markets?
- What competitive advantages does [company] have in its industry?
- Are there any pending or ongoing legal proceedings that could result in financial liabilities or damage to [company]'s reputation?
- What are the current industry and market conditions, and how do they impact [company]'s growth potential?
- Who are [company]'s major competitors, and how does it differentiate itself in the market?
""")

# Initialize LLM chain in session_state
if 'chain' not in st.session_state:
    st.session_state['chain'] = load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant",
                                     "content": "Hi human! I am the SEC 10-K AI. How can I help you today?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Sidebar with company list
companies = [
    "Agilent Technologies", "Apple Inc.", "AbbVie Inc.", "Accenture", "Amgen Inc.",
    "Amazon.com Inc.", "Broadcom Inc.", "Bank of America Corp", "Comcast Corporation",
    "ConocoPhillips", "Costco Wholesale Corporation", "Salesforce.com, Inc.", "Cisco Systems, Inc.",
    "The Walt Disney Company", "Danaher Corporation", "Alphabet Inc. (Class C)", "Alphabet Inc. (Class A)",
    "Intel Corporation", "Intuit Inc.", "Johnson & Johnson", "JPMorgan Chase & Co.", "The Coca-Cola Company",
    "Eli Lilly and Company", "Mastercard Incorporated", "McDonald's Corporation", "Meta Platforms, Inc.",
    "Merck & Co., Inc.", "Microsoft Corporation", "Oracle Corporation", "PepsiCo, Inc.", "Pfizer Inc.",
    "Procter & Gamble Co.", "Philip Morris International Inc.", "Tesla, Inc.", "Texas Instruments Incorporated",
    "UnitedHealth Group Incorporated", "Visa Inc.", "Verizon Communications Inc.", "Wells Fargo & Co.",
    "Walmart Inc.", "Exxon Mobil Corporation"
]

st.sidebar.subheader("The SEC Chatbot includes 10-k information on the following top companies:")
for company in companies:
    st.sidebar.text(company)

# Chat logic
if query := st.chat_input("Ask me about the 10-k"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking..."):  # <-- This is where the spinner gets activated
        with st.chat_message("assistant", avatar=company_logo):
            message_placeholder = st.empty()
            # Send user's question to our chain
            result = st.session_state['chain']({"question": query})
            response = result['answer']
            full_response = ""

            # Simulate stream of response with milliseconds delay
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

