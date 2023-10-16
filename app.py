from datetime import date, datetime, timedelta
from calendar import HTMLCalendar
from colorama import Fore
import calendar

from flask import Flask, render_template, request
import os


app = Flask(__name__)
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, my_year, my_month, my_day, fertile_period, next_period_day, next_period):
        super().__init__()
        self.my_year = my_year
        self.my_month = my_month
        self.my_day = my_day
        self.fertile_period = fertile_period
        self.next_period_day = next_period_day
        self.next_period = next_period

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # Empty cell for days outside the current month
        else:
            css_class = "day"
            if day == self.my_day and day != -1:
                css_class = "red-day"
            elif day in self.fertile_period and day > self.my_day:
                css_class = "green-day"
                # Remove fertile days that were already highlighted, otherwise they will be duplicated for next month
                self.fertile_period.remove(day)
            elif day == self.next_period_day and self.my_month == self.next_period.month:
                css_class = "orange-day"
            return f'<td class="{css_class}">{day}</td>'

    def formatweek(self, theweek):
        week = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return f'<tr>{week}</tr>'

def calculate_next_period(year, month, day, period_days):
    current_date = datetime.now()
    my_year = year
    my_month = month
    my_day = day
    days_to_add = period_days - 1
    
    current_period = date(my_year, my_month, my_day)
    next_period = current_period + timedelta(days=days_to_add)

    print_format = "%a, %d-%b-%Y, Week %W"
    print(f"\nInput date: {current_period.strftime(print_format)}")
    print(f"+{days_to_add + 1} day(s): {next_period.strftime(print_format)}\n")

    fertile_days = 5
    next_period_day = next_period.day

    _, num_days = calendar.monthrange(my_year, my_month)

    fertile_period = [(next_period_day - 14 - i) % num_days + 1 for i in range(fertile_days)]
    

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    days = " ".join(days)
    print(f"{calendar.month_name[my_month]} {my_year}".center(len(days)))
    print(days)


    my_calendar = CustomHTMLCalendar(
        my_year, my_month, my_day, fertile_period, next_period_day, next_period
    )
    # Current month period should not be highlighted in the next month's calendar
    my_day = -1
    
    # Generate the HTML for the calendar
    calendar_html = my_calendar.formatmonth(my_year, my_month)


    if next_period.month != my_month:
        next_month = my_month % 12 + 1
        next_year = my_year + 1 if next_month == 1 else my_year
        # next_month_calendar = calendar.monthcalendar(next_year, next_month)

        my_next_calendar = CustomHTMLCalendar(
            next_year, next_month, my_day, fertile_period, next_period_day, next_period
        )
            
        # Generate the HTML for the next month calendar
        my_next_calendar_html = my_next_calendar.formatmonth(next_year, next_month)
        # ... and return the calendar for both months
        return calendar_html + my_next_calendar_html
        
    # If no next month calendar needed, return the HTML calendar for the current month
    return calendar_html


@app.route("/", methods=['POST', 'GET'])
def generate_calendar():
    # Get form data
    if request.method == 'POST':
        # Get form data
        print("[DEBUG] ", request.form)
        try:
            year = int(request.form.get('year'))
            month = int(request.form.get('month'))
            day = int(request.form.get('day'))
        except:
            year = date.today().year
            month = date.today().month
            day = date.today().day
            
        period_days = request.form.get('period_days')
        if period_days is not None and period_days.isdigit():
            period_days = int(period_days)
        else:
            period_days = 27
        # print(f"\n[DEBUG] User form input is: year {year} | month {month} | day {day} | days between periods {period_days}")
    else:
        # Hardcoded test data
        year = date.today().year
        month = date.today().month
        day = date.today().day
        period_days = 27  # zero indexed
    
    # Generate the calendar HTML
    calendar_html = calculate_next_period(year, month, day, period_days)

    return render_template("calendar.html", calendar_html=calendar_html)


if __name__ == "__main__":
    app.run()
