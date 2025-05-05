

def test_public_interface():
    """Test the public interface of the module."""
    import importlib
    import inspect

    module = importlib.import_module("promptworks")
    public_interface = inspect.getmembers(module)
    assert len(public_interface) > 0

    names = [name for name, _ in public_interface]

    assert "Prompt" in names
    assert "interfaces" in names
    assert "LocalFileComponent" in names
    assert "TimeComponent" in names
    assert "PlaintextComponent" in names
