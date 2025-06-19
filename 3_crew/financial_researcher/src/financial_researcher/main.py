#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from financial_researcher.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the AI in finance research crew.
    """
    # Create and run the crew
    result = ResearchCrew().crew().kickoff()

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()