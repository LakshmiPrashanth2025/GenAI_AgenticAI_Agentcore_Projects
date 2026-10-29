from data_validation_agent import DataValidationAgent
from test_generator_agent import TestGeneratorAgent
from tools.jbehave_parser import parse_story_file
from xray_jira_agent import XRayJiraAgent


class OrchestratorAgent:
    def __init__(self):
        self.generator = TestGeneratorAgent()
        self.validator = DataValidationAgent()
        self.xray_agent = XRayJiraAgent()

    def run_pipeline(self, config: dict):
        contract_name = config.get("contract_name", "order_fee_contract")
        story_file_path = self.generator.generate_jbehave_story_file(contract_name, config)

        parsed_scenarios = parse_story_file(story_file_path)
        scenario = parsed_scenarios[0] if parsed_scenarios else {}
        scenario_name = scenario.get("scenario_name", "Default Scenario")
        steps = scenario.get("steps", [])

        validation_res = self.validator.execute_validation_steps(
            bucket=config["bucket"],
            prefix=config["prefix"],
            glue_job=config["glue_job"],
            dag_id=config["dag_id"],
        )
        exec_status = validation_res["status"]

        lifecycle_res = self.xray_agent.process_test_lifecycle(
            scenario_name=scenario_name,
            steps=steps,
            execution_result=exec_status,
        )

        return {
            "orchestrator_status": "COMPLETED",
            "generated_story_file": story_file_path,
            "parsed_scenario": scenario,
            "validation_results": validation_res,
            "xray_jira_integration": lifecycle_res,
        }
