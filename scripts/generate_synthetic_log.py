#!/usr/bin/env python3
import csv, random, datetime, argparse

def generate(path, rows=1000, days=1):
    headers = ["timestamp","src_ip","user","event_id","status"]
    start = datetime.datetime.now() - datetime.timedelta(days=days)
    users = ["Administrator","jsmith","ayounes","svc-backup"]
    ips = ["192.168.1.50","192.168.1.77","10.0.0.4","172.16.0.10","203.0.113.5"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for i in range(rows):
            t = start + datetime.timedelta(seconds=i*60)
            user = random.choice(users)
            ip = random.choice(ips)
            if 500 <= i <= 580:
                ip = "198.51.100.66"
                user = "Administrator"
                status = "FAIL" if random.random() < 0.9 else "SUCCESS"
                event_id = 4625 if status == "FAIL" else 4624
            else:
                status = "FAIL" if random.random() < 0.2 else "SUCCESS"
                event_id = 4625 if status == "FAIL" else 4624
            w.writerow([t.isoformat(), ip, user, event_id, status])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="data/synthetic.csv")
    ap.add_argument("--rows", type=int, default=1500)
    ap.add_argument("--days", type=int, default=1)
    args = ap.parse_args()
    generate(args.path, args.rows, args.days)
