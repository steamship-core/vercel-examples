from typing import List

from langchain import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.docstore.document import Document
from steamship import Steamship
from steamship_langchain import OpenAI

from constants import DEBUG


class FactChecker:
    FACT_CHECK_PROMPT_TEMPLATE = """I want you to verify the truthfulness and correctness of a given ANSWER. 

                   Answer "incorrect" if you think the ANSWER is incorrect in light of the SOURCES. 
                   Answer "correct" if you think the ANSWER is correct in light of the SOURCES. 

                   QUESTION: {question}

                   ANSWER: {answer}

                   SOURCES: {sources}

                   DECISION: """

    FACT_CHECK_PROMPT = PromptTemplate(
        template=FACT_CHECK_PROMPT_TEMPLATE,
        input_variables=["question", "answer", "sources"],
    )

    def __init__(self, client: Steamship):

        self.fact_check_chain = LLMChain(
            prompt=self.FACT_CHECK_PROMPT,
            llm=OpenAI(client=client, temperature=0, verbose=DEBUG),
        )

    def fact_check(self, question: str, answer: str, sources: List[Document]) -> bool:

        if (
            "I do not know" in answer
            or "I don't know" in answer
            or "No sources found" in answer
        ):
            return True
        if not sources:
            return False

        response = self.fact_check_chain.run(
            question=question,
            answer=answer,
            sources="\n".join([doc.page_content for doc in sources]),
        )
        return "incorrect" not in response.lower()
