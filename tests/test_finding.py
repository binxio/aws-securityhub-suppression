from aws_securityhub_suppression import Finding


def test_finding() -> None:
    finding = Finding.from_dict(
        {
            "Name": "my-name",
            "FindingArn": "arn:aws:securityhub:eu-west-1:111122223333:subscription/custom-standard/finding/11111111-1111-1111-1111-111111111111",
        }
    )
    assert isinstance(finding, Finding) is True
    assert finding.name == "my-name"
    assert finding.id == "11111111-1111-1111-1111-111111111111"
    assert (
        finding.arn
        == "arn:aws:securityhub:eu-west-1:111122223333:subscription/custom-standard/finding/11111111-1111-1111-1111-111111111111"
    )
    assert finding.region == "eu-west-1"
    assert finding.account_id == "111122223333"
    assert finding.service == "securityhub"
    assert finding.generator_id == "custom-standard"
    assert (
        finding.product_arn == "arn:aws:securityhub:eu-west-1::product/aws/securityhub"
    )
    assert str(finding) == finding.arn
