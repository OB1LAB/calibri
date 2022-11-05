from app.models import User, HistoryBuy, HistoryViolation, HistoryVacation
from validator import error_status
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource


class History(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        return get_history()


def get_history():
    data = {}
    for server in ['dt', 'tmrpg']:
        data[server] = {
            'vacation': [],
            'violation': [],
            'buy': []
        }
    for row in HistoryVacation.query.all():
        data[row.server.name]['vacation'].append({
            'id': row.id,
            'user': User.query.get(row.user_id).name,
            'user_id': row.user_id,
            'start': row.date_start.strftime('%d-%m-%Y'),
            'end': row.date_end.strftime('%d-%m-%Y'),
            'days': (row.date_end - row.date_start).days,
            'cause': row.cause
        })
    for row in HistoryViolation.query.all():
        data[row.server.name]['violation'].append({
            'id': row.id,
            'user': User.query.get(row.user_id).name,
            'user_id': row.user_id,
            'date': row.date.strftime('%d-%m-%Y'),
            'cause': row.translate() + "/" + row.cause
        })
    for row in HistoryBuy.query.all():
        data[row.server.name]['buy'].append({
            'id': row.id,
            'user': row.user.name,
            'user_id': row.user_id,
            'date': row.date.strftime('%d-%m-%Y'),
            'amount': row.amount,
            'item': row.item.viewName,
            'state': row.state,
            'price': float(row.item.price)
        })
    return data
