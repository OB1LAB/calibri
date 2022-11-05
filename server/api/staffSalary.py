from datetime import timedelta
from app import db
from app.models import User, Server, Activity, AppLogs
from validator import error_status, validate
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from activity.log_lib import output_time, date_range_str, to_datetime


class Salary(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        return get_staff_salary()

    @jwt_required()
    def put(self):
        args = parser.parse_args()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if args['selectedServer'] == 'dt':
            current_user_role = current_user.dt_role
            server = Server.query.filter_by(name='dt').first()
            log_text = '[ДТ]'
        elif args['selectedServer'] == 'tmrpg':
            current_user_role = current_user.tmrpg_role
            server = Server.query.filter_by(name='tmrpg').first()
            log_text = '[ТМРПГ]'
        else:
            return error_status('Выбранный сервер', 'не найден')
        if current_user_role.lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        db.session.add(
            AppLogs(
                log=f"{log_text} {current_user.name} изменил погашенный итог с {server.coffers} на {args['value']}"))
        server.coffers = args['value']
        db.session.commit()
        return get_staff_salary()


parser = reqparse.RequestParser()
parser.add_argument('value', required=True, type=int)
parser.add_argument('selectedServer', required=True, type=validate('server_name'))


def get_staff_salary():
    data = {}
    td = Server.query.filter_by(name='dt').first()
    tmrpg = Server.query.filter_by(name='tmrpg').first()
    for server in [td, tmrpg]:
        data[server.name] = {
            'salaryPlayers': [],
            'salaryData': {
                'mainSalary': 0,
                'answerForum': 0,
                'online': 0,
                'additionallyOnline': 0,
                'bonus': 0,
                'totalWeek': 0,
                'totalAllTime': 0
            },
            'chartData': {
                'labels': [],
                'playerData': []
            },
            'chartOnlineData': {
                'labels': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
                'playerData': []
            },
            'coffers': server.coffers
        }
        report = server.reports.all()[-1]
        days = date_range_str(report.date, (to_datetime(report.date) + timedelta(days=6)).strftime('%d-%m-%Y'))
        users = [user for user in report.users.all()]
        sorted_name = sorted(users, key=lambda o: o.user.name)
        if server.name == 'dt':
            sorted_users = sorted(sorted_name, key=lambda o: o.user.dt_role.lvl)
        else:
            sorted_users = sorted(sorted_name, key=lambda o: o.user.tmrpg_role.lvl)
        sorted_users.reverse()
        for user in sorted_users:
            if not 2 <= user.user.dt_role.lvl <= 4 and not 2 <= user.user.tmrpg_role.lvl <= 4:
                continue
            data[server.name]['salaryPlayers'].append({
                'name': user.user.name,
                'rank': user.user.max_role().viewName,
                'mainSalary': user.salary,
                'answerForum': user.answer_forum,
                'online': output_time(user.online),
                'additionallyOnline': user.add_online,
                'bonus': user.bonus,
                'totalWeek': float(user.week_balance),
                'totalAllTime': float(user.user.balance),
                'birthday': user.user.birthday
            })
            activity = server.players.filter_by(name=user.user.name).first().activity.filter(
                Activity.date.in_(days)).all()
            data[server.name]['chartData']['labels'].append(user.user.name)
            data[server.name]['chartData']['playerData'].append(float(user.week_balance))
            data[server.name]['chartOnlineData']['playerData'].append({
                'label': user.user.name,
                'data': [f'{data.online / 3600:.1f}' for data in activity],
            })
            data[server.name]['salaryData']['mainSalary'] += user.salary
            data[server.name]['salaryData']['answerForum'] += user.answer_forum
            data[server.name]['salaryData']['online'] += user.online
            data[server.name]['salaryData']['additionallyOnline'] += user.add_online
            data[server.name]['salaryData']['bonus'] += user.bonus
            data[server.name]['salaryData']['totalWeek'] += float(user.week_balance)
            data[server.name]['salaryData']['totalAllTime'] += float(user.user.balance)
        data[server.name]['salaryData']['online'] = output_time(data[server.name]['salaryData']['online'])
    return data
