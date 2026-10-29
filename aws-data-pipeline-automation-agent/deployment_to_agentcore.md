# Deploy AWS Data Pipeline Automation Agent to Amazon Bedrock AgentCore

## 1. Purpose

This project packages a JBehave-style data-pipeline test automation harness for deployment to Amazon Bedrock AgentCore. The workflow generates/parses test stories, checks AWS S3 and Glue execution, validates a transformation rule, and records the test lifecycle through an Xray/Jira adapter plus CSV execution report.

> **Important:** the MWAA/Airflow DAG status and Xray REST calls are intentionally adapter placeholders in this sample. Wire them to your environment before production use.

## 2. Prerequisites

- AWS account and AWS CLI credentials configured for the target account/region.
- Python 3.11+.
- IAM permissions for STS, S3 and Glue used by the runtime.
- Amazon Bedrock/AgentCore permissions required by your organization's deployment model.
- Xray/Jira credentials if enabling real Xray integration.

Check AWS identity:

```bash
aws sts get-caller-identity
```

## 3. Create a virtual environment

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure environment variables

For real Xray integration, do not hard-code secrets. Configure them in your deployment secret/environment mechanism:

```bash
export XRAY_API_URL="https://your-domain.atlassian.net"
export XRAY_API_TOKEN="replace-with-secret-reference"
```

## 5. IAM permissions

The runtime role should follow least privilege. At minimum, this sample needs permissions equivalent to:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sts:GetCallerIdentity"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET",
        "arn:aws:s3:::YOUR_BUCKET/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:GetJobRuns", "glue:GetJobRun", "glue:GetJob"],
      "Resource": "*"
    }
  ]
}
```

Add MWAA/Airflow, Secrets Manager, Bedrock, CloudWatch, or Jira networking permissions as required by your implementation.

## 6. AgentCore configuration

The included `.agentcoreconfig` uses:

```yaml
agent_name: aws-data-pipeline-automation-agent
entrypoint: src/agentcore_entrypoint.py
python_version: "3.11"
memory_size: 2048
timeout: 300
region: us-east-1
```

Change the region and runtime settings to match your AWS environment.

## 7. Configure and launch

From the project root:

```bash
agentcore configure -e src/agentcore_entrypoint.py
agentcore launch
```

AgentCore CLI syntax can evolve; if your installed starter toolkit prompts for runtime/entrypoint details, use `src/agentcore_entrypoint.py` and the `handler`/`lambda_handler` entry functions supplied by this project.

## 8. Invoke the agent

```bash
agentcore invoke '{
  "contract_name": "order_fee_contract",
  "s3_path": "s3://my-data-lake-bucket/raw/orders/",
  "bucket": "my-data-lake-bucket",
  "prefix": "data-contracts/orders/",
  "glue_job": "orders-transform-job",
  "dag_id": "orders_dag_pipeline"
}'
```

Expected workflow:

1. Generate a `.story` file from the contract configuration.
2. Parse the JBehave Given/When/Then steps.
3. Verify AWS caller identity and S3 prefix access.
4. Read the latest Glue job run status.
5. Check the DAG adapter status.
6. Validate the fee transformation rule.
7. Register/update the Xray/Jira lifecycle adapter.
8. Write `Test_Execution_Report.csv`.
9. Return a JSON orchestration result.

## 9. Production hardening

Before production deployment:

- Replace the hard-coded sample transformation record with data loaded from S3 output artifacts.
- Implement actual MWAA/Airflow DAG status lookup rather than the sample `SUCCESS` value.
- Implement authenticated Xray REST API calls instead of sample IDs.
- Store Jira/Xray credentials in AWS Secrets Manager or another approved secret store.
- Add retry/backoff and structured error handling around AWS/API calls.
- Add CloudWatch structured logging, metrics and tracing.
- Add idempotency for Xray test/execution creation.
- Add schema/data-contract validation and multiple transformation rules.
- Add unit/integration tests and CI/CD deployment controls.

## 10. Troubleshooting

If S3 validation fails, confirm the runtime role can list the bucket/prefix. If Glue status returns `NOT_FOUND`, verify the job name and region. If the latest Glue run is not `SUCCEEDED`, the harness intentionally marks validation as failed. For Xray, replace the adapter placeholders and ensure outbound connectivity and authentication are configured.
