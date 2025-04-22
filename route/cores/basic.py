from abc import ABC
from uuid import uuid4
from typing import Any, Dict, Optional, List


class BaseNode(ABC):
    def __init__(
        self,
        name: str,
        description: str = "",
        metadata: Optional[Dict[str, str]] = None,
        node_id: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.metadata = metadata or {}
        self.id = node_id or str(uuid4())

    def __str__(self):
        return (
            f"Node(id={self.id}, name={self.name}, description={self.description}, "
            f"metadata={self.metadata})"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'BaseNode':
        raise NotImplementedError("Subclasses must implement `from_json` method.")

    @classmethod
    def from_file(cls, data: Dict[str, Any]) -> List['BaseNode']:
        raise NotImplementedError("Subclasses must implement `from_file` method.")

    @classmethod
    def from_database(cls, data: Dict[str, Any]) -> List['BaseNode']:
        raise NotImplementedError("Subclasses must implement `from_database` method.")
