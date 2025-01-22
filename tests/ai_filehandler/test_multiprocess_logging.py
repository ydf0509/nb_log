import multiprocessing
import time
import sys
import os
from pathlib import Path

# Add parent directory to Python path to make imports work
sys.path.append(str(Path(__file__).parent))

from custom_file_handler_demo import CustomRotatingFileHandler
import logging


def worker_process(process_id):
    # Create logger for this process
    logger = logging.getLogger(f"process_{process_id}")
    logger.setLevel(logging.DEBUG)

    # Create and configure file handler
    file_handler = CustomRotatingFileHandler(
        filename="/pythonlogs/multiprocess_test2.log",
        max_bytes=1024*10240,  # Small size to trigger rotation frequently
        backup_count=5,
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - PID:%(process)d - %(message)s',
        "%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(file_handler)

    # Write some logs
    for i in range(1000000):
        logger.info(f"Process {process_id} - Message {i}")
        # time.sleep(0.01)  # Small delay to simulate work

    # file_handler.close()


def main():
    # Create multiple processes
    processes = []
    for i in range(5):  # Start 5 processes
        p = multiprocessing.Process(target=worker_process, args=(i,))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(f"Time taken: {t2 - t1} seconds") 