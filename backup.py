import os
import tarfile
import subprocess
import json
from datetime import datetime
from time import perf_counter

# ANSI color codes
# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

LOG_FILE = "log.txt"

def log(message):
    # Печать с цветами
    print(message)
    # Запись без цветовых кодов
    plain_message = message.replace(RED, '').replace(GREEN, '').replace(YELLOW, '').replace(RESET, '')
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(plain_message + "\n")

# Load configuration from JSON file
def load_config(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        return json.load(f)

# Load config
config = load_config('config.json')

backup_dir = config['backup_dir']
directories = config.get('directories', [])
exclude_dirs = config.get('exclude_dirs', [])
compose_links_dir = config.get('compose_links_dir')
stop_containers = config.get('stop_containers', False)
restart_containers = config.get('restart_containers', False)

# Clear log file at start
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"Backup started at {datetime.now().isoformat()}\n")

# Ensure backup_dir exists
os.makedirs(backup_dir, exist_ok=True)

timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"docker_backup_{timestamp}.tar.gz")

# Function to stop Docker containers
def stop_all_containers():
    log(f"{RED}Stopping all running Docker containers...{RESET}")
    subprocess.run(
        "docker stop $(docker ps -a --format '{{.Names}}')", shell=True
    )

# Function to restart Docker containers from symlinked compose files
def restart_containers_from_symlinks(links_dir):
    if not os.path.exists(links_dir):
        log(f"{YELLOW}Warning: Links directory does not exist:{RESET} {links_dir}")
        return

    symlinks = [f for f in os.listdir(links_dir) if os.path.islink(os.path.join(links_dir, f))]

    if not symlinks:
        log(f"{YELLOW}Warning: No symbolic links found in:{RESET} {links_dir}")
        return

    for filename in symlinks:
        link_path = os.path.join(links_dir, filename)

        # Resolve real path
        real_path = os.path.realpath(link_path)

        if not os.path.exists(real_path):
            log(f"{YELLOW}Warning: Target of symlink does not exist:{RESET} {real_path}")
            continue

        if not os.path.basename(real_path) in ["docker-compose.yml", "docker-compose.yaml"]:
            log(f"{YELLOW}Warning: Target is not a docker-compose file:{RESET} {real_path}")
            continue

        # Use the parent directory of docker-compose file
        compose_dir = os.path.dirname(real_path)

        log(f"{GREEN}Restarting containers in:{RESET} {compose_dir}")

        result = subprocess.run(
            "docker compose up -d",
            shell=True,
            cwd=compose_dir
        )

        if result.returncode != 0:
            log(f"{RED}Error restarting containers in:{RESET} {compose_dir}")
        else:
            log(f"{GREEN}Containers restarted successfully in:{RESET} {compose_dir}")

# Optionally stop containers
if stop_containers:
    stop_all_containers()

# Create a new tar archive and add directories to it
with tarfile.open(backup_file, "w:gz") as tar:
    log(f"{RED}Creating new backup archive:{RESET} {backup_file}")
    for dir_path in directories:
        if dir_path in exclude_dirs:
            log(f"{GREEN}Skipping excluded directory:{RESET} {dir_path}")
            continue

        if not os.path.exists(dir_path):
            log(f"{YELLOW}Warning: Directory does not exist and will be skipped:{RESET} {dir_path}")
            continue

        start_time = perf_counter()
        log(f"{RED}Adding directory to archive:{RESET} {dir_path}")

        tar.add(dir_path, arcname=os.path.basename(dir_path))

        end_time = perf_counter()
        elapsed_time = end_time - start_time
        if elapsed_time >= 60:
            minutes, seconds = divmod(elapsed_time, 60)
            log(f"{GREEN}Backup completed for:{RESET} {dir_path} in {GREEN}{int(minutes)} minute(s) and {seconds:.2f} second(s){RESET}")
        else:
            log(f"{GREEN}Backup completed for:{RESET} {dir_path} in {GREEN}{elapsed_time:.2f} seconds{RESET}")

log(f"{GREEN}Backup completed successfully:{RESET} {backup_file}")

# Optionally restart containers
if restart_containers and compose_links_dir:
    restart_containers_from_symlinks(compose_links_dir)

log(f"{GREEN}Script finished at {datetime.now().isoformat()}.{RESET}")
