# period-and-fertility-calculator
Flask Period and Fertility Calendar Calculator

Web-app is up-and-running on this subdomain http://period-and-fertility-calculator.stefanrosu.ro/ 

# Run the Flask app as a systemd service at boot
sudo nano /etc/systemd/system/flask-app.service
sudo systemctl status flask-app.service
sudo systemctl start flask-app.service

# Run the Flask app in the background manually
# 2>&1 -> redirect stderr to stdout
# & -> run in the background
nohup python3 app.py > log.txt 2>&1 &

