import csv
import os
import os
import requests

XRAY_AUTH_URL = (
    "https://xray.cloud.getxray.app/api/v2/authenticate"
)

XRAY_GRAPHQL_URL = (
    "https://xray.cloud.getxray.app/api/v2/graphql"
)



def create_xray_test_case_with_steps(story_name: str, steps: list, xray_api_url: str, auth_token: str):
    # Replace with the Xray Cloud/Server REST API call appropriate for your environment.
    return {
        "xray_test_key": "XRAY-102",
        "story_name": story_name,
        "parsed_steps": steps,
        "status": "Successfully registered in Jira Xray with Given/When/Then steps",
    }


def post_test_execution_result_csv(result_data: list, filename="Test_Execution_Report.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["TestCaseID", "Scenario", "Status", "Timestamp"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in result_data:
            writer.writerow(row)
    return {"status": "CSV Report generated successfully", "file": filename}


def create_xray_test_execution(test_key: str, status: str):
    return {
        "jira_xray_execution": "EX-502",
        "test_key": test_key,
        "execution_status": status,
    }  


def get_xray_token() -> str:

    response = requests.post(
        XRAY_AUTH_URL,
        json={
            "client_id": os.environ["XRAY_CLIENT_ID"],
            "client_secret": os.environ["XRAY_CLIENT_SECRET"]
        },
        timeout=30
    )

    response.raise_for_status()

    # Xray returns the token as a JSON string.
    return response.json()



def create_xray_test(
    project_key: str,
    requirement_key: str,
    summary: str,
    steps: list[dict]
) -> dict:
    """
    Create an Xray manual Test and link it
    to the Jira requirement/user story.

    steps example:

    [
        {
            "action": "Orders CSV exists in S3",
            "data": "s3://bucket/input/orders.csv",
            "result": "CSV file exists"
        }
    ]
    """

    token = get_xray_token()

    mutation = """
    mutation CreateTest(
        $testType: UpdateTestTypeInput!,
        $steps: [CreateStepInput],
        $jira: JSON!,
        $requirements: [String]
    ) {
        createTest(
            testType: $testType
            steps: $steps
            jira: $jira
            requirements: $requirements
        ) {
            test {
                issueId
                jira(fields: ["key", "summary"])
            }
            warnings
        }
    }
    """

    variables = {

        "testType": {
            "name": "Manual"
        },

        "jira": {
            "fields": {
                "project": {
                    "key": project_key
                },

                "summary": summary
            }
        },

        "steps": steps,

        "requirements": [
            requirement_key
        ]
    }

    response = requests.post(
        XRAY_GRAPHQL_URL,

        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },

        json={
            "query": mutation,
            "variables": variables
        },

        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        raise RuntimeError(
            f"Xray GraphQL error: {result['errors']}"
        )

    test = result["data"]["createTest"]["test"]

    jira_data = test.get("jira", {})

    return {
        "issue_id": test["issueId"],
        "test_key": jira_data.get("key"),
        "summary": jira_data.get("summary"),
        "requirement_key": requirement_key,
        "warnings":
            result["data"]["createTest"].get(
                "warnings", []
            )
    }
