from pawabot import cli


def test_main():
    assert cli.main([]) == 0