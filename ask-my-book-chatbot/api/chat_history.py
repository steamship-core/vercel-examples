import json
from datetime import datetime
from typing import Optional, List, Tuple

from steamship import File, SteamshipError, Steamship, Block, Tag
from steamship.data import TagKind


def _block_sort_key(block: Block) -> str:
    """Return a sort key for Blocks based on associated timestamp tags."""
    return [
        tag.value.get("timestamp")
        for tag in block.tags
        if tag.kind == TagKind.TIMESTAMP
    ][0]


def _timestamp_tag() -> Tag:
    """Return a Tag with the current datetime as the value"""
    return Tag(
        kind=TagKind.TIMESTAMP,
        value={"timestamp": datetime.now().isoformat()},
    )


class ChatHistory:
    def __init__(self, client: Steamship, chat_session_id: Optional[str] = None):
        self.chat_session_id = chat_session_id or "default"
        self.client = client

    def _get_chat_history_file(self) -> Optional[File]:
        try:
            return File.get(self.client, handle=self.chat_session_id)
        except SteamshipError:
            return None

    def _get_or_create_chat_history_file(self) -> File:
        convo_file = self._get_chat_history_file()
        if convo_file:
            return convo_file
        return File.create(self.client, handle=self.chat_session_id, blocks=[])

    def append(self, question: str, message: str):
        conversation_file = self._get_or_create_chat_history_file()
        Block.create(
            self.client,
            file_id=conversation_file.id,
            text=json.dumps((question, message)),
            tags=[_timestamp_tag()],
        )

    def load(self) -> List[Tuple[str, str]]:
        """Return history buffer."""
        convo_file = self._get_chat_history_file()
        if not convo_file:
            return []

        return [
            json.loads(block.text)
            for block in sorted(convo_file.blocks, key=_block_sort_key)
        ]

    def clear(self) -> None:
        convo_file = self._get_chat_history_file()
        if convo_file:
            convo_file.delete()


if __name__ == "__main__":
    client = Steamship()
    ch = ChatHistory(client, chat_session_id="random-chat-history")
    print(ch.load())
    ch.clear()
    ch.append("question 1", "message 1")
    print(ch.load())
    ch.append("question 2", "message 2")
    print(ch.load())
