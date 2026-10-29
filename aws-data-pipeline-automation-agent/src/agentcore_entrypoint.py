import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator_agent import OrchestratorAgent


def lambda_handler(event, context=None):
    body = json.loads(event.get("body", "{}")) if isinstance(event, dict) and "body" in event else event
    body = body or {}

    config = {
        "contract_name": body.get("contract_name", "order_fee_contract"),
        "s3_path": body.get("s3_path", "s3://my-bucket/raw/orders/"),
        "glue_job": body.get("glue_job", "orders-transform-job"),
        "dag_id": body.get("dag_id", "orders_dag_pipeline"),
        "bucket": body.get("bucket", "my-data-lake-bucket"),
        "prefix": body.get("prefix", "data-contracts/orders/"),
        "rule_description": body.get(
            "rule_description",
            "the transformation rules in the data contract are satisfied where fees match the order amount calculation",
        ),
    }

    result = OrchestratorAgent().run_pipeline(config)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": result,
            "success": result["validation_results"]["status"] == "SUCCESS",
            "metadata": {"framework": "JBehave-AgentCore Harness"},
        }),
    }


# AgentCore-friendly callable alias.
def handler(payload, context=None):
    return lambda_handler(payload, context)
