from langchain import PromptTemplate

CONDENSE_QUESTION_PROMPT_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    CONDENSE_QUESTION_PROMPT_TEMPLATE
)

ANSWER_QUESTION_PROMPT_TEMPLATE = """I want you to ANSWER a QUESTION based on the following pieces of CONTEXT. 

        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Your ANSWER should be analytical and straightforward. 
        Try to share deep, thoughtful insights and explain complex ideas in a simple and concise manner. 
        When appropriate use analogies and metaphors to illustrate your point. 
        Your ANSWER should have a strong focus on clarity, logic, and brevity.
        Your ANSWER should be truthful and correct according to the given SOURCES

        CONTEXT: {context}

        QUESTION: {question}

        ANSWER:
        """
ANSWER_QUESTION_PROMPT = PromptTemplate(
    template=ANSWER_QUESTION_PROMPT_TEMPLATE, input_variables=["context", "question"]
)
