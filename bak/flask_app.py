from flask import Flask, render_template
from calendar import HTMLCalendar
from datetime import date


app = Flask(__name__)


class MyHTMLCalendar(HTMLCalendar):
    def formatday(self, day, weekday):
        # Your logic for customizing each day's content
        if day == 0:
            return f"<td>  </td>"
        if day < 10:
            return f"<td>&nbsp;&nbsp;{day}</td>"
        return f"<td>{day}</td>"

    def formatweek(self, theweek):
        # Create a row for a week
        week = "".join(self.formatday(d, wd) for (d, wd) in theweek)
        return f"<tr>{week}</tr>"

    def formatmonth(self, theyear, themonth):
        # Create the HTML for an entire month
        cal = super().formatmonth(theyear, themonth)
        return cal


@app.route("/")
def generate_calendar():
    year = date.today().year
    month = date.today().month

    # Generate the calendar HTML
    cal = MyHTMLCalendar()
    calendar_html = cal.formatmonth(year, month)

    return render_template("calendar.html", calendar_html=calendar_html)


if __name__ == "__main__":
    app.run()
