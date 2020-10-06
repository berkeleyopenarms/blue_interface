import pytest


def test_no_rosbridge():
    """Make sure that importing BlueInterface and instantiating it results in the correct
    error when no rosbridge server is running.

    (( assumes that no rosbridge server is running at localhost:444 ))
    """

    from blue_interface import BlueInterface

    with pytest.raises(ConnectionRefusedError):
        BlueInterface(side="left", ip="127.0.0.1", port=444)
