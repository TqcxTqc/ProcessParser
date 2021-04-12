import subprocess
import pprint
import json
from collections import defaultdict, Counter

# REPORT keys
USER = "users"
USERS_PROCESS_COUNT = "users_process_count"
PROCESS_COUNT = "process_count"
MEMORY_USAGE = "memory_usage"
CPU_USAGE = "cpu_usage"
EAT_MOST_MEMORY = "eat_most_memory"
EAT_MOST_CPU = "eat_most_cpu"

REPORT = {
    USER: list(),
    USERS_PROCESS_COUNT: defaultdict(int),
    PROCESS_COUNT: 0,
    MEMORY_USAGE: 0,
    CPU_USAGE: 0,
    EAT_MOST_CPU: "",
    EAT_MOST_MEMORY: ""
}


def getProcessData():
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, universal_newlines=True).stdout.readlines()
    nfields = len(process[0].split()) - 1
    retval = []
    for row in process[1:]:
        retval.append(row.split(None, nfields))
    return retval


def get_count_of_process(lines):
    return len(lines)


def get_users_from_process(lines):
    users = []
    for line in lines:
        if line[0] not in users:
            users.append(line[0])

    return users


def calculate_all_memory_usage(lines):
    result = 0
    for line in lines:
        number = float(line[2])

        result += number

    return round(result, 2)


def user_process_count(lines):
    process_by_user = defaultdict(int)
    for line in lines:
        user_item = line[0]
        process_by_user[user_item] += 1
    return process_by_user


data = getProcessData()

calculated_memory_usage = calculate_all_memory_usage(data)
process_count = get_count_of_process(data)
users = get_users_from_process(data)
user_processes_count = user_process_count(data)

REPORT[USER] = users
REPORT[PROCESS_COUNT] = process_count
REPORT[USERS_PROCESS_COUNT] = user_processes_count

pprint.pprint(REPORT)

# with open('process_statistics.json', 'w') as fp:
#     json.dump(REPORT, fp, indent=3)
