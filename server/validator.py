from datetime import datetime


def error_status(name, message):
    return {
        'message': {name: message}
    }, 400


schemes = {
    'name': {
        'type': str,
        'min_length': 3,
        'max_length': 16
    },
    'code': {
        'type': str,
        'min_length': 6,
        'max_length': 64
    },
    'date': {
        'type': str,
        'min_length': 10,
        'max_length': 10
    },
    'id': {
        'type': int
    },
    'balance': {
        'type': int,
    },
    'birthday': {
        'type': str,
        'min_length': 4,
        'max_length': 32
    },
    'server_name': {
        'type': str,
        'min_length': 2,
        'max_length': 16
    },
    'role_name': {
        'type': str,
        'min_length': 2,
        'max_length': 32
    },
    'discord_id': {
        'type': str,
        'min_length': 2,
        'max_length': 20
    },
    'cause': {
        'type': str,
        'min_length': 0,
        'max_length': 256
    },
    'violation': {
        'type': str,
        'min_length': 2,
        'max_length': 32
    },
    'state': {
        'type': str,
        'min_length': 2,
        'max_length': 32
    }
}


def validate(type_data):
    def validator(value):
        schema = schemes[type_data]
        if not isinstance(value, schemes[type_data]['type']):
            raise ValueError(f"Невалидный тип данных. Ожидается {schema['type']}")
        elif schema['type'] == str and not schema['max_length'] >= len(value) >= schema['min_length']:
            raise ValueError(f"Длина должна быть в диапозоне [{schema['min_length']}, {schema['max_length']}]")
        if type_data == 'date':
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f'Дата должна быть в формате 31-12-2022')
        return value
    return validator
