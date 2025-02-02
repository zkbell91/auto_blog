import schedule
import time

def schedule_job(job_func, time_str="10:00"):
    """
    Schedule a job to run at a specific time.
    
    Args:
        job_func: The function to run
        time_str: The time to run the job at (24-hour format, e.g., "10:00")
    """
    schedule.every().day.at(time_str).do(job_func)
    
    print(f"Job scheduled to run daily at {time_str}")
    print("Starting scheduler. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
    except Exception as e:
        print(f"\nScheduler stopped due to error: {str(e)}")
