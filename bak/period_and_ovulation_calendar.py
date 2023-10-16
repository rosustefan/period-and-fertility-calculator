from datetime import date
from datetime import datetime
from datetime import timedelta
import calendar

# from IPython.display import clear_output

# try:
#     from colorama import Fore  # import colorama
# except:
#     print("Installing module 'colorama'")
#     !pip3 install colorama --quiet  # install colorama package
from colorama import Fore


print_format = "%a, %d-%b-%Y, Week %W"

# Get the current date
current_date = datetime.now()


def calculate_next_period():
    try:
        my_year, my_month, my_day = map(
            int,
            input(
                "Type the year, month and date separated by spaces(if empty/invalid will default to current date): "
            ).split(),
        )
    except ValueError:
        # Extract the year, month, and day from the current date
        my_year = current_date.year
        my_month = current_date.month
        my_day = current_date.day
        print(f"[INFO] Invalid input provided, using the current date.")
    except Exception as e:
        print(f"Something went wrong when processing the date: {e}")
        exit(e)

    # Get the days to add to the current menstrual date
    try:
        days_to_add = input(
            "Type the number of days to add (if empty/invalid will default to 28): "
        )
        days_to_add = int(days_to_add) - 1
    except ValueError:
        print("[INFO] Invalid input provided, using the default value.")
        days_to_add = (
            28 - 1
        )  # minus 1 to also count the first day of the period 'my_day'
    except Exception as e:
        print(f"Something went wrong when processing the days to add: {e}")
        exit(e)

    current_period = date(my_year, my_month, my_day)
    next_period = current_period + timedelta(days=days_to_add)

    print(f"\nInput date: {current_period.strftime(print_format)}")
    print(f"+{days_to_add+1} day(s): {next_period.strftime(print_format)}\n")

    # Create a calendar object
    current_month_calendar = calendar.monthcalendar(my_year, my_month)

    # Extract the day from the next_period
    next_period_day = next_period.day

    # Define the fertile period number of days
    fertile_days = 5

    # Get number of days in the current month
    _, num_days = calendar.monthrange(my_year, my_month)

    # Calculate the fertile_period
    fertile_period = [
        (next_period_day - 14 - i) % num_days + 1 for i in range(fertile_days)
    ]

    # Define the days of the week
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Print the current month's name and the days of the week in the header
    days = " ".join(days)
    print(f"{calendar.month_name[my_month]} {my_year}".center(len(days)))
    print(days)

    # Print the calendar for the current month
    for week in current_month_calendar:
        for day in week:
            if day == 0:
                print("   ", end=" ")  # Print spaces for days outside the month
            else:
                if day == my_day:
                    print(f"{Fore.RED}{day:2}{Fore.RESET}  ", end="")
                elif day in fertile_period:
                    if day > my_day:
                        print(
                            f"{Fore.GREEN}{day:2}{Fore.RESET}  ", end=""
                        )  # Emphasize the fertile days
                        fertile_period.remove(
                            day
                        )  # Remove the printed fertile days from the array
                    else:
                        print(f"{day:2}  ", end="")
                elif day == next_period_day and next_period.month == my_month:
                    print(
                        f"{Fore.RED}{day:2}{Fore.RESET}  ", end=""
                    )  # Emphasize the specified day(s)
                else:
                    print(f"{day:2}  ", end="")
        print()  # Move to the next line for the next week

    # Check if the next_period day is in the next month
    if next_period.month != my_month:
        next_month = (
            my_month % 12 + 1
        )  # Increment the month and wrap to January if necessary
        next_year = (
            my_year + 1 if next_month == 1 else my_year
        )  # If next month is January, increment the year
        next_month_calendar = calendar.monthcalendar(
            next_year, next_month
        )  # Create the calendar for the next month

        # Print next month's name and the days of the week in the header
        print("\n" + f"{calendar.month_name[next_month]} {next_year}".center(len(days)))
        print(days)

        # Iterate through the rows (weeks) of the next month's calendar
        for week in next_month_calendar:
            for day in week:
                if day == 0:
                    print("   ", end=" ")  # Print spaces for days outside the month
                else:
                    if day in fertile_period:  # and day <= next_period_day:
                        print(
                            f"{Fore.GREEN}{day:2}{Fore.RESET}  ", end=""
                        )  # Emphasize the fertile days
                    elif day == next_period_day:
                        print(
                            f"{Fore.RED}{day:2}{Fore.RESET}  ", end=""
                        )  # Emphasize next period
                    else:
                        print(f"{day:2}  ", end="")
            print()  # Move to the next line for the next week


print(
    f"This program predicts the date of {Fore.RED}the next menstrual cycle\
{Fore.RESET} based on the input date.\nMoreover, it also highlights {Fore.GREEN}the ovulation days{Fore.RESET}.\n"
)
input("Press any key to continue.")

while True:
    calculate_next_period()
    show_me_more = (
        input("\nPress any key to continue or 'no' to stop: ").lower().strip()
    )
    if show_me_more == "no":
        break
    clear_output()
