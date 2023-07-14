import os.path

from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from landingzone_organization import Organization

from aws_securityhub_suppression.cli import cli


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0


def test_update_with_debug_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "update"])

    assert result.exit_code == 0


def test_update() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["update"])

    assert result.exit_code == 0


@patch("aws_securityhub_suppression.cli.Context")
def test_update_suppression(mock_context) -> None:
    mock_client = MagicMock()
    mock_context.return_value.session.client.return_value = mock_client

    config_path = os.path.join(os.path.dirname(__file__), "workloads")
    runner = CliRunner()
    result = runner.invoke(cli, ["update", "suppression", config_path])

    assert mock_client.batch_update_findings.called is True
    mock_client.batch_update_findings.assert_called_with(
        FindingIdentifiers=[
            {
                "Id": "arn:aws:securityhub:eu-west-1:111122223333:subscription/custom-standard/finding/11111111-1111-1111-1111-111111111111",
                "ProductArn": "arn:aws:securityhub:eu-west-1::product/aws/securityhub",
            }
        ],
        Note={
            "Text": "The reason why this finding can be suppressed.",
            "UpdatedBy": "Cloud Center of Excellence",
        },
        Workflow={"Status": "SUPPRESSED"},
    )

    assert result.exit_code == 0


@patch("aws_securityhub_suppression.documentation_generator.DocumentationGenerator")
def test_update_docs(mock_generator) -> None:
    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "test-template.md"
    )
    config_path = os.path.join(os.path.dirname(__file__), "workloads")
    runner = CliRunner()

    result = runner.invoke(cli, ["update", "docs", template_path, config_path])
    assert mock_generator.called is True
    assert result.exit_code == 0


@patch("aws_securityhub_suppression.workload_generator.WorkloadGenerator")
@patch("landingzone_organization.AWSOrganization")
@patch("boto3.session.Session")
def test_prepare(
    mock_session, mock_organization, mock_workload_generator, organization: Organization
) -> None:
    mock_organization.return_value.parse.return_value = organization

    config_path = os.path.join(os.path.dirname(__file__), "workloads")
    runner = CliRunner()
    result = runner.invoke(cli, ["prepare", config_path, "Workloads"])

    assert mock_workload_generator.return_value.execute.called is True

    assert result.exit_code == 0


def test_check() -> None:
    config_path = os.path.join(os.path.dirname(__file__), "workloads")
    runner = CliRunner()
    result = runner.invoke(cli, ["check", config_path])

    assert result.exit_code == 0


def test_check_invalid_path() -> None:
    config_path = os.path.join(os.path.dirname(__file__), "non-existing-folder")
    runner = CliRunner()
    result = runner.invoke(cli, ["check", config_path])
    assert "non-existing-folder is not a valid path" in result.output

    assert result.exit_code == 1


def test_check_invalid_info() -> None:
    config_path = os.path.join(
        os.path.dirname(__file__), "invalid-schemas/invalid-info"
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["check", config_path])
    assert (
        f"In {config_path}/info.yaml we detected the following violation:"
        in result.output
    )
    assert result.exit_code == 1


def test_check_invalid_environment() -> None:
    config_path = os.path.join(
        os.path.dirname(__file__), "invalid-schemas/invalid-environment"
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["check", config_path])
    assert (
        f"In {config_path}/development.yaml we detected the following violation:"
        in result.output
    )

    assert result.exit_code == 1
