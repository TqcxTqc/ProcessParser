import subprocess
from datetime import datetime
from collections import defaultdict


def getProcessData():
    """Call in terminal command ps aux to get process list"""
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, universal_newlines=True).stdout.readlines()
    nfields = len(process[0].split()) - 1
    retval = []
    for row in process[1:]:
        retval.append(row.split(None, nfields))
    return retval


def get_count_of_process(lines):
    """Get count of processes"""
    return len(lines)


def get_users_from_process(lines):
    """Taking all users which are in the process"""
    users = []
    for line in lines:
        if line[0] not in users:
            users.append(line[0])

    return users


def user_process_count(lines):
    """Taking how much process have each user from the process"""
    process_by_user = defaultdict(int)
    for line in lines:
        user_item = line[0]
        process_by_user[user_item] += 1
    return process_by_user


def calculate_memory_and_cpu_usage(lines):
    """Counting how much CPU and MEMORY is using"""
    memory_result = 0
    cpu_result = 0
    for line in lines:
        memory_number = float(line[3])
        cpu_number = float(line[2])
        memory_result += memory_number
        cpu_result += cpu_number

    return (round(memory_result, 2), round(cpu_result, 2))


def process_who_eat_cpu_and_memory(lines):
    """Taking name of drained CPU and MEMORY process"""
    highest_memory = 0
    highest_cpu_load = 0
    highest_memory_name = ""
    highest_cpu_load_name = ""
    for line in lines:
        if float(line[3]) > highest_memory:
            highest_memory = float(line[3])
            highest_memory_name = line[10][:23]
        elif float(line[2]) > highest_cpu_load:
            highest_cpu_load = float(line[2])
            highest_cpu_load_name = line[10][:23]

    return (highest_memory_name, highest_cpu_load_name)


data = getProcessData()
cpu_and_memory = calculate_memory_and_cpu_usage(data)
process_count = get_count_of_process(data)
users = get_users_from_process(data)
user_processes_count = user_process_count(data)
name_of_highest_cpu_and_memory = process_who_eat_cpu_and_memory(data)

report = [
    f"USERS IN PROCESS: {users}\n",
    f"PROCESSES RUNNING: {process_count}\n",
    f"PROCESSES BY USERS: {dict(user_processes_count)}\n",
    f"TOTAL MEMORY USED: {cpu_and_memory[0]}\n",
    f"TOTAL CPU USED: {cpu_and_memory[1]}\n",
    f"PROCESS WITH MOST OF MEMORY USAGE: {name_of_highest_cpu_and_memory[0]}\n",
    f"PROCESS WITH MOST OF CPU USAGE: {name_of_highest_cpu_and_memory[1]}",

]

with open(f"{datetime.today():%d-%m-%Y-%H:%M}-scan.txt", 'w') as fp:
    fp.writelines(report)
