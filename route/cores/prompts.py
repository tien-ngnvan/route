import re
from typing import List



class PromptTemplate:
    def __init__(self, input_variables: List[str], template: str):
        self.input_variables = input_variables
        self.template = template

    def format(self, **kwargs):
        """
        Format the template by replacing placeholders with values.
        Any missing values in kwargs will use the default input_variables as keys.
        """
        for var in self.input_variables:
            if var not in kwargs:
                raise ValueError(f"Missing value for required input variables: {var}")

        formatted_template = self.template
        for var, value in kwargs.items():
            formatted_template = formatted_template.replace(f"{{{var}}}", str(value))
            
        # Checking for variables in the template
        variables = self.check_variables(formatted_template)
        if variables:
            print(f"\n⚠️ Warning: Unfilled placeholders in template: {variables}\n")
            for var in variables:
                formatted_template = formatted_template.replace(f"{{{var}}}", ' ')

        return formatted_template

    def from_template(self, template: str):
        """
        Update the template string if needed.
        """
        self.template = template
    
    def check_variables(self, input_string: str, pattern=r"\{(.*?)\}") -> List[str]:
        """
        Return the list of variables (placeholders) found in the template.
        """
        values = re.findall(pattern, input_string)
        
        return values