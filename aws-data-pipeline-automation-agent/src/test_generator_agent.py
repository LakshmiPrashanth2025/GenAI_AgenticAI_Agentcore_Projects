import os


class TestGeneratorAgent:
    def __init__(self, stories_dir="src/stories"):
        self.stories_dir = stories_dir
        os.makedirs(self.stories_dir, exist_ok=True)

    def generate_jbehave_story_file(self, contract_name: str, rules: dict) -> str:
        file_path = os.path.join(self.stories_dir, f"{contract_name}.story")

        s3_path = rules.get("s3_path", "s3://my-bucket/raw/")
        glue_job = rules.get("glue_job", "default-transform-job")
        dag_id = rules.get("dag_id", "default_dag")
        rule_description = rules.get("rule_description", "fees match the order amount calculation")

        story_content = f'''Narrative:
As a Data Engineer
I want to validate data contracts and transformations for {contract_name} in AWS S3
So that all output artifacts comply with defined business rules

Scenario: Automated validation for {contract_name} pipeline execution and transformation rules
Given data contract and source CSV exist in S3 path "{s3_path}"
When the Glue job "{glue_job}" and DAG "{dag_id}" execute successfully
And output artifacts are generated in S3 test output folder for "{contract_name}"
Then {rule_description}
'''

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(story_content.strip())
        return file_path
