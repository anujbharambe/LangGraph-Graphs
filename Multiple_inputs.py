from typing import List, TypedDict
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    values : List[int]
    name : str
    operator : str
    result : int

def sum_node(state:AgentState) -> AgentState:
    """Processes a list of values"""
    if state["operator"] == "*":
        state["result"] = f"Hello {state['name']}. Your product is {math.prod(state['values'])}"
    else:
        state["result"] = f"Hello {state['name']}. Your sum is {sum(state['values'])}"
    print(state)
    return state

graph = StateGraph(AgentState)
graph.add_node("processor", sum_node)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

# result = app.invoke({"values": [2,3,4], "name": "Alice", "operator": "+"})
result = app.invoke({"values": [2,3,4], "name": "Alice", "operator": "*"})
print(result["result"])