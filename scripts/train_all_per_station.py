#!/usr/bin/env python3
"""Train a per-station model for every station in the DB.

Usage:
  PYTHONPATH="." python scripts/train_all_per_station.py --workers 2 --epochs 30 --retries 1

Features:
- Runs per-station training in parallel workers
- Saves per-station stdout/stderr into logs/station_{id}.log
- Writes a CSV summary with status, exit code, duration
- Supports retries on failures
"""

import argparse
import concurrent.futures
import subprocess
import sys
import time
import os
import csv
from pathlib import Path

from src.db import get_stations

LOG_DIR = Path('logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_CSV = Path('logs/per_station_training_summary.csv')


def run_train_for_station(station_id, python_exe, extra_args, timeout=None, retries=0):
    attempt = 0
    start_time = time.time()
    last_output = ""
    rc = 1
    while attempt <= retries:
        attempt += 1
        cmd = [python_exe, "src/train.py", "--mode", "per_station", "--station", str(station_id)] + extra_args
        log_path = LOG_DIR / f"station_{station_id}.log"
        t0 = time.time()
        try:
            print(f"[Station {station_id}] Starting attempt {attempt}: {' '.join(cmd)}")
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
            last_output = res.stdout
            rc = res.returncode
            duration = time.time() - t0
            with open(log_path, 'a') as f:
                f.write(f"\n--- Attempt {attempt} (rc={rc}) ---\n")
                f.write(last_output)
        except subprocess.TimeoutExpired as e:
            last_output = f"[Timeout after {timeout}s]\n"
            rc = -1
            duration = time.time() - t0
            with open(log_path, 'a') as f:
                f.write(f"\n--- Attempt {attempt} (timeout) ---\n")
                f.write(str(e))
        except Exception as e:
            last_output = str(e)
            rc = -2
            duration = time.time() - t0
            with open(log_path, 'a') as f:
                f.write(f"\n--- Attempt {attempt} (exception) ---\n")
                f.write(last_output)

        if rc == 0:
            break
        else:
            print(f"[Station {station_id}] Attempt {attempt} failed (rc={rc}).")
            if attempt <= retries:
                print(f"[Station {station_id}] Retrying...")

    total_duration = time.time() - start_time
    status = 'ok' if rc == 0 else 'failed'
    return {
        'station_id': station_id,
        'status': status,
        'return_code': rc,
        'attempts': attempt,
        'duration_s': round(total_duration, 2),
        'log_path': str(log_path),
        'output_snippet': last_output[:400]
    }


def main(workers, start, end, epochs, batch_size, lr, retries, timeout, extra_flags):
    stations = get_stations()
    station_ids = [s['id'] for s in stations if (start is None or s['id'] >= start) and (end is None or s['id'] <= end)]

    extra_args = []
    if epochs is not None:
        extra_args += ["--epochs", str(epochs)]
    if batch_size is not None:
        extra_args += ["--batch-size", str(batch_size)]
    if lr is not None:
        extra_args += ["--lr", str(lr)]
    extra_args += extra_flags

    python_exe = sys.executable

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(run_train_for_station, sid, python_exe, extra_args, timeout, retries): sid for sid in station_ids}
        for fut in concurrent.futures.as_completed(futures):
            sid = futures[fut]
            try:
                res = fut.result()
                results.append(res)
                print(f"[Station {sid}] Completed: {res['status']} (rc={res['return_code']}, attempts={res['attempts']})")
            except Exception as e:
                print(f"[Station {sid}] Unexpected error: {e}")
                results.append({'station_id': sid, 'status': 'error', 'return_code': -9, 'attempts': 0, 'duration_s': 0, 'log_path': '', 'output_snippet': str(e)})

    # Write CSV summary
    with open(SUMMARY_CSV, 'w', newline='') as csvfile:
        fieldnames = ['station_id', 'status', 'return_code', 'attempts', 'duration_s', 'log_path', 'output_snippet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, '') for k in fieldnames})

    successful = sum(1 for r in results if r['status'] == 'ok')
    print(f"\nSummary: {successful}/{len(results)} stations trained successfully. CSV: {SUMMARY_CSV}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train per-station models for all stations')
    parser.add_argument('--workers', type=int, default=1, help='Number of parallel workers')
    parser.add_argument('--start', type=int, help='Start station id (inclusive)')
    parser.add_argument('--end', type=int, help='End station id (inclusive)')
    parser.add_argument('--epochs', type=int, help='Override epochs for per-station training')
    parser.add_argument('--batch-size', type=int, help='Override batch size for per-station training')
    parser.add_argument('--lr', type=float, help='Override learning rate for per-station training')
    parser.add_argument('--retries', type=int, default=0, help='Number of retries on failure')
    parser.add_argument('--timeout', type=int, help='Per-job timeout in seconds')
    parser.add_argument('--log-dir', type=str, default=str(LOG_DIR), help='Directory to store logs')
    parser.add_argument('extra', nargs=argparse.REMAINDER, help='Extra args forwarded to per-station train')

    args = parser.parse_args()

    # Ensure log dir
    if args.log_dir and args.log_dir != str(LOG_DIR):
        LOG_DIR = Path(args.log_dir)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        SUMMARY_CSV = LOG_DIR / 'per_station_training_summary.csv'

    main(args.workers, args.start, args.end, args.epochs, args.batch_size, args.lr, args.retries, args.timeout, args.extra)