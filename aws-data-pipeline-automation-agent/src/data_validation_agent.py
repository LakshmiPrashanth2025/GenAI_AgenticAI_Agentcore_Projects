from tools.aws_toolkit import (
    check_transformation_rules,
    verify_aws_account_and_s3,
    verify_glue_and_dag_status,
)


class DataValidationAgent:
    def execute_validation_steps(self, bucket: str, prefix: str, glue_job: str, dag_id: str):
        account_check = verify_aws_account_and_s3(bucket, prefix)
        if account_check["status"] != "SUCCESS":
            return {
                "status": "FAILED",
                "reason": "AWS Account or S3 check failed",
                "aws_details": account_check,
            }

        pipeline_check = verify_glue_and_dag_status(glue_job, dag_id)
        if pipeline_check.get("glue_status") != "SUCCEEDED" or pipeline_check.get("dag_status") != "SUCCESS":
            return {
                "status": "FAILED",
                "reason": "Glue job or DAG did not complete successfully",
                "aws_details": account_check,
                "pipeline_details": pipeline_check,
            }

        # Demo record. Replace with records loaded from the generated S3 output artifact.
        sample_record = {"order_amount": 150.0, "calculated_fee": 3.0}
        rule_check = check_transformation_rules(sample_record)

        return {
            "status": "SUCCESS" if rule_check["rule_satisfied"] else "FAILED",
            "aws_details": account_check,
            "pipeline_details": pipeline_check,
            "transformation_validation": rule_check,
        }
