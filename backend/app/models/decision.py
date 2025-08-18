from typing import List, Optional

from pydantic import BaseModel, Field


class DecisionRequest(BaseModel):
    tree_id: str = Field(
        ..., description="The ID of the decision tree to interact with."
    )
    current_node_id: Optional[str] = Field(
        None, description="The ID of the current node. Omit to start from the root."
    )
    answer: Optional[str] = Field(
        None, description="The user's answer to the question of the current node."
    )


class DecisionResponseData(BaseModel):
    tree_id: str
    node_id: str
    node_type: str = Field(..., description="Either 'DECISION' or 'OUTCOME'.")
    text: str = Field(..., description="The question or the final outcome.")
    possible_answers: Optional[List[str]] = Field(
        None, description="A list of possible answers if the node is a 'DECISION' node."
    )
