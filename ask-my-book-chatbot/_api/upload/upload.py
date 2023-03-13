"""Script to upload books to a vector index."""
import json
import re
from pathlib import Path
from typing import Optional, Set

import click
from langchain.document_loaders import PagedPDFSplitter
from steamship import Steamship
from steamship_langchain.vectorstores import SteamshipVectorStore

# Step 1: Give your index a name
INDEX_NAME = "test-123"

# Step 2: List the books or folders of books you want to add to your index
BOOKS_OR_BOOK_FOLDERS = [
    "uploads",
]


def index_document(
        document: Path,
        index: SteamshipVectorStore,
        loaded_documents: Optional[Set[str]] = None,
):
    loaded_documents = loaded_documents or set()

    if document.name in loaded_documents:
        if click.confirm(
                f'The book "{document.name}" is already indexed, do you want me to skip it?',
                default=True,
        ):
            return

    loader = PagedPDFSplitter(str(document.resolve()))
    pages = loader.load_and_split()

    index.add_texts(
        texts=[re.sub("\u0000", "", page.page_content) for page in pages],
        metadatas=[{**page.metadata, "source": document.name} for page in pages],
    )


if __name__ == "__main__":
    client = Steamship(workspace=INDEX_NAME)

    doc_index = SteamshipVectorStore(
        client=client, index_name=INDEX_NAME, embedding="text-embedding-ada-002"
    )

    documents = set(
        json.loads(item.metadata)["source"]
        for item in doc_index.index.index.list_items().items
    )

    if len(documents) > 0:
        print(
            "The index already contains the following books: \n* "
            + "\n* ".join(documents)
        )
        if click.confirm("Do you want to reset your index?", default=True):
            print("Resetting your index, this will take a while ⏳")
            doc_index.index.reset()

    for book in BOOKS_OR_BOOK_FOLDERS:
        data_path = Path(book)

        if data_path.is_dir():
            for child_data_path in data_path.iterdir():
                index_document(child_data_path, doc_index, documents)
        else:
            index_document(data_path, doc_index, documents)

    package_instance = client.use(
        "ask-my-book-chat-api", config={"index_name": INDEX_NAME}, version="0.0.22"
    )
    print("Your documents are successfully added to the index")
    print("You can query your documents on this endpoint: ")
    print(package_instance.invocation_url)


