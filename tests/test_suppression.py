from aws_securityhub_suppression import Suppression


def test_suppression() -> None:
    assert Suppression.from_dict({}) is None

    suppression = Suppression.from_dict(
        {"Name": "my-name", "Reason": "My Reason", "Findings": []}
    )
    assert isinstance(suppression, Suppression) is True
    assert suppression.name == "my-name"
    assert suppression.reason == "My Reason"
    assert suppression.findings == []
