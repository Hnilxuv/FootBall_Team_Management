from cerberus import Validator


def validate_update_data(data):
    schema = {'username': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                           'regex': '^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$'},
              'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
              'id': {'type': 'string', 'empty': False},
              'email': {'type': 'string', 'empty': False, 'maxlength': 50,
                        'regex': r'\b[A-Za-z0-9_%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'},
              'phone': {'type': 'string', 'empty': False, 'regex': r'[0-9]{11}'},
              'role_name': {'type': 'string', 'empty': False},
              'status': {'type': 'string', 'empty': False},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_insert_data(data):
    schema = {'username': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                           'regex': '^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$'},
              'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
              'password': {'type': 'string', 'empty': False, 'maxlength': 50},
              'confirm_password': {'type': 'string', 'empty': False, 'maxlength': 50},
              'email': {'type': 'string', 'empty': False, 'maxlength': 50,
                        'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,}\b'},
              'phone': {'type': 'string', 'empty': False, 'regex': r'[0-9]{11}'},
              'role_name': {'type': 'string', 'empty': False},
              'status': {'type': 'boolean', 'empty': False},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_register_data(data):
    schema = {'username': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                           'regex': '^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$'},
              'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
              'password': {'type': 'string', 'empty': False, 'maxlength': 50},
              'confirm_password': {'type': 'string', 'empty': False, 'maxlength': 50},
              'email': {'type': 'string', 'empty': False, 'maxlength': 50,
                        'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,}\b'},
              'phone': {'type': 'string', 'empty': False, 'regex': r'[0-9]{11}'},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_login_data(data):
    schema = {'username': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                           'regex': '^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$'},
              'password': {'type': 'string', 'empty': False, 'maxlength': 50},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}
              }
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_changepw_data(data):
    schema = {'old_password': {'type': 'string', 'empty': False},
              'new_password': {'type': 'string', 'empty': False},
              'new_confirm_password': {'type': 'string', 'empty': False},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_update_account_info(data):
    schema = {'username': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                           'regex': '^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$'},
              'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50,
                       },
              'email': {'type': 'string', 'empty': False, 'maxlength': 50,
                        'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,}\b'},
              'phone': {'type': 'string', 'empty': False, 'regex': r'[0-9]{11}'},
              'role_name': {'type': 'string', 'empty': False},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


def validate_data(data):
    schema = {'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors


# def validate_insert_league_data(data):
#     schema = {'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
#               'submit': {'type': 'string'},
#               'csrf_token': {'type': 'string'}}
#     v = Validator(schema)
#     if v.validate(data, schema):
#         return True
#     else:
#         return v.errors


def validate_player_data(data):
    schema = {'name': {'type': 'string', 'empty': False, 'minlength': 2, 'maxlength': 50},
              'shirt_number': {'type': 'integer', 'empty': False},
              'age': {'type': 'integer', 'empty': False},
              'position_name': {'type': 'string', 'empty': False},
              'submit': {'type': 'string'},
              'csrf_token': {'type': 'string'}}
    v = Validator(schema)
    if v.validate(data, schema):
        return True
    else:
        return v.errors