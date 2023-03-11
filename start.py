import subprocess


subprocess.run(['alembic', 'upgrade', 'head'])
subprocess.run(['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '10000'])