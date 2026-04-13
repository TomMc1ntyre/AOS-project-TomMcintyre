"""
System information commands for pysh.

Uses psutil to display system statistics.
"""

import os
import sys
import time

try:
    import psutil
except ImportError:
    psutil = None


def format_bytes(bytes_val):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}PB"


def builtin_sysinfo(args):
    """
    Display system information.
    Usage: sysinfo [--sort cpu|memory]
    
    Shows memory, swap, CPU usage, and top processes.
    Refreshes every 2 seconds until interrupted.
    """
    if psutil is None:
        print("sysinfo: psutil not installed (run: pip install psutil)", file=sys.stderr)
        return 1

    sort_by = 'cpu'
    for arg in args:
        if arg == '--sort' and len(args) > 1:
            sort_by = args[args.index(arg) + 1]
            if sort_by not in ('cpu', 'memory'):
                print("sysinfo: invalid sort option (use 'cpu' or 'memory')", file=sys.stderr)
                return 1

    try:
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            
            print("=" * 60)
            print("SYSTEM INFORMATION")
            print("=" * 60)
            print()

            mem = psutil.virtual_memory()
            print("MEMORY")
            print(f"  Total:     {format_bytes(mem.total)}")
            print(f"  Used:      {format_bytes(mem.used)}")
            print(f"  Available: {format_bytes(mem.available)}")
            print(f"  Usage:     {mem.percent}%")
            print()

            swap = psutil.swap_memory()
            print("SWAP")
            print(f"  Total:     {format_bytes(swap.total)}")
            print(f"  Used:      {format_bytes(swap.used)}")
            print(f"  Free:      {format_bytes(swap.free)}")
            print(f"  Usage:     {swap.percent}%")
            print()

            cpu_percent = psutil.cpu_percent(interval=0.1)
            print(f"CPU USAGE (overall): {cpu_percent}%")
            print()

            per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
            print("PER-CPU USAGE:")
            for i, pct in enumerate(per_cpu):
                print(f"  CPU {i}: {pct}%")
            print()

            print(f"TOP 10 PROCESSES (sorted by {sort_by.upper()})")
            print("-" * 60)
            print(f"{'PID':<8} {'USER':<15} {'CPU%':<8} {'MEM%':<8} {'NAME':<20}")
            print("-" * 60)

            processes = []
            for p in psutil.process_iter(['pid', 'username', 'cpu_percent', 'memory_percent', 'name']):
                try:
                    processes.append(p.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            if sort_by == 'cpu':
                processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            else:
                processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)

            for proc in processes[:10]:
                pid = proc.get('pid', 'N/A')
                user = proc.get('username', 'N/A')[:14]
                cpu = proc.get('cpu_percent') or 0
                mem = proc.get('memory_percent') or 0
                name = proc.get('name', 'N/A')[:19]
                print(f"{pid:<8} {user:<15} {cpu:<8.1f} {mem:<8.1f} {name:<20}")

            print()
            print("Press Ctrl+C to return to shell...")

            time.sleep(2)

    except KeyboardInterrupt:
        pass

    return 0