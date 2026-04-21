from slack_client import download_schedules
from parser import pdf_to_dates, pdf_to_schedule, sort_dates
from calendar_client import create_events
import logging

logging.basicConfig(filename="sync.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
end_message = "End of program run instance.\n"

def main():
    logging.info("Logging script started.")

    schedule_file = download_schedules()
    if schedule_file is None:
        logging.info("No new schedule found.")
        logging.info(end_message)
        return
    else:
        print("file " + schedule_file)

    
    dates = pdf_to_dates(schedule_file)
    if dates is None:
        logging.error("Dates not properly extracted from pdf.")
        logging.info(end_message)
        return
    else:
        sort_dates(dates)
        print("dates " + str(dates))

    schedule = pdf_to_schedule(schedule_file)
    if schedule is None:
        logging.error("Schedule not properly extracted from pdf.")
        logging.info(end_message)
        return
    else:
        print("schedule " + str(schedule))

    try:
        create_events(dates, schedule)
    except Exception:
        logging.error("Error during event creation.", exc_info=True)

    logging.info(end_message)

if __name__ == "__main__":
    main()