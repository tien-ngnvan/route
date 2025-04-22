import json
from typing import List, Dict, Any, Optional
from route.cores import BaseNode



class Node(BaseNode):
    def __init__(
        self,
        name: str,
        description: str = "",
        metadata: Dict[str, Any] = None,
        node_id: Optional[str] = None,
    ):
        super().__init__(name, description, metadata, node_id)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Node':
        """
        Creates a Node from a JSON-like dictionary.
        
        :param data: A dictionary containing the data for the node.
        :return: A Node object initialized with the given data.
        """
        return cls(
            name=data.get('name'),
            description=data.get('description', ''),
            metadata=data.get('metadata', {}),
            node_id=data.get('id'),
        )

    @classmethod
    def from_file(cls, file_path: str) -> List['Node']:
        """
        Reads a JSON file and returns a list of Node objects.
        
        :param file_path: Path to the JSON file.
        :return: A list of Node objects.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [cls.from_json(item) for item in data]