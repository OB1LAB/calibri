import os
from app import app, db
from app.models import Role, User, Server, ServerLogs, Line, Player, Activity, ItemShop
from activity.activity_check import get_activity
from activity.log_lib import date_sort, log_type
from items import items_dt, items_tmrpg, donate, cases

with app.app_context():
    # db.drop_all()
    # db.create_all()
    user = Role(name='user', viewName="Пользователь", lvl=1)
    helper1 = Role(name='helper1', viewName="Стажёр", salary=50, lvl=2)
    helper2 = Role(name='helper2', viewName="Помощник", salary=100, lvl=3)
    mod = Role(name='mod', viewName="Модератор", salary=150, lvl=4)
    st = Role(name='st', viewName="Старший модератор", lvl=5)
    gm = Role(name='gm', viewName="Главный модератор", lvl=6)
    curator = Role(name='curator', viewName="Куратор", lvl=7)
    admin = Role(name='admin', viewName="*", lvl=8)
    dt = Server(name='dt')
    tmrpg = Server(name='tmrpg')
    db.session.add_all([user, helper1, helper2, mod, st, gm, curator, admin, dt, tmrpg])
    db.session.commit()
    ob1ch = User(name="OB1CHAM", discord_id="727563752421195789", dt_role_id=admin.id, tmrpg_role_id=admin.id,
                 birthday="3 сентября")
    francuzz = User(name="Francuzz214", discord_id='388767423081349130', dt_role_id=admin.id, tmrpg_role_id=admin.id,
                    birthday="10 апреля")
    db.session.add_all([ob1ch, francuzz])
    db.session.commit()
    for server in ['dt', 'tmrpg']:
        players = {}
        server_db = Server.query.filter_by(name=server).first()
        dates = date_sort(os.listdir(f'logs/{server}'), with_txt=False)
        for date in dates:
            add_data = []
            logs = ServerLogs(date=date, server_id=server_db.id)
            db.session.add(logs)
            db.session.commit()
            lines = open(f'logs/{server}/{date}.txt', 'r', encoding='utf-8').readlines()
            for line in lines:
                line_split = line.split()
                add_data.append(Line(line=line, serverLogs_id=logs.id))
                if len(line_split) == 3:
                    log_line = log_type(line_split)
                    if log_line['type'] == 'join' and log_line['player'] not in players:
                        player = Player(name=log_line['player'], server_id=server_db.id)
                        add_data.append(player)
                        players[log_line['player']] = player
            db.session.add_all(add_data)
            db.session.commit()
        for date in dates:
            add_data = []
            players_activity = get_activity(server_db, players.keys(), date)
            for player in players_activity:
                player_activity = Activity(date=date, player_id=players[player].id)
                player_activity.local_msg = players_activity[player]['L']
                player_activity.global_msg = players_activity[player]['G']
                player_activity.private_msg = players_activity[player]['PM']
                player_activity.warns = players_activity[player]['Warns']
                player_activity.mutes = players_activity[player]['Mutes']
                player_activity.kicks = players_activity[player]['Kicks']
                player_activity.bans = players_activity[player]['Bans']
                player_activity.online = players_activity[player]['online_time']
                player_activity.online_vanish = players_activity[player]['vanish_time']
                if date == dates[-1]:
                    players[player].online = players_activity[player]['Online']
                    players[player].vanish = players_activity[player]['Vanish']
                add_data.append(player_activity)
            db.session.add_all(add_data)
            db.session.commit()
    shop = []
    for item in items_dt:
        name = item['itemname']
        viewName = item['name']
        type_item = 'item/dt'
        price = round(float(item['pricerub']) / int(item['amount']), 2)
        stack = item['stacksize']
        categories = item['cat']
        shop.append(ItemShop(name=name, viewName=viewName, type=type_item, price=price, stack=stack,
                             categories=categories))
    for item in items_tmrpg:
        name = item['itemname']
        viewName = item['name']
        type_item = 'item/tmrpg'
        price = round(float(item['pricerub']) / int(item['amount']), 2)
        stack = item['stacksize']
        categories = item['cat']
        shop.append(ItemShop(name=name, viewName=viewName, type=type_item, price=price, stack=stack,
                             categories=categories))
    for item in cases:
        name = item['id']
        viewName = item['name']
        type_item = 'case'
        price = float(item['pricerub'])
        stack = 1
        categories = 'case'
        shop.append(ItemShop(name=name, viewName=viewName, type=type_item, price=price, stack=stack,
                             categories=categories))
    for item in donate:
        name = item['name'].split('>')[1].split('<')[0].split('(')[0]
        viewName = item['name'] + " | " + item['pricerub'].split(' | ')[1]
        type_item = 'donate'
        price = float(item['pricerub'].split(' |')[0])
        stack = 1
        categories = 'donate'
        shop.append(ItemShop(name=name, viewName=viewName, type=type_item, price=price, stack=stack,
                             categories=categories))
    db.session.add_all(shop)
    db.session.commit()
