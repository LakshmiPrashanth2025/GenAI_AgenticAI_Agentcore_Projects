Narrative:
As a Data Engineer
I want to validate order data contracts and transformations in AWS S3
So that calculated fees comply with business rules

Scenario: Verify order fee calculation based on data contract and S3 output
Given data contract and source CSV exist in S3 path "s3://my-bucket/raw/orders/"
When the Glue job "orders-transform-job" and DAG "orders_dag_pipeline" execute successfully
And output artifacts are generated in S3 test output folder
Then the transformation rules in the data contract are satisfied where fees match the order amount calculation
