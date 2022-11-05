from app import db
from api.history import get_history
from app.models import User, HistoryBuy, Server, ItemShop, AppLogs
from validator import error_status, validate
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse


class Market(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        data = {
            'dt': [],
            'tmrpg': [],
            'case': [],
            'donate': []
        }
        for item in ItemShop.query.all():
            type_item = item.type
            if '/' in type_item:
                type_item = type_item.split('/')[1]
            data[type_item].append(
                {
                    'id': item.id,
                    'name': item.name,
                    'viewName': item.viewName,
                    'cat': item.categories,
                    'price': float(item.price),
                    'img_path': f'images/{type_item}/{item.name}.png'.replace(':', '_')
                }
            )
        return data

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        if args['selectedServer'] == 'dt':
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'Не найден')
        item = ItemShop.query.get(args['itemId'])
        if not item:
            return error_status('Предмет', 'не найден')
        if args['amount'] <= 0:
            return error_status('Можно купить', 'только положительное число предметов')
        if item.price * args['amount'] > current_user.balance:
            return error_status('Недостаточно средст', 'для покупки')
        current_user.balance -= item.price * args['amount']
        db.session.add(HistoryBuy(user_id=current_user.id, amount=args['amount'], item_id=item.id,
                                  state='На рассмотрении', server_id=server.id))
        db.session.commit()

    @jwt_required()
    def put(self):
        args = historyBuy.parse_args()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        row = HistoryBuy.query.get(args['rowId'])
        if not row:
            return error_status('Запись', 'не найдена')
        if row.server.name == 'dt':
            db.session.add(AppLogs(log=f'[ДТ] {current_user.name} изменил статус покупки '
                                       f'с {row.state} на {args["status"]} [{row.id}]'))
        else:
            db.session.add(AppLogs(log=f'[ТМРПГ] {current_user.name} изменил статус покупки '
                                       f'с {row.state} на {args["status"]} [{row.id}]'))
        if args['status'] == 'Отказано':
            row.user.balance += row.amount * row.item.price
        elif args['status'] == 'Выдано' and row.state == 'Отказано':
            row.user.balance -= row.amount * row.item.price
        row.state = args['status']
        db.session.commit()
        return get_history()


parser = reqparse.RequestParser()
parser.add_argument('itemId', required=True, type=int)
parser.add_argument('selectedServer', required=True, type=validate('server_name'))
parser.add_argument('amount', required=True, type=int)

historyBuy = reqparse.RequestParser()
historyBuy.add_argument('rowId', required=True, type=int)
historyBuy.add_argument('status', required=True, type=validate('state'))
