"""
download command for pysh.

Downloads files from a list of URLs using a producer-consumer pattern.
A producer reads URLs from a file into a shared queue; worker threads
consume the queue and save files to a local downloads/ directory.
"""

import os
import queue
import sys
import threading
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# Module-level shared state so --status can report across calls
_queue = queue.Queue()
_lock = threading.Lock()
_completed = 0
_active_workers = 0


def _worker(downloads_dir):
    """Pull URLs from the queue and download each one."""
    global _completed, _active_workers

    with _lock:
        _active_workers += 1

    while True:
        try:
            url = _queue.get(timeout=2)
        except queue.Empty:
            break

        filename = url.rstrip('/').split('/')[-1].split('?')[0] or 'download'
        dest = downloads_dir / filename

        try:
            r = requests.get(url, timeout=30, stream=True)
            r.raise_for_status()
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"\ndownload: saved {filename}")
            with _lock:
                _completed += 1
        except requests.exceptions.Timeout:
            print(f"\ndownload: timeout: {url}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"\ndownload: failed {url}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"\ndownload: error saving {filename}: {e}", file=sys.stderr)
        finally:
            _queue.task_done()

    with _lock:
        _active_workers -= 1


def builtin_download(args):
    """
    Download files from a URL list using worker threads.
    Usage:
      download <file>        Download URLs from file using 3 workers
      download <file> -w N  Download using N workers
      download --status      Show queue size, active workers, completed count
    """
    global _completed

    if requests is None:
        print("download: requests not installed (run: pip install requests)", file=sys.stderr)
        return 1

    if not args:
        print("Usage: download <file> [-w N] | download --status", file=sys.stderr)
        return 1

    if args[0] == '--status':
        with _lock:
            queued = _queue.qsize()
            active = _active_workers
            done = _completed
        print(f"Queued:    {queued}")
        print(f"Active:    {active}")
        print(f"Completed: {done}")
        return 0

    url_file = args[0]
    num_workers = 3

    i = 1
    while i < len(args):
        if args[i] == '-w' and i + 1 < len(args):
            try:
                num_workers = int(args[i + 1])
            except ValueError:
                print(f"download: invalid worker count: {args[i + 1]}", file=sys.stderr)
                return 1
            i += 2
        else:
            i += 1

    try:
        with open(url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"download: {url_file}: No such file or directory", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"download: {url_file}: {e}", file=sys.stderr)
        return 1

    if not urls:
        print("download: no URLs found in file", file=sys.stderr)
        return 1

    downloads_dir = Path(os.getcwd()) / 'downloads'
    downloads_dir.mkdir(exist_ok=True)

    for url in urls:
        _queue.put(url)

    print(f"download: queued {len(urls)} URLs, starting {num_workers} workers")

    for _ in range(num_workers):
        t = threading.Thread(target=_worker, args=(downloads_dir,), daemon=True)
        t.start()

    return 0
