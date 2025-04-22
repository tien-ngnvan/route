import asyncio
import requests
from typing import Any, Dict, Optional
from pydantic import model_validator

from route.nodes import Node
from route.cores import BaseRouter
from route.utils import convert_to_secret_str, get_from_dict_or_env



class LLMRouter(BaseRouter):
    """Router for interacting with a Language Model (LLM) API."""
    
    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that the API key exists in the environment."""
        try:
            api_key = convert_to_secret_str(
                get_from_dict_or_env(values, "key", "LLM_ROUTER_KEY")
            )

        except ValueError as original_exc:
            raise original_exc

        session = requests.Session()
        session.headers.update(
            {
                "Authorization": f"Bearer {api_key.get_secret_value()}",
                "Accept-Encoding": "identity",
                "Content-type": "application/json",
            }
        )
        
        values["session"] = session

        return values

    def register_node(self, name: str, description: str) -> None:
        """
        Registers a new node, representing a specific function or endpoint
        of the LLM, by adding its name and description to the list of nodes.

        Args:
            name: The unique name of the node.
            description: A brief description of what this node does.
        """
        self.nodes.append(
            Node(name=name, description=description, metadata=None)
        )

    def compile_nodes(self) -> str:
        """
        Formats the list of registered nodes into a human-readable string.
        Each node is represented on a new line with its name in backticks
        followed by its description.

        Returns:
            A string containing the formatted list of registered nodes.
        """
        return "\n".join(
            f"`{node.name}`: {node.description}" for node in self.nodes
        )

    def invoke(self, text: str, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invokes the LLM API with the given text input and optional configuration.

        Args:
            text: The text input to be processed by the LLM.
            config: Optional dictionary containing additional parameters to be
                    passed in the request body.

        Returns:
            The JSON response from the LLM API, specifically the value associated
            with the 'data' key if it exists, otherwise the entire JSON response.

        Raises:
            TypeError: If the `text` input is not a string.
            RuntimeError: If the HTTP request to the LLM API fails.
        """
        if not isinstance(text, str):
            raise TypeError(f"Text input must be a string, got {type(text).__name__}.")

        config = config or {}
        try:
            response = self.session.post(
                self.url, json={"text_input": text, **config}
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            json_resp = response.json()

            return json_resp.get("data", json_resp)

        except requests.RequestException as e:
            raise RuntimeError(f"Request to LLM API failed: {e}") from e

    async def ainvoke(
        self, text: str, config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Asynchronously invokes the LLM API using a separate thread
        to avoid blocking the event loop.

        Args:
            text: The text input for the LLM.
            config: Optional configuration parameters.

        Returns:
            The result of the LLM invocation.
        """
        return await asyncio.to_thread(self.invoke, text, config)
