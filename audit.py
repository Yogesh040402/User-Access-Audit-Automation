import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
USER_FILE = os.path.join(BASE_DIR, "users.csv")
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")
INACTIVE_DAYS = 180

with open(USER_FILE,"r") as file:
    reader = csv.DictReader(file)
    users = list(reader)

inactive_users = []
expired_users = []
username_count = {}

today = datetime.today()

for user in users:

    username = user['username']
    username_count[username] = username_count.get(username, 0) + 1

    last_login_str = user['last_login']
    last_login_date = datetime.strptime(last_login_str, '%Y-%m-%d')

    days_inactive = (today - last_login_date).days

    if days_inactive > INACTIVE_DAYS:
        inactive_users.append(user['username'])

    expiry_str = user["access_expiry"]
    expiry_date = datetime.strptime(expiry_str,'%Y-%m-%d')

    if expiry_date < today:
        expired_users.append(user['username'])

duplicate_users = []
for username, count in username_count.items():
    if count > 1:
        duplicate_users.append(username)

with open(REPORT_FILE,"w") as report:
    report.write("User Access Audit Report\n")
    report.write("========================\n")
    report.write(f"Report Date: {today.date()}\n\n")
    report.write("Inactive_users (> 180 days):\n")
    if inactive_users:
        for u in inactive_users:
            report.write(f"- {u}\n")
    else:
        report.write("None\n")
    report.write("\n")

    report.write("Expired Access Users:\n")
    if expired_users:
        for u in expired_users:
            report.write(f"- {u}\n")

    else:
        report.write("None\n")
    report.write("\n")

    if duplicate_users:
        report.write("Duplicate Usernames:\n")
        for u in duplicate_users:
            report.write(f"- {u}\n")

    else:
        report.write("None\n")


print("Audit report generated:", REPORT_FILE)
print("Audit Completed sucessfully.")