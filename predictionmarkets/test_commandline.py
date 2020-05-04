import subprocess

def test_invocation():
    proc = subprocess.run(["bash", "-c", "timeout 1 python -m predictionmarkets.server.plain_html"])  # if changed, update ctrl-f "invocation-cmd"
    assert proc.returncode == 124
