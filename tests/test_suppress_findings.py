import boto3
from botocore.stub import Stubber

from aws_securityhub_suppression import Workload
from aws_securityhub_suppression.suppress_findings import SuppressFindings


def test_suppress(workload: Workload) -> None:
    client = boto3.client("securityhub", region_name="eu-west-1")

    with Stubber(client) as stubber:
        stubber.add_response(
            method="batch_update_findings",
            service_response={"ProcessedFindings": [], "UnprocessedFindings": []},
            expected_params={
                "FindingIdentifiers": [
                    {
                        "Id": "arn:aws:securityhub:eu-west-1:000000000000:subscription/finding/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                        "ProductArn": "arn:aws:securityhub:eu-west-1::product/aws/securityhub",
                    }
                ],
                "Note": {
                    "Text": "Good reason",
                    "UpdatedBy": "Cloud Center of Excellence",
                },
                "Workflow": {"Status": "SUPPRESSED"},
            },
        )

        suppress_findings = SuppressFindings(client=client, workload=workload)
        suppress_findings.execute()

        stubber.assert_no_pending_responses()
