from app import db
from app.models import User, Role, AppLogs, Server
from validator import validate, error_status
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse


class UserDb(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        users_list = []
        for staff in User.query.all():
            data = {
                'id': staff.id,
                'name': staff.name,
                'balance': float(staff.balance),
                'birthday': staff.birthday,
                'discord': staff.discord_id,
                'dt': {
                    'name': staff.dt_role.name,
                    'lvl': staff.dt_role.lvl,
                    'viewName': staff.dt_role.viewName
                },
                'tmrpg': {
                    'name': staff.tmrpg_role.name,
                    'lvl': staff.tmrpg_role.lvl,
                    'viewName': staff.tmrpg_role.viewName
                }
            }
            users_list.append(data)
        return users_list

    @jwt_required()
    def post(self):
        args = add.parse_args()
        check_user = User.query.filter_by(name=args['name']).first()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        current_discord = User.query.filter_by(discord_id=args['discord_id']).first()
        if args['selectedServer'] == 'dt':
            current_user_role = current_user.dt_role
            selected_role = Role.query.filter_by(name=args['selectedRole']).first()
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            current_user_role = current_user.tmrpg_role
            selected_role = Role.query.filter_by(name=args['selectedRole']).first()
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'не найден')
        if not selected_role:
            return error_status('Роль', 'не найдена')
        if selected_role.lvl >= current_user_role.lvl or current_user_role.lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        if selected_role.lvl == 1:
            return error_status('Должность', 'должна быть выше чем "пользователь"')
        if check_user:
            if args['selectedServer'] == 'dt':
                user_role = check_user.dt_role
            else:
                user_role = check_user.tmrpg_role
            if user_role.lvl > 1:
                return error_status('Пользователь', 'уже есть в таблице данного сервера')
        if not check_user:
            user = User()
        else:
            user = User.query.filter_by(name=args['name']).first()
        if current_discord:
            error_status('Данный дискорд', f'уже используется пользователем {current_discord.name}')
        if not server.players.filter_by(name=args['name']).first():
            return error_status('Пользователь', 'в этом вайпе не заходил на сервер')
        user.name = args['name']
        user.discord_id = args['discord_id']
        user.birthday = args['birthday']
        if args['selectedServer'] == 'dt':
            log_text = '[ДТ]'
            user.dt_role_id = selected_role.id
            if not check_user:
                user.tmrpg_role_id = 1
        else:
            user.tmrpg_role_id = selected_role.id
            log_text = '[ТМРПГ]'
            if not check_user:
                user.dt_role_id = 1
        log_text += f' {current_user.name} назначил {user.name} на должность {selected_role.viewName}'
        log_text += f' с дискорд ID {user.discord_id}'
        if not check_user:
            db.session.add(user)
        db.session.add(AppLogs(log=log_text))
        db.session.commit()

    @jwt_required()
    def put(self):
        args = edit.parse_args()
        check_name = User.query.filter_by(name=args['name']).first()
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        current_discord = User.query.filter_by(discord_id=args['discord_id']).first()
        user = User.query.get(args['id'])
        if check_name and user.id != check_name.id:
            return error_status('Никнейм', 'уже занят')
        if not user:
            return error_status('Пользователь', 'не найден')
        if args['selectedServer'] == 'dt':
            log_text = f'[ДТ]'
            current_user_role = current_user.dt_role
            user_role = user.dt_role
            selected_role = Role.query.filter_by(name=args['selectedRole']).first()
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            log_text = f'[ТМРПГ]'
            current_user_role = current_user.tmrpg_role
            user_role = user.tmrpg_role
            selected_role = Role.query.filter_by(name=args['selectedRole']).first()
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'Не найден')
        if not selected_role:
            return error_status('Роль', 'Не найдена')
        if (user_role.lvl >= current_user_role.lvl or selected_role.lvl >= current_user_role.lvl
                or current_user_role.lvl < 5):
            return error_status('Permissions', 'You don\'t have permissions')
        if not server.players.filter_by(name=args['name']).first():
            return error_status('Пользователь', 'в этом вайпе не заходил на сервер')
        log_text += f' {current_user.name} изменил у {user.name}'
        check_edit = len(log_text)
        if user.name != args['name']:
            log_text += f' никнейм на {args["name"]}'
            user.name = args['name']
        if user.discord_id != args['discord_id']:
            if current_discord and current_user.discord_id != args['discord_id']:
                return error_status('Данный дискорд', f'уже занят пользователем {current_discord.name}')
            log_text += f' дискорд с {user.discord_id} на {args["discord_id"]}'
            user.discord_id = args['discord_id']
        if user.balance != args['balance']:
            log_text += f' баланс с {user.balance} на {args["balance"]}'
            user.balance = args['balance']
        if user.birthday != args['birthday']:
            log_text += f' др с {user.birthday} на {args["birthday"]}'
            user.birthday = args['birthday']
        if args['selectedServer'] == 'dt' and user.dt_role_id != selected_role.id:
            log_text += f' роль с {user.dt_role.viewName} на {selected_role.viewName}'
            user.dt_role_id = selected_role.id
        elif args['selectedServer'] == 'tmrpg' and user.tmrpg_role_id != selected_role.id:
            log_text += f' роль с {user.tmrpg_role.viewName} на {selected_role.viewName}'
            user.tmrpg_role_id = selected_role.id
        if selected_role.lvl == 1:
            server.coffers += user.balance
            log_text += f' баланс на момент ухода: {user.balance}'
            user.balance = 0
        if len(log_text) != check_edit:
            db.session.add(AppLogs(log=log_text))
        db.session.commit()


edit = reqparse.RequestParser()
edit.add_argument('id', required=True, type=validate('id'))
edit.add_argument('name', required=True, type=validate('name'))
edit.add_argument('balance', required=True, type=validate('balance'))
edit.add_argument('discord_id', required=True, type=validate('discord_id'))
edit.add_argument('birthday', required=True, type=validate('birthday'))
edit.add_argument('selectedRole', required=True, type=validate('role_name'))
edit.add_argument('selectedServer', required=True, type=validate('server_name'))

add = reqparse.RequestParser()
add.add_argument('name', required=True, type=validate('name'))
add.add_argument('discord_id', required=True, type=validate('discord_id'))
add.add_argument('birthday', required=True, type=validate('birthday'))
add.add_argument('selectedRole', required=True, type=validate('role_name'))
add.add_argument('selectedServer', required=True, type=validate('server_name'))
