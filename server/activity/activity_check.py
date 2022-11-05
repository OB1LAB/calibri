from activity.log_lib import log_type, unix_log, diff_times


def get_activity(server, players, date_check):
    activity, date, logs, local_dates = {}, None, None, server.get_logs_date()
    for nick_name in players:
        activity[nick_name] = {
            'L': 0,
            'G': 0,
            'PM': 0,
            'Warns': 0,
            'Mutes': 0,
            'Kicks': 0,
            'Bans': 0,
            'join': [],
            'exit': [],
            'vanish_join': [],
            'vanish_exit': [],
            'Online': False,
            'Vanish': False
        }
    if date_check in local_dates and local_dates.index(date_check) > 0:
        date = local_dates[local_dates.index(date_check) - 1]
        for line in server.logs.filter_by(date=date).first().get_logs():
            log = log_type(line)
            if log['type'] and log['player'] in activity:
                if log['type'] == 'join' and not activity[log['player']]['Online']:
                    activity[log['player']]['Online'] = True
                elif log['type'] == 'exit' and activity[log['player']]['Online']:
                    activity[log['player']]['Online'] = False
                    if activity[log['player']]['Vanish']:
                        activity[log['player']]['Vanish'] = False
                elif log['type'] == 'Vanish':
                    if activity[log['player']]['Vanish']:
                        activity[log['player']]['Vanish'] = False
                    else:
                        activity[log['player']]['Vanish'] = True
                if log['type'] != 'exit' and not activity[log['player']]['Online']:
                    activity[log['player']]['Online'] = True
            elif log['type'] == 'server_off':
                for player in activity:
                    if activity[player]['Online']:
                        activity[player]['Online'] = False
                        if activity[player]['Vanish']:
                            activity[player]['Vanish'] = False
    logs = server.logs.filter_by(date=date_check).first().get_logs()
    for line in logs:
        log = log_type(line.split())
        if log['type'] and log['player'] in activity:
            if log['type'] == 'join' and not activity[log['player']]['Online']:
                activity[log['player']]['Online'] = True
                activity[log['player']]['join'].append(unix_log(date_check, line))
            elif log['type'] == 'exit' and activity[log['player']]['Online']:
                activity[log['player']]['Online'] = False
                if not activity[log['player']]['join']:
                    activity[log['player']]['join'].append(unix_log(date_check, logs[0]))
                activity[log['player']]['exit'].append(unix_log(date_check, line))
                if activity[log['player']]['Vanish']:
                    if not activity[log['player']]['vanish_join']:
                        activity[log['player']]['vanish_join'].append(unix_log(date_check, logs[0]))
                    activity[log['player']]['vanish_exit'].append(unix_log(date_check, line))
                    activity[log['player']]['Vanish'] = False
            elif log['type'] == 'Vanish':
                if activity[log['player']]['Vanish']:
                    if not activity[log['player']]['vanish_join']:
                        activity[log['player']]['vanish_join'].append(unix_log(date_check, logs[0]))
                    activity[log['player']]['vanish_exit'].append(unix_log(date_check, line))
                    activity[log['player']]['Vanish'] = False
                else:
                    activity[log['player']]['vanish_join'].append(unix_log(date_check, line))
                    activity[log['player']]['Vanish'] = True
            elif log['type'] in ['L', 'G', 'PM', 'Warns', 'Mutes', 'Kicks', 'Bans']:
                activity[log['player']][log['type']] += 1
            if log['type'] != 'exit' and not activity[log['player']]['Online']:
                activity[log['player']]['join'].append(unix_log(date_check, line))
                activity[log['player']]['Online'] = True
            elif (log['type'] != 'Vanish' and activity[log['player']]['Vanish']
                  and len(activity[log['player']]['vanish_join']) == 0):
                activity[log['player']]['vanish_join'].append(unix_log(date_check, line))
        elif log['type'] == 'server_off':
            for player in activity:
                if activity[player]['Online']:
                    activity[player]['Online'] = False
                    activity[player]['exit'].append(unix_log(date_check, line))
                    if activity[player]['Vanish']:
                        if not activity[player]['vanish_join']:
                            activity[player]['vanish_join'].append(unix_log(date_check, logs[0]))
                        activity[player]['vanish_exit'].append(unix_log(date_check, line))
                        activity[player]['Vanish'] = False
    for pc in activity:
        if len(activity[pc]['join']) > len(activity[pc]['exit']):
            activity[pc]['exit'].append(unix_log(date_check, logs[-1]))
        if len(activity[pc]['vanish_join']) > len(activity[pc]['vanish_exit']):
            activity[pc]['vanish_exit'].append(unix_log(date_check, logs[-1]))
        activity[pc]['online_time'] = diff_times(activity[pc]['join'], activity[pc]['exit'])
        activity[pc]['vanish_time'] = diff_times(activity[pc]['vanish_join'], activity[pc]['vanish_exit'])
    return activity
