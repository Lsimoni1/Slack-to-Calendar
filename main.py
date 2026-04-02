from slack_client import download_schedules
from parser import pdf_to_dates, pdf_to_schedule, sort_dates
from calendar_client import create_events

def main():
    schedule_file = download_schedules()
    print("file " + schedule_file)
    if schedule_file is None:
        return
    
    dates = pdf_to_dates(schedule_file)
    sort_dates(dates)
    schedule = pdf_to_schedule(schedule_file)
    print("dates " + str(dates))
    print("schedule " + str(schedule))

    create_events(dates, schedule)

if __name__ == "__main__":
    main()