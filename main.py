from slack_client import fetch_new_schedules, download_schedules
from parser import pdf_to_dates, pdf_to_schedule, sort_dates
from calendar_client import create_events
import logging

logging.basicConfig(filename="sync.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
end_message = "End of program run instance.\n"

def main():
    logging.info("Logging script started.")

    try:
        fetch_new_schedules()
    except Exception:
        logging.error("Failed to fetch schedules", exc_info=True)
        logging.info(end_message)
        return

    ts_list = []
    try:
        with open("latest_processed_file") as f:
            for line in f:
                if line.split()[1] == "UNPROCESSED":
                    ts_list.append(line.split()[0])
    except Exception:
        logging.error("Error reading latest_processed_file.", exc_info=True)
        logging.info(end_message)
        return

    if not ts_list:
        logging.info("No new schedules found.")
        logging.info(end_message)
        return

    #main loop to process each schedule
    for ts in ts_list:

        try:
            schedule_file = download_schedules(ts)
            print("file " + schedule_file)
        except Exception:
            logging.error("Error downloading schedule at timestamp: " + ts , exc_info=True)
            continue

        try:
            dates = pdf_to_dates(schedule_file)
            sort_dates(dates)
            print("dates " + str(dates))
        except Exception:
            logging.error("Error extracting dates from schedule at timestamp: " + ts, exc_info=True)
            continue

        try:
            schedule = pdf_to_schedule(schedule_file)
            print("schedule " + str(schedule))
        except Exception:
            logging.error("Error extracting schedule from pdf at timestamp: " + ts, exc_info=True)
            continue

        try:
            create_events(dates, schedule)
            with open("latest_processed_file", "r") as f:
                lines = f.readlines()
            with open("latest_processed_file", "w") as f:
                for line in lines:
                    if line.split()[0] == ts:
                        f.write(ts + " PROCESSED\n")
                    else:
                        f.write(line)
        except Exception:
            logging.error("Error during event creation.", exc_info=True)

    try:
        with open("latest_processed_file", "r") as f:
            full_file = f.readlines()
        processed_files = [line for line in full_file if line.split()[1] == "PROCESSED"]
        unprocessed_files = [line for line in full_file if line.split()[1] == "UNPROCESSED"]
    except Exception:
        logging.error("Error reading latest_processed_file.", exc_info=True)
        logging.info(end_message)
        return

    try:
        remaining_files = processed_files[-5:] + unprocessed_files
        remaining_files.sort(key=lambda x: float(x.split()[0]))
        with open("latest_processed_file", "w") as f:
            for line in remaining_files:
                f.write(line)
    except Exception:
        logging.error("Error writing to latest_processed_file.", exc_info=True)

    logging.info(end_message)

if __name__ == "__main__":
    main()