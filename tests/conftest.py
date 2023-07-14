import os

import pytest
import landingzone_organization

from landingzone_organization import Organization, OrganizationUnit
from aws_securityhub_suppression import Workload, Account
from aws_securityhub_suppression.finding import Finding
from aws_securityhub_suppression.suppression import Suppression


@pytest.fixture
def config_path() -> str:
    return os.path.join(os.path.dirname(__file__), "workloads")


@pytest.fixture
def template() -> str:
    return os.path.join(os.path.dirname(__file__), "templates", "test-template.md")


@pytest.fixture
def workload() -> Workload:
    return Workload(
        "my-workload",
        [
            Account(
                name="binxio-my-workload-development",
                account_id="000000000000",
                suppressions=[
                    Suppression(
                        name="My Suppression",
                        reason="Good reason",
                        findings=[
                            Finding(
                                name="my-resource",
                                finding_arn="arn:aws:securityhub:eu-west-1:000000000000:subscription/my-generator/finding/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                            )
                        ],
                    )
                ],
            ),
            Account(
                name="binxio-my-workload-testing",
                account_id="000000000000",
                suppressions=[],
            ),
            Account(
                name="binxio-my-workload-acceptance",
                account_id="000000000000",
                suppressions=[],
            ),
            Account(
                name="binxio-my-workload-production",
                account_id="000000000000",
                suppressions=[],
            ),
        ],
    )


@pytest.fixture
def organization() -> Organization:
    return Organization(
        "r-1234",
        landingzone_organization.OrganizationUnit(
            id="r-1234",
            name="Root",
            accounts=[landingzone_organization.Account("root-account", "000000000000")],
            units=[
                OrganizationUnit(
                    id="ou-1",
                    name="Core",
                    accounts=[
                        landingzone_organization.Account(
                            "connectivity", "111111111111"
                        ),
                    ],
                ),
                OrganizationUnit(
                    id="ou-2",
                    name="Security",
                    accounts=[
                        landingzone_organization.Account("audit", "111111111112"),
                    ],
                ),
                OrganizationUnit(
                    id="ou-3",
                    name="Workloads",
                    accounts=[],
                    units=[
                        OrganizationUnit(
                            id="ou-4",
                            name="Development",
                            accounts=[
                                landingzone_organization.Account(
                                    "binxio-example-workload-development",
                                    "111122223333",
                                ),
                                landingzone_organization.Account(
                                    "binxio-other-workload-development",
                                    "111111111111",
                                ),
                            ],
                        ),
                        OrganizationUnit(
                            id="ou-5",
                            name="Testing",
                            accounts=[
                                landingzone_organization.Account(
                                    "binxio-example-workload-testing", "222233334444"
                                ),
                            ],
                        ),
                        OrganizationUnit(
                            id="ou-6",
                            name="Acceptance",
                            accounts=[
                                landingzone_organization.Account(
                                    "binxio-example-workload-acceptance", "333344445555"
                                ),
                            ],
                        ),
                        OrganizationUnit(
                            id="ou-7",
                            name="Production",
                            accounts=[
                                landingzone_organization.Account(
                                    "binxio-example-workload-production", "444455556666"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )
