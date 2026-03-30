from tts_util.cli import main
import tts_util.cli as cli_mod


def test_cli_default_invokes_start(monkeypatch):
    called = []

    def fake_start(*, use_gui=False):
        called.append(use_gui)

    monkeypatch.setattr(cli_mod, "start", fake_start)
    result = main([])
    assert result == 0
    assert called == [False]


def test_cli_up_and_alias_start_invoke_service(monkeypatch):
    called = []

    def fake_start(*, use_gui=False):
        called.append(use_gui)

    monkeypatch.setattr(cli_mod, "start", fake_start)
    assert main(["up"]) == 0
    assert main(["start"]) == 0
    assert called == [False, False]


def test_cli_gui_flag_invokes_gui_controller(monkeypatch):
    called = []

    def fake_start(*, use_gui=False):
        called.append(use_gui)

    monkeypatch.setattr(cli_mod, "start", fake_start)
    assert main(["--gui"]) == 0
    assert called == [True]
