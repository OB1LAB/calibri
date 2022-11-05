from datetime import datetime, timedelta
from time import sleep
from app import app, db
from app.models import User, Server, Activity, WeekUser, Report
from activity.log_lib import date_range_str

with app.app_context():
    while True:
        today = datetime.now()
        report_date = (today - timedelta(days=today.weekday())) - timedelta(weeks=1)
        report_day = report_date.strftime('%d-%m-%Y')
        days = date_range_str(report_day, (report_date+timedelta(days=6)).strftime('%d-%m-%Y'))
        for server in ['dt', 'tmrpg']:
            server_db = Server.query.filter_by(name=server).first()
            report = server_db.reports.filter_by(date=report_day).first()
            if not report:
                report = Report(date=report_day, server_id=server_db.id)
                db.session.add(report)
                db.session.commit()
                if server == 'dt':
                    users = [user for user in User.query.all() if user.dt_role.lvl in [2, 3, 4]]
                else:
                    users = [user for user in User.query.all() if user.tmrpg_role.lvl in [2, 3, 4]]
                for user in users:
                    vacation, violation = False, False
                    vacations, violations = user.vacations.all(), user.violations.all()
                    for row in vacations:
                        if (row.date_end - datetime.now()).total_seconds() > 0:
                            vacation = True
                    for row in violations:
                        if row.type == 'rebuke' and 31 > (datetime.now() - row.date).days > 0:
                            violation = True
                    online, salary, add_online = 0, 0, 0
                    activity = server_db.players.filter_by(name=user.name).first().activity.filter(
                        Activity.date.in_(days)).all()
                    for date in activity:
                        online += date.online
                    if server == 'dt' and not violation:
                        salary = user.dt_role.salary
                    elif server == 'tmrpg' and not violation:
                        salary = user.tmrpg_role.salary
                    if vacation:
                        salary = salary / 2
                    if server == 'dt' and int(online/7) > 7200 and not violation and not vacation:
                        add_online = (int(online/7) - 7200)/60*0.5
                    elif server == 'tmrpg' and int(online/7) > 10800 and not violation and not vacation:
                        add_online = (int(online/7) - 10800)/60*0.5
                    week_user = WeekUser(
                        user_id=user.id,
                        report_id=report.id,
                        online=int(online/7),
                        add_online=add_online,
                        salary=salary,
                        week_balance=salary+add_online
                    )
                    user.balance += int(salary+add_online)
                    db.session.add(week_user)
                db.session.commit()
                print(f'Сделан отчёт на {server_db.name} с {days[0]} до {days[-1]}')
        sleep(60)
