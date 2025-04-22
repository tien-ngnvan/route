import uuid
from abc import ABC
from pydantic import BaseModel, Field, UUID4
from typing import Any, Optional, List, Dict
from route.cores import BaseNode



class BaseRouter(ABC, BaseModel):
    """
    Abstract base class for defining API routers.
    """
    
    id: UUID4 = Field(default_factory=uuid.uuid4, frozen=True)
    key:str = Field(default=None, description="Authentication key to connect to the API")
    url:str = Field(default=None, description="Base URL of the API")
    nodes: Optional[List[BaseNode]] = Field(
        default_factory=list, 
        description="Node prediction to classifier"
    )
    
    model_config = {"arbitrary_types_allowed": True}
    
    def from_file(self, file_path):
        """
            Return a list of Nodes initialized from file
        
        Args:
            file_path: a file direction path
            
        Returns:
            List of Nodes initialized from file
        """
        
        raise NotImplementedError("Subclasses must implement `register_node` method.")
    
    async def afrom_file(self, file_path):
        """
        Async return a list of Nodes initialized from file
        
        Args:
            file_path: a file direction path
            
        Returns:
            List of Nodes initialized from file
        
        Returns:
            A Node 
        """
        raise NotImplementedError("Subclasses must implement `register_node` method.")
    
    def register_node(self, name: str, description: str) -> None:
        """
        Registers a new node in the router.

        Args:
            name: The name of the node.
            description: A description of the node.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement `register_node` method.")

    def get_nodes(self) -> List[Dict[str, str]]:
        """
        Returns the list of registered nodes.

        Returns:
            A list of dictionaries, where each dictionary represents a node
            and contains its name and description.
        """
        return self.nodes

    def invoke(self, text: str, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invokes a specific node in the router synchronously.

        Args:
            text: The input text for the invocation.
            config: Optional configuration parameters for the invocation.

        Returns:
            The result of the invocation.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement `invoke` method.")

    async def ainvoke(self, text: str, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invokes a specific node in the router asynchronously.

        Args:
            text: The input text for the invocation.
            config: Optional configuration parameters for the invocation.

        Returns:
            The result of the asynchronous invocation.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        return await self.invoke(text, config)