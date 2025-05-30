from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    num1 : int
    num2 : int
    operator : str
    result : int

def adder(state: AgentState) -> AgentState:
    """Adds two numbers"""
    state["result"] = state["num1"] + state["num2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    """Subtracts two numbers"""
    state["result"] = state["num1"] - state["num2"]
    return state

def decide_next_node(state: AgentState) -> AgentState:
    """Decides which operation to perform based on the operator"""
    if state["operator"] == "+":
        return "addition_operation"
    elif state["operator"] == "-":
        return "subtraction_operation"

graph = StateGraph(AgentState)
graph.add_node("add", adder)
graph.add_node("subtract", subtractor)
graph.add_node("router", lambda state: state)

graph.add_edge(START, "router")

graph.add_conditional_edges("router", decide_next_node, {
    "addition_operation": "add",
    "subtraction_operation": "subtract"
})

graph.add_edge("add", END)
graph.add_edge("subtract", END)

app = graph.compile()
result = app.invoke({"num1": 10, "num2": 5, "operator": "+"})
# result = app.invoke({"num1": 10, "num2": 5, "operator": "-"})
print(f"Result of addition: {result['result']}")