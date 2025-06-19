# src/financial_researcher/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class ResearchCrew():
    """Research crew for analyzing AI advancements in banking and finance"""

    @agent
    def ai_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_researcher'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def fintech_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['fintech_analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AI in finance research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )