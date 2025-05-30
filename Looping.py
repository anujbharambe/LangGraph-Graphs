from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict):
    name : str
    number : List[int]
    counter : int

def greeting_node(state: AgentState) -> AgentState:
    """Greets the user and initializes the counter"""
    state["name"] = f"Hello {state['name']}, let's start counting!"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number and adds it to the list"""
    state["number"].append(random.randint(1, 100))
    state["counter"] += 1
    return state

def should_continue(state : AgentState) -> AgentState:
    """Decides whether to continue or stop based on the counter"""
    if state["counter"] < 5:
        print(f"Entering loop: {state['counter']}")
        return "continue"
    else:
        return "stop"
    
graph = StateGraph(AgentState)
graph.add_node("greet", greeting_node)
graph.add_node("random", random_node)

graph.add_edge("greet","random")

graph.add_conditional_edges("random", should_continue, {
    "continue": "random",
    "stop": END
})

graph.add_edge(START, "greet")

app = graph.compile()

result = app.invoke({"name": "John", "number": [], "counter": 0})
print(result)
