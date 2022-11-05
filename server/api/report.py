from app import db
from datetime import datetime, timedelta
from app.models import User, Server, Activity, WeekUser, AppLogs
from validator import validate, error_status
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from activity.log_lib import date_range_str


class Report(Resource):
    @jwt_required()
    def put(self):
        args = parser.parse_args()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if args['selectedServer'] == 'dt':
            current_user_role = current_user.dt_role
            server = Server.query.filter_by(name='dt').first()
            users = [user for user in User.query.all() if user.dt_role.lvl in [2, 3, 4]]
            log_text = f'[ДТ]'
        elif args['selectedServer'] == 'tmrpg':
            current_user_role = current_user.tmrpg_role
            server = Server.query.filter_by(name='tmrpg').first()
            users = [user for user in User.query.all() if user.tmrpg_role.lvl in [2, 3, 4]]
            log_text = f'[ТМРПГ]'
        else:
            return error_status('Выбранный сервер', 'не найден')
        if current_user_role.lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        today = datetime.now()
        this_monday = today - timedelta(days=today.weekday())
        report_date = this_monday - timedelta(weeks=1)
        report_day = report_date.strftime('%d-%m-%Y')
        days, check_days = [], date_range_str(report_day, (report_date + timedelta(days=6)).strftime('%d-%m-%Y'))
        for day in range(len(check_days)):
            if day in args['days']:
                days.append(check_days[day])
        if not len(days):
            days = check_days
        report = server.reports.filter_by(date=report_day).first()
        for user in users:
            vacation, violation = False, False
            vacations, violations = user.vacations.all(), user.violations.all()
            for row in vacations:
                if (row.date_end - this_monday).total_seconds() > 0:
                    vacation = True
            for row in violations:
                if row.type == 'rebuke' and 31 > (this_monday-row.date).days > 0:
                    violation = True
            online, salary, add_online = 0, 0, 0
            check_user = server.players.filter_by(name=user.name).first()
            if not check_user:
                error_status(f'{user.name}', 'Не найден в логах сервера')
            activity = check_user.activity.filter(Activity.date.in_(days)).all()
            for date in activity:
                online += date.online
            if server.name == 'dt' and not violation:
                salary = user.dt_role.salary
            elif server.name == 'tmrpg' and not violation:
                salary = user.tmrpg_role.salary
            if vacation:
                salary = salary / 2
            if server.name == 'dt' and int(online / len(days)) > 7200 and not violation and not vacation:
                add_online = (int(online / len(days)) - 7200) / 60 * 0.5
            elif server.name and int(online / len(days)) > 10800 and not violation and not vacation:
                add_online = (int(online / len(days)) - 10800) / 60 * 0.5
            week_user = report.users.filter_by(user_id=user.id).first()
            if not week_user:
                week_user = WeekUser(
                    user_id=user.id,
                    report_id=report.id,
                    online=int(online / len(days)),
                    add_online=add_online,
                    salary=salary,
                    week_balance=salary + add_online
                )
                user.balance += int(salary + add_online)
                db.session.add(week_user)
            else:
                factor = 0
                if args['selectedServer'] == 'dt' and user.dt_role.lvl > 2:
                    factor = 15
                elif user.tmrpg_role.lvl > 2:
                    factor = 15
                week_salary = salary + add_online + week_user.bonus + week_user.answer_forum*factor
                user.balance += int(week_salary - week_user.week_balance)
                week_user.online = int(online / len(days))
                week_user.add_online = add_online
                week_user.salary = salary
                week_user.week_balance = week_salary
        log_text += f' {current_user.name} обновил отчёт со следующими датами: {", ".join(days)}'
        db.session.add(AppLogs(log=log_text))
        db.session.commit()


parser = reqparse.RequestParser()
parser.add_argument('selectedServer', required=True, type=validate('server_name'))
parser.add_argument('days', required=True, type=int, action='append')
