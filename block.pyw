import os
import time
from datetime import datetime
import json
import logging.config


def blocker_logger(text):
    """ Logger for system info """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger_handler = logging.FileHandler('logfile.log')
    logger_handler.setLevel(logging.INFO)
    logger_formatter = logging.Formatter('%(asctime)s - %(message)s')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    logger.info(text)


def hosts_file_path():
    """ Checking OS type and select host patch """
    if os.name == 'nt':
        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    elif os.name == 'posix':
        hosts_path = '/etc/hosts'
    return hosts_path


def set_block_times(file, hours, minutes):
    """ Set a block time """
    with open(file) as f_obj:
        pop_data = json.load(f_obj)
    for pop_dict in pop_data:
        b_hours = pop_dict[hours]
        b_minutes = pop_dict[minutes]
        block_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, b_hours, b_minutes)
    return block_time


def block_access(host_path, redirect_url, blocked_sites):
    """ Block accesses to sites"""
    try:
        with open(host_path, 'r+') as f:
            hosts_src = f.read()
            for site_url in blocked_sites:
                if site_url in hosts_src:
                    pass
                else:
                    f.write(f'{redirect_url} {site_url}\n')
    except PermissionError:
        blocker_logger("ERROR: Not running as administrator")
        exit()            


def unblock_access(host_path, blocked_sites):
    """Unblock access to sites"""
    try:
        with open(host_path, 'r+') as f:
            hosts_src = f.readlines()
            f.seek(0)
            for line in hosts_src:
                if not any(site_url in line for site_url in blocked_sites):
                    f.write(line)
            f.truncate()
    except PermissionError:
        blocker_logger("ERROR: Not running as administrator")
        exit()            


def blocklist(settings_file):
    """ Load sites from file """
    with open(settings_file) as f_obj:
        pop_data = json.load(f_obj)
        for pop_dict in pop_data:
            file = pop_dict["blocklist"]
    block = []
    with open(file, 'r') as f:
        lines = f.readlines()
        if not lines:
            pass
        else:
            for line in lines:
                block.append(line)
    return block


def main():
    """ Run a program"""
    hosts_path = hosts_file_path()
    settings = 'settings.json'
    redirect_url = '127.0.0.1'
    blocked_sites = blocklist(settings)
    start_time = set_block_times(settings, "start_hours", "start_minutes")
    stop_time = set_block_times(settings, "stop_hours", "stop_minutes")
    blocker_logger("INFO: Time set from {} to {}" .format(start_time, stop_time))
    while True:
        if start_time < datetime.now() < stop_time:
            block_access(hosts_path, redirect_url, blocked_sites)
        else:
            unblock_access(hosts_path, blocked_sites)
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        blocker_logger('WARNING: Stopped by user')
        exit()
