from app import db
from datetime import datetime


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    viewName = db.Column(db.String(32), unique=True)
    lvl = db.Column(db.Integer)
    salary = db.Column(db.Integer, default=0)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    discord_id = db.Column(db.String(20), unique=True, index=True)
    balance = db.Column(db.Numeric(10, 2), default=0)
    dt_role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    tmrpg_role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    dt_role = db.relationship('Role', foreign_keys=dt_role_id, uselist=False)
    tmrpg_role = db.relationship('Role', foreign_keys=tmrpg_role_id, uselist=False)
    birthday = db.Column(db.String(32))
    vacations = db.relationship('HistoryVacation', backref='user_historyvacation', lazy='dynamic')
    violations = db.relationship('HistoryViolation', backref='user_historyviolation', lazy='dynamic')

    def max_role(self):
        if self.dt_role.lvl > self.tmrpg_role.lvl:
            return self.dt_role
        return self.tmrpg_role


class WeekUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id, uselist=False)
    answer_forum = db.Column(db.Integer, default=0)
    bonus = db.Column(db.Integer, default=0)
    online = db.Column(db.Integer, default=0)
    add_online = db.Column(db.Integer, default=0)
    salary = db.Column(db.Integer, default=0)
    week_balance = db.Column(db.Integer, default=0)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id', ondelete='CASCADE'))


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), index=True)
    users = db.relationship('WeekUser', backref='report_weekuser', passive_deletes=True, lazy='dynamic')
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    coffers = db.Column(db.Integer, default=0)
    logs = db.relationship('ServerLogs', backref='server_serverlogs', lazy='dynamic')
    players = db.relationship('Player', backref='server_player', lazy='dynamic')
    reports = db.relationship('Report', backref='server_report', lazy='dynamic')

    def get_logs_date(self):
        return [log.date for log in self.logs.all()]


class ServerLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), index=True)
    lines = db.relationship('Line', backref='server_logs_line', lazy='dynamic')
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

    def get_logs(self):
        return sorted([line.line for line in self.lines.all()])


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(256))
    serverLogs_id = db.Column(db.Integer, db.ForeignKey('server_logs.id'))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    online = db.Column(db.db.Boolean, default=False)
    vanish = db.Column(db.db.Boolean, default=False)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    activity = db.relationship('Activity', backref='player_activity', lazy='dynamic')


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), index=True)
    local_msg = db.Column(db.Integer, default=0)
    global_msg = db.Column(db.Integer, default=0)
    private_msg = db.Column(db.Integer, default=0)
    warns = db.Column(db.Integer, default=0)
    mutes = db.Column(db.Integer, default=0)
    kicks = db.Column(db.Integer, default=0)
    bans = db.Column(db.Integer, default=0)
    online = db.Column(db.Integer, default=0)
    online_vanish = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))


class HistoryVacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    cause = db.Column(db.String(256))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server', foreign_keys=server_id, uselist=False)


class HistoryViolation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    type = db.Column(db.String(32))
    cause = db.Column(db.String(256))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server', foreign_keys=server_id, uselist=False)

    def translate(self):
        if self.type == 'easy':
            return 'Лёгкое'
        elif self.type == 'strict':
            return 'Строгое'
        elif self.type == 'rough':
            return 'Грубое'
        elif self.type == 'rebuke':
            return 'Выговор'
        return 'Not found'


class HistoryBuy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id, uselist=False)
    date = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item_shop.id', ondelete='CASCADE'))
    item = db.relationship('ItemShop', foreign_keys=item_id, passive_deletes=True, uselist=False)
    state = db.Column(db.String(32))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server', foreign_keys=server_id, uselist=False)


class ItemShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    viewName = db.Column(db.String(128))
    type = db.Column(db.String(16))
    price = db.Column(db.Numeric(10, 2))
    categories = db.Column(db.String(64))
    stack = db.Column(db.Integer)


class AppLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    log = db.Column(db.String(512))
