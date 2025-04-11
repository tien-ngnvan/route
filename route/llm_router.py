from typing import Optional, Any
from route.cores import BaseRouter


class LLMRouter(BaseRouter):
    model: Optional[Any] = None
    
    def format_register_nodes(self) -> str:
        """
        Formats the registered nodes into a string where each node's name and description
        are displayed on a new line. Each node's name is enclosed in backticks, followed
        by its description.

        Returns:
            str: A formatted string representing all registered nodes, each on a new line.
        """
        
        texts = []
        for node in self.register_nodes:
            texts.append(f"`{node['name']}`: {node['description']} ")

        register_node = "\n\n".join(t for t in texts)

        return register_node

    def register_node(self, name: str, description: str) -> None:
        """
        Registers a new node by adding a dictionary with 'name' and 'description'
        to the list of registered nodes.

        Args:
            name (str): The name of the node to register.
            description (str): A brief description of the node.
        """
        
        self.register_nodes.append({
            "name": name, "description": description
        })
    
    def invoke(self, text):
        return    

    async def a_invoke(self, text):
        return self.invoke(text)
    
    

if __name__ == '__main__':
    from route.prompt_configs.llm_router_configs import LLAMA3_PROMPT
    from route.cores.prompts import PromptTemplate
    
    router = LLMRouter(
        model=''
    )

    router.register_node(name='CHAT', description='The CHAT node is responsible for maintaining an ongoing conversation with the user. It is designed for casual, continuous dialogue, and the system should focus on engagement and context retention.')
    router.register_node(name='QUESTION_ANSWERING', description='The QUESTION_ANSWERING node is focused on responding to a user query with a clear, accurate, and concise answer. It is used when the user asks specific, direct questions that require factual or informational responses.')
    router.register_node(name='REASONING', description='The REASONING node is used to explain a process, decision, or complex concept. It requires logical, step-by-step explanations and might involve reasoning through a problem or concept to help the user understand a conclusion.')
    
    structure_prompt = router.format_register_nodes()
    
    prompt_template = PromptTemplate(
        input_variables=["register_nodes", "question"],
        template=LLAMA3_PROMPT
    )
    
    prompt = prompt_template.format(register_nodes=structure_prompt, question='Can you exaplain me a define of solution?')
    
    print("\nprompt: ", prompt, "\n\n")
