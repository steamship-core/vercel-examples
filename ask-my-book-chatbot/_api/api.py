import json
from typing import Type, Optional, Dict, Any, List

import langchain
from langchain.chains import ChatVectorDBChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from steamship.invocable import Config
from steamship.invocable import PackageService, post, get
from steamship_langchain import OpenAI
from steamship_langchain.vectorstores import SteamshipVectorStore

from chat_history import ChatHistory
from constants import DEBUG
from fact_checker import FactChecker
from prompts import ANSWER_QUESTION_PROMPT, CONDENSE_QUESTION_PROMPT

langchain.llm_cache = None


class AskMyBook(PackageService):
    class AskMyBookConfig(Config):
        index_name: str
        default_chat_session_id: Optional[str] = "default"

    config: AskMyBookConfig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qa_chatbot_chain = self._get_qa_chain()
        self.fact_checker = FactChecker(self.client)

    @classmethod
    def config_cls(cls) -> Type[Config]:
        return cls.AskMyBookConfig

    @get("/documents", public=True)
    def get_indexed_documents(self) -> List[str]:
        """Fetch all the documents in the index"""
        return list(
            set(
                json.loads(item.metadata)["source"]
                for item in self._get_index().index.index.list_items().items
            )
        )

    @post("/answer", public=True)
    def answer(
        self, question: str, chat_session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Answer a given question using a collection of source documents."""
        chat_session_id = chat_session_id or self.config.default_chat_session_id
        chat_history = ChatHistory(self.client, chat_session_id)

        result = self.qa_chatbot_chain(
            {"question": question, "chat_history": chat_history.load()}
        )
        sources = result["source_documents"]
        if len(sources) == 0:
            return {
                "answer": "No sources found to answer your question. Please try another question.",
                "sources": sources,
                "is_plausible": True,
            }

        answer = result["answer"].strip()
        chat_history.append(question, answer)
        is_plausible = self.fact_checker.fact_check(question, answer, sources)

        return {
            "answer": answer,
            "sources": sources,
            "is_plausible": is_plausible,
        }

    def _get_index(self):
        """Get the vector store index."""
        return SteamshipVectorStore(
            client=self.client,
            index_name=self.config.index_name,
            embedding="text-embedding-ada-002",
        )

    def _get_qa_chain(self):
        """Construct the question answering chain."""
        doc_index = self._get_index()

        answer_question_chain = load_qa_chain(
            OpenAI(client=self.client, temperature=0, verbose=DEBUG),
            chain_type="stuff",
            prompt=ANSWER_QUESTION_PROMPT,
            verbose=DEBUG,
        )
        condense_question_chain = LLMChain(
            llm=OpenAI(client=self.client, temperature=0, verbose=DEBUG),
            prompt=CONDENSE_QUESTION_PROMPT,
        )
        return ChatVectorDBChain(
            vectorstore=doc_index,
            combine_docs_chain=answer_question_chain,
            question_generator=condense_question_chain,
            return_source_documents=True,
            top_k_docs_for_context=2,
        )
