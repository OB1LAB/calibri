from datetime import datetime, timedelta
from app.models import User, Activity, Server, Player
from validator import error_status, validate
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from activity.log_lib import date_sort, output_time


class ActivityPlayers(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        today = datetime.now()
        data = {
            'dt': {
                'staff': [],
                'players': []
            },
            'tmrpg': {
                'staff': [],
                'players': []
            },
            'monday': (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        }
        for server in ['dt', 'tmrpg']:
            server_db = Server.query.filter_by(name=server).first()
            logs = date_sort([log.date for log in server_db.logs.all()], with_txt=False, reverse_dates=True)
            for player in server_db.players.all():
                data[server]['players'].append(
                    {
                        'name': player.name,
                        'rank': 'player',
                        'lvl': 1
                    }
                )
                data[server]['wipe'] = logs[0]
                data[server]['lastDay'] = logs[-1]
        users = User.query.all()
        for user in users:
            if user.dt_role.lvl in [2, 3, 4]:
                data['dt']['staff'].append({
                    'name': user.name,
                    'rank': user.dt_role.name,
                    'lvl': user.dt_role.lvl
                })
            if user.tmrpg_role.lvl in [2, 3, 4]:
                data['tmrpg']['staff'].append({
                    'name': user.name,
                    'rank': user.tmrpg_role.name,
                    'lvl': user.tmrpg_role.lvl
                })
        return data

    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 2:
            return error_status('Permissions', 'You don\'t have permissions')
        data_players = {}
        args = parser.parse_args()
        if args['selectedServer'] == 'dt':
            server = Server.query.filter_by(name='dt').first()
        elif args['selectedServer'] == 'tmrpg':
            server = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Выбранный сервер', 'не найден')
        dates = [
            (args['date1'] + timedelta(
                days=day)).strftime('%d-%m-%Y') for day in range((args['date2'] - args['date1']).days+1)]
        for player in server.players.filter(Player.name.in_(args['players'])).all():
            activity_data = {
                'L': 0,
                'G': 0,
                'PM': 0,
                'Warns': 0,
                'Mutes': 0,
                'Kicks': 0,
                'Bans': 0,
                'Vanish': player.vanish,
                'Status': player.online
            }
            online, vanish = 0, 0
            for data in player.activity.filter(Activity.date.in_(dates)).all():
                activity_data['L'] += data.local_msg
                activity_data['G'] += data.global_msg
                activity_data['PM'] += data.private_msg
                activity_data['Warns'] += data.warns
                activity_data['Mutes'] += data.mutes
                activity_data['Kicks'] += data.kicks
                activity_data['Bans'] += data.bans
                online += data.online
                vanish += data.online_vanish
            if len(dates) == 0:
                dates.append("01-01-1970")
            activity_data['AVG'] = output_time(int(online / len(dates))) + ' ' + output_time(int(vanish / len(dates)))
            activity_data['Total'] = output_time(online) + ' ' + output_time(vanish)
            data_players[player.name] = activity_data
        return data_players


parser = reqparse.RequestParser()
parser.add_argument('date1', required=True, type=validate('date'))
parser.add_argument('date2', required=True, type=validate('date'))
parser.add_argument('players', required=True, type=str, action='append')
parser.add_argument('selectedServer', required=True, type=validate('server_name'))
