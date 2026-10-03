from pathlib import Path


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    ruta = Path(__file__).resolve().parents[1] / "coverage.xml"
    if not ruta.is_file():
        return
    texto = ruta.read_text(encoding="utf-8")
    ajustado = texto.replace("<source>app</source>", "<source>backend/app</source>", 1)
    if ajustado != texto:
        ruta.write_text(ajustado, encoding="utf-8")
