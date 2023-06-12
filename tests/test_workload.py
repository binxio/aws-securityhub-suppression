from aws_securityhub_suppression import Workload


def test_workload() -> None:
    assert Workload.from_dict({}, accounts=[]) is None
    workload = Workload.from_dict({"Name": "my-name"}, accounts=[])
    assert isinstance(workload, Workload) is True
    assert workload.name == "my-name"
    assert workload.accounts == []
