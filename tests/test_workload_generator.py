from unittest.mock import mock_open, patch, call

from aws_securityhub_suppression import Workload
from aws_securityhub_suppression.workload_generator import WorkloadGenerator


@patch("os.path.isfile")
@patch("os.path.isdir")
@patch("os.mkdir")
@patch("builtins.open", new_callable=mock_open)
def test_generate_new_workload(
    mock_file, mock_mkdir, mock_isdir, mock_isfile, config_path: str, workload: Workload
) -> None:
    mock_isdir.return_value = False
    mock_isfile.return_value = False
    mock_file.return_value.write.return_value = None
    generator = WorkloadGenerator(config_path=config_path, workload=workload)
    generator.execute()

    assert mock_mkdir.called is True

    assert mock_file.call_args_list == [
        call(f"{config_path}/my-workload/info.yaml", "w"),
        call(f"{config_path}/my-workload/development.yaml", "w"),
        call(f"{config_path}/my-workload/testing.yaml", "w"),
        call(f"{config_path}/my-workload/acceptance.yaml", "w"),
        call(f"{config_path}/my-workload/production.yaml", "w"),
    ]


@patch("os.path.isfile")
@patch("os.path.isdir")
@patch("os.mkdir")
@patch("builtins.open", new_callable=mock_open)
def test_generate_existing_workload(
    mock_file, mock_mkdir, mock_isdir, mock_isfile, config_path: str, workload: Workload
) -> None:
    mock_isdir.return_value = True
    mock_isfile.return_value = True
    mock_file.return_value.write.return_value = None

    generator = WorkloadGenerator(config_path=config_path, workload=workload)

    with patch("yaml.safe_load") as mock_load:
        mock_load.return_value = {"Name": "my-workload"}
        generator.execute()

    assert mock_mkdir.called is False

    assert mock_file().write.call_args_list == [
        call("Name"),
        call(":"),
        call(" "),
        call("my-workload"),
        call("\n"),
    ]
    assert mock_file.call_args_list == [
        call(f"{config_path}/my-workload/info.yaml", "r"),
        call(f"{config_path}/my-workload/info.yaml", "w"),
        call(),
    ]


@patch("os.path.isfile")
@patch("os.path.isdir")
@patch("os.mkdir")
@patch("builtins.open", new_callable=mock_open)
def test_generate_existing_workload_new_name(
    mock_file, mock_mkdir, mock_isdir, mock_isfile, config_path: str, workload: Workload
) -> None:
    mock_isdir.return_value = True
    mock_isfile.return_value = True
    mock_file.return_value.write.return_value = None

    generator = WorkloadGenerator(config_path=config_path, workload=workload)

    with patch("yaml.safe_load") as mock_load:
        mock_load.return_value = {"Name": "old-workload"}
        generator.execute()

    assert mock_mkdir.called is False

    assert mock_file().write.call_args_list == [
        call("Name"),
        call(":"),
        call(" "),
        call("my-workload"),
        call("\n"),
    ]
    assert mock_file.call_args_list == [
        call(f"{config_path}/my-workload/info.yaml", "r"),
        call(f"{config_path}/my-workload/info.yaml", "w"),
        call(),
    ]
