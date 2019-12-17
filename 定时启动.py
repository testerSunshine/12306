import schedule
import time
import os
print("python begin:")
def job():
    print("I'm working...")
    os.system("python run.py")
 
# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("8:50").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
 
while True:
    schedule.run_pending()
