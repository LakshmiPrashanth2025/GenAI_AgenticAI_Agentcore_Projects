# AWS Data Pipeline Automation Agent

A multi-agent/JBehave-style automation harness designed for Amazon Bedrock AgentCore. It generates executable-style stories, validates AWS data-pipeline state and transformation rules, and integrates the test lifecycle with an Xray/Jira adapter.

## Components

- **TestGeneratorAgent** — generates JBehave `.story` files from contract/pipeline configuration.
- **DataValidationAgent** — validates AWS account/S3 access, Glue execution status, DAG status adapter, and transformation rules.
- **XRayJiraAgent** — registers test lifecycle data through the Xray adapter and writes a CSV report.
- **OrchestratorAgent** — coordinates the end-to-end workflow.
- **AgentCore entrypoint** — exposes the workflow for runtime invocation.

## Project structure

```text
aws-data-pipeline-automation-agent/
├── src/
│   ├── stories/fee_validation.story
│   ├── tools/
│   │   ├── aws_toolkit.py
│   │   ├── xray_toolkit.py
│   │   └── jbehave_parser.py
│   ├── test_generator_agent.py
│   ├── data_validation_agent.py
│   ├── xray_jira_agent.py
│   ├── orchestrator_agent.py
│   └── agentcore_entrypoint.py
├── .agentcoreconfig
├── requirements.txt
├── deployment_to_agentcore.md
└── README.md
```

## Install

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Deploy

See [`deployment_to_agentcore.md`](deployment_to_agentcore.md) for IAM, configuration, deployment, invocation, and production-hardening guidance.

## Notes

This is a starter implementation. The MWAA/Airflow and Xray/Jira functions are explicit adapters/placeholders and should be connected to real APIs for production. The transformation validator currently demonstrates the 2% fee rule with a sample record; production implementations should load generated output data from S3.
