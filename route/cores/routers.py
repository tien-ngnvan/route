from pydantic import BaseModel
from typing import Any, Optional, List



class BaseRouter(BaseModel):
    register_nodes: List[Any] = []
    
    def register_node(self, name, description):
        """ Register output predict of node"""
        return
    
    def get_nodes(self):
        return self.register_nodes
    
    def invoke(self, text):
        assert isinstance(text, str)

    async def ainvoke(self, text: str):
        assert isinstance(text, str)
    
    
class BaseRouterOutput(BaseModel):
    content: Optional[Any] = None
    meta_data: Optional[Any] = None
    scores: Optional[float] = None
    
    