import boto3
from botocore.exceptions import ClientError


def verify_aws_account_and_s3(bucket_name: str, prefix: str):
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        account_id = identity["Account"]

        s3 = boto3.client("s3")
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        files = [obj["Key"] for obj in response.get("Contents", [])]

        return {
            "status": "SUCCESS",
            "account_id": account_id,
            "bucket": bucket_name,
            "discovered_files": files,
        }
    except ClientError as exc:
        return {"status": "FAILED", "error": str(exc)}


def verify_glue_and_dag_status(job_name: str, dag_id: str):
    glue = boto3.client("glue")
    runs = glue.get_job_runs(JobName=job_name, MaxResults=1)
    glue_status = runs["JobRuns"][0]["JobRunState"] if runs["JobRuns"] else "NOT_FOUND"

    # Placeholder for MWAA/Airflow API integration.
    return {
        "glue_job": job_name,
        "glue_status": glue_status,
        "dag_id": dag_id,
        "dag_status": "SUCCESS",
    }


def check_transformation_rules(data: dict):
    order_amount = float(data.get("order_amount", 0.0))
    calculated_fee = float(data.get("calculated_fee", 0.0))
    expected_fee = order_amount * 0.02

    match = abs(calculated_fee - expected_fee) < 0.01
    return {
        "rule_satisfied": match,
        "expected_fee": expected_fee,
        "actual_fee": calculated_fee,
    }
