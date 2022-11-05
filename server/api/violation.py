from app import db
from app.models import User, AppLogs, Server, HistoryViolation
from validator import error_status, validate
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from api.history import get_history


class Violation(Resource):
    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        args = parser.parse_args()
        user = User.query.get(args['userId'])
        date_start = args['dateStart']
        if not user:
            return error_status('Пользователь', 'не найден')
        if args['type'] == 'easy':
            user.balance -= 50
        elif args['type'] == 'strict':
            user.balance -= 100
        elif args['type'] == 'rough':
            user.balance -= 200
        elif args['type'] != 'rebuke':
            error_status('Тип', 'Не найден тип')
        if args['selectedServer'] == 'dt':
            db.session.add(AppLogs(log=f'[ДТ] {current_user.name} выдал наказание "{args["type"]}" '
                                       f'пользователю {user.name}'))
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            db.session.add(AppLogs(log=f'[ТМРПГ] {current_user.name} выдал наказание "{args["type"]}" '
                                       f'пользователю {user.name}'))
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'не найден')
        db.session.add(HistoryViolation(user_id=user.id, date=date_start, type=args['type'], cause=args['cause'],
                                        server_id=server.id))
        db.session.commit()

    @jwt_required()
    def put(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        args = deleteViolation.parse_args()
        violation = HistoryViolation.query.get(args['violationId'])
        if not violation:
            return error_status('Запись', 'не найдена')
        user = User.query.get(violation.user_id)
        if args['selectedServer'] == 'dt':
            db.session.add(AppLogs(
                log=f'[ДТ] {current_user.name} очистил нарушение у {user.name} ({violation.translate()})'))
        elif args['selectedServer'] == 'tmrpg':
            db.session.add(AppLogs(
                log=f'[ТМРПГ] {current_user.name} очистил нарушение у {user.name} ({violation.translate()})'))
        else:
            return error_status('Выбранный сервер', 'не найден')
        if violation.type == 'easy':
            user.balance += 50
        elif violation.type == 'strict':
            user.balance += 100
        elif violation.type == 'rough':
            user.balance += 200
        db.session.delete(violation)
        db.session.commit()
        return get_history()


parser = reqparse.RequestParser()
parser.add_argument('userId', required=True, type=int)
parser.add_argument('dateStart', required=True, type=validate('date'))
parser.add_argument('type', required=True, type=validate('violation'))
parser.add_argument('cause', required=True, type=validate('cause'))
parser.add_argument('selectedServer', required=True, type=validate('server_name'))

deleteViolation = reqparse.RequestParser()
deleteViolation.add_argument('violationId', required=True, type=int)
deleteViolation.add_argument('selectedServer', required=True, type=validate('server_name'))
