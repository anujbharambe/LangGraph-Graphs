from typing import List, TypedDict, Dict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name : str
    age : int
    skills : List[str]
    result : str

def first_node(state : AgentState) -> AgentState:
    state["result"] = f"{state['name']}, welcome to the system! "
    return state

def second_node(state : AgentState) -> AgentState:
    state["result"] += f"You are {state['age']} years old. "
    return state

def third_node(state : AgentState) -> AgentState:
    state["result"] += f"Your skills are: {state['skills']}. "
    return state

graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)

graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.add_edge("second", "third")
graph.set_finish_point("third")

app = graph.compile()
result = app.invoke({"name": "Alice", "age": 30, "skills": ["Python", "Data Analysis", "Machine Learning"]})
print(result["result"])
