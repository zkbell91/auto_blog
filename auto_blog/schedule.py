import schedule
import time

def schedule_job(job_func, time_str):
    schedule.every().day.at(time_str).do(job_func)

    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute between checks
