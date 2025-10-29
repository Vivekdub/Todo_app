from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
from .db import SessionLocal
from .models import Task, User
from .emailer import send_email

REMINDER_MINUTES = 10#int(os.getenv("REMINDER_MINUTES", "30"))

def check_and_send_reminders():
    print("Here")
    db = SessionLocal()
    try:
        now = datetime.now()
        window_start = now
        window_end = now + timedelta(minutes=REMINDER_MINUTES + 1)
        tasks = db.query(Task).filter(
            Task.due_at != None,
            Task.is_completed == False,
            Task.reminder_sent == False,
            Task.due_at >= window_start,
            Task.due_at <= window_end
            ).all()
        print("Found tasks:", tasks)

        for t in tasks:
            user = db.query(User).filter(User.id == t.user_id).first()
            if not user:
                continue
            subject = f"Reminder: {t.title} due at {t.due_at.isoformat()}"
            body = f"Hi,\n\nThis is a reminder that your task \"{t.title}\" is due at {t.due_at}.\n\nDescription: {t.description or '—'}\n\nMark it complete if done.\n"
            sent = send_email(user.email, subject, body)
            if sent:
                print("Successful")
                t.reminder_sent = True
                db.add(t)
        print("Completed")
        db.commit()
    finally:
        db.close()

def start_scheduler():
    sched = BackgroundScheduler()
    sched.add_job(check_and_send_reminders, 'interval', seconds=60, id="reminder-job", replace_existing=True)
    sched.start()
    print("Scheduler started.")
