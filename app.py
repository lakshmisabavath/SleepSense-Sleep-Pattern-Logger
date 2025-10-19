from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

sleep_data = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_sleep():
    sleep_time = request.form['sleep_time']
    wake_time = request.form['wake_time']
    sleep_period = request.form['sleep_period']
    wake_period = request.form['wake_period']

    # Combine time + AM/PM into one string and parse
    fmt = "%I:%M %p"
    sleep_str = f"{sleep_time} {sleep_period}"
    wake_str = f"{wake_time} {wake_period}"

    sleep_dt = datetime.strptime(sleep_str, fmt)
    wake_dt = datetime.strptime(wake_str, fmt)

    # Calculate sleep duration (hours)
    duration = (wake_dt - sleep_dt).total_seconds() / 3600
    if duration < 0:
        duration += 24  # handle overnight sleep

    sleep_data.append({
        'date': datetime.now().strftime("%Y-%m-%d"),
        'sleep_time': f"{sleep_time} {sleep_period}",
        'wake_time': f"{wake_time} {wake_period}",
        'duration': round(duration, 2)
    })

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if not sleep_data:
        return render_template('dashboard.html', avg_sleep=0, suggestions="No data yet.", data=[])

    total = sum(d['duration'] for d in sleep_data)
    avg_sleep = round(total / len(sleep_data), 2)

    if avg_sleep < 6:
        suggestion = "Try sleeping earlier; you’re getting less than 6 hours on average."
    elif 6 <= avg_sleep <= 8:
        suggestion = "Good job! You’re maintaining healthy sleep duration."
    else:
        suggestion = "You might be oversleeping. Try maintaining 7–8 hours daily."

    return render_template('dashboard.html', avg_sleep=avg_sleep, suggestions=suggestion, data=sleep_data)

if __name__ == '__main__':
    app.run(debug=True)
