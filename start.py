import subprocess


subprocess.run(['alembic', 'upgrade', 'head'])
subprocess.run(['uvicorn', 'app.main:app'])
