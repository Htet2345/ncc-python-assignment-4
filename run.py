"""Start the app in one terminal and open the browser when it is ready."""
import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
from urllib.error import URLError
from urllib.request import urlopen
import webbrowser


def open_when_ready(url):
    for _ in range(100):
        try:
            with urlopen(url, timeout=0.5) as response:
                if response.status == 200:
                    webbrowser.open(url)
                    return
        except (URLError, OSError):
            time.sleep(0.2)
    print(f'Open {url} in your browser once the server is ready.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Port must be between 1 and 65535.')
    os.chdir(Path(__file__).resolve().parent)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        import django
        from django.core.management import call_command, execute_from_command_line
    except ImportError:
        print('Run setup.ps1 first to install Django.')
        return 1
    with socket.socket() as check:
        if check.connect_ex(('127.0.0.1', args.port)) == 0:
            print(f'Port {args.port} is already in use. Press Ctrl+C in the existing server terminal, then run again.')
            return 1
    django.setup()
    call_command('migrate', interactive=False, verbosity=0)
    url = f'http://127.0.0.1:{args.port}/'
    print(f'Starting Student CRUD at {url}', flush=True)
    print('Keep this terminal open. Press Ctrl+C to stop.', flush=True)
    if not args.no_browser:
        threading.Thread(target=open_when_ready, args=(url,), daemon=True).start()
    execute_from_command_line(['manage.py', 'runserver', f'127.0.0.1:{args.port}', '--noreload'])
    return 0


if __name__ == '__main__':
    project_python = Path(__file__).resolve().parent / '.venv' / 'Scripts' / 'python.exe'
    if not project_python.is_file():
        print('Run setup.ps1 first to set up the app.')
        raise SystemExit(1)
    if Path(sys.executable).resolve() != project_python.resolve():
        # The Run button may use system Python. Start the project interpreter.
        try:
            result = subprocess.run([str(project_python), str(Path(__file__).resolve()), *sys.argv[1:]])
            raise SystemExit(result.returncode)
        except KeyboardInterrupt:
            raise SystemExit(130)
    raise SystemExit(main())
