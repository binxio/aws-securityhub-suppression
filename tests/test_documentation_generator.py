from unittest.mock import call, patch, mock_open

from aws_securityhub_suppression import Workload
from aws_securityhub_suppression.documentation_generator import DocumentationGenerator

expected_documentation = """# my-workload suppression's

The my-workload workload has the following accounts:

**Account Name** | **Account ID**
-----------------|---------------
binxio-my-workload-development | 000000000000
binxio-my-workload-testing | 000000000000
binxio-my-workload-acceptance | 000000000000
binxio-my-workload-production | 000000000000


## binxio-my-workload-development

The binxio-my-workload-development has the following suppressions registered:

**Name** | **Findings** | **Reason**
---------|--------------|---------------
My Suppression | <ul><li>arn:aws:securityhub:eu-west-1:000000000000:subscription/finding/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX</li></ul> | Good reason


## binxio-my-workload-testing

There are no suppression's registered under the binxio-my-workload-testing account.

## binxio-my-workload-acceptance

There are no suppression's registered under the binxio-my-workload-acceptance account.

## binxio-my-workload-production

There are no suppression's registered under the binxio-my-workload-production account."""


@patch(
    "aws_securityhub_suppression.documentation_generator.open", new_callable=mock_open
)
def test_generate_new_workload(
    mock_file, template: str, config_path: str, workload: Workload
) -> None:
    generator = DocumentationGenerator(
        template_path=template, config_path=config_path, workload=workload
    )
    generator.render()

    assert mock_file.call_args_list == [
        call(f"{config_path}/my-workload/README.md", "w"),
    ]
    mock_file.return_value.write.assert_called_with(expected_documentation)
