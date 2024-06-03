import schedule
import time

def schedule_job(job_function, time_string):
    schedule.every().day.at(time_string).do(job_function)

    while True:
        schedule.run_pending()
        time.sleep(60)