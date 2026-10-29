import os
import re


def parse_story_file(file_path: str):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    scenarios = []
    scenario_pattern = re.compile(r"Scenario:\s*(.*?)(?=\n\s*Scenario:|\Z)", re.DOTALL)

    for match in scenario_pattern.findall(content):
        lines = [line.strip() for line in match.strip().split("\n") if line.strip()]
        if not lines:
            continue
        scenario_title = lines[0]
        steps = []
        for line in lines[1:]:
            if line.startswith(("Given", "When", "Then", "And")):
                steps.append(line)
        scenarios.append({"scenario_name": scenario_title, "steps": steps})

    return scenarios
