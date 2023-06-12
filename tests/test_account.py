from aws_securityhub_suppression import Account


def test_account() -> None:
    assert Account.from_dict({}) is None

    account = Account.from_dict(
        {"Name": "my-name", "AccountId": "123456781234", "Suppressions": []}
    )
    assert isinstance(account, Account) is True
    assert account.name == "my-name"
    assert account.account_id == "123456781234"
    assert account.suppressions == []
