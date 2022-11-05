from app import db
from app.models import User, HistoryVacation, AppLogs, Server
from validator import error_status, validate
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from api.history import get_history


class Vacation(Resource):
    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        args = parser.parse_args()
        user = User.query.get(args['userId'])
        date_start = args['dateStart']
        date_end = args['dateEnd']
        if not user:
            return error_status('Пользователь', 'не найден')
        if args['selectedServer'] == 'dt':
            db.session.add(
                AppLogs(log=f'[ДТ] {current_user.name} отправил в отпуск {user.name} с '
                            f'{date_start.strftime("%d-%m-%Y")} по {date_end.strftime("%d-%m-%Y")} '
                            f'({(date_end-date_start).days})'))
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            db.session.add(
                AppLogs(log=f'[ТМРПГ] {current_user.name} отправил в отпуск {user.name} с '
                            f'{date_start.strftime("%d-%m-%Y")} по {date_end.strftime("%d-%m-%Y")} '
                            f'({(date_end - date_start).days})'))
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'не найден')
        db.session.add(HistoryVacation(user_id=user.id, date_start=date_start, date_end=date_end, cause=args['cause'],
                                       server_id=server.id))
        db.session.commit()

    @jwt_required()
    def put(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        args = deleteVacation.parse_args()
        vacation = HistoryVacation.query.get(args['vacationId'])
        if not vacation:
            return error_status('Запись', 'не найдена')
        user = User.query.get(vacation.user_id)
        if args['selectedServer'] == 'dt':
            db.session.add(AppLogs(log=f'[ДТ] {current_user.name} очистил отпуск у {user.name}'))
        elif args['selectedServer'] == 'tmrpg':
            db.session.add(AppLogs(log=f'[ТМРПГ] {current_user.name} очистил отпуск у {user.name}'))
        else:
            return error_status('Выбранный сервер', 'не найден')
        db.session.delete(vacation)
        db.session.commit()
        return get_history()


parser = reqparse.RequestParser()
parser.add_argument('userId', required=True, type=int)
parser.add_argument('dateStart', required=True, type=validate('date'))
parser.add_argument('dateEnd', required=True, type=validate('date'))
parser.add_argument('cause', required=True, type=validate('cause'))
parser.add_argument('selectedServer', required=True, type=validate('server_name'))

deleteVacation = reqparse.RequestParser()
deleteVacation.add_argument('vacationId', required=True, type=int)
deleteVacation.add_argument('selectedServer', required=True, type=validate('server_name'))
