import os
from datetime import datetime, timezone

from tools.xray_toolkit import (
    create_xray_test_case_with_steps,
    create_xray_test_execution,
    post_test_execution_result_csv,
)


class XRayJiraAgent:
    def process_test_lifecycle(self, scenario_name: str, steps: list, execution_result: str):
        xray_tc = create_xray_test_case_with_steps(
            story_name=scenario_name,
            steps=steps,
            xray_api_url=os.getenv("XRAY_API_URL", "https://your-jira-instance.atlassian.net"),
            auth_token=os.getenv("XRAY_API_TOKEN", "YOUR_JIRA_API_TOKEN"),
        )
        test_key = xray_tc["xray_test_key"]

        post_test_execution_result_csv([{
            "TestCaseID": test_key,
            "Scenario": scenario_name,
            "Status": execution_result,
            "Timestamp": datetime.now(timezone.utc).isoformat(),
        }])

        jira_exec = create_xray_test_execution(test_key, execution_result)
        return {
            "xray_test": test_key,
            "parsed_steps_registered": len(steps),
            "execution_entry": jira_exec,
            "report_updated": True,
        }
