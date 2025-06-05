# app/agents/base_agent.py

from crewai import Agent

def create_base_agent(name: str, goal: str, backstory: str, tools=None) -> Agent:
    return Agent(
        role=name,
        goal=goal,
        backstory=backstory,
        tools=tools or [],  # ✅ Properly include tools here
        verbose=True
    )
