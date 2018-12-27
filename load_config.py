from functools import wraps

SECRET_KEY = 'SECRET_KEY'
ALLOWED_HOSTS = 'ALLOWED_HOSTS'
TIMEZONE = 'TIMEZONE'

# ADMIN EMAIL
ADMINS = 'ADMINS'

# DATABASE CONFIGURATION
ENGINE = 'ENGINE'
NAME = 'NAME'
HOST = 'HOST'
PORT = 'PORT'
USER = 'USER'
PASSWORD = 'PASSWORD'
POSTGRES_ENGINE = 'django.db.backends.postgresql_psycopg2'
SQLITE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_CONFIG = [NAME, HOST, PORT, USER, PASSWORD, POSTGRES_ENGINE, SQLITE_ENGINE]

# EMAIL CONFIGURATION
EMAIL_HOST = 'EMAIL_HOST'
EMAIL_PORT = 'EMAIL_PORT'
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'

# DEFAULT VALUES
DEFAULT_ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DEFAULT_TIMEZONE = 'UTC'
DEFAULT_ENGINE = SQLITE_ENGINE
DEFAULT_SQLITE_NAME = 'db.sqlite3'

COMMENT_CHARS = ['#', ';']


def database_conf_not_allow(func):
    @wraps(func)
    def inner(self, key):
        if key in DATABASE_CONFIG:
            raise ValueError('Key %s not supported. Please use get_database_config() method.' % key)
        return func(self, key)

    return inner


class ConfigLoader:
    def __init__(self, file_path=None):
        self.file_path = 'config.ini' if file_path is None else file_path
        self.conf_dict = {}
        self._load_config_file()

    def _load_config_file(self):
        with open(self.file_path) as file:
            lines = file.readlines()
            for line in lines:
                if line[0] in COMMENT_CHARS or line == '' or line == '\n':
                    continue
                key, value = self._process_line(line)
                self.conf_dict[key] = value

    @staticmethod
    def _normalize_line(line: str):
        return line.strip()

    @staticmethod
    def _process_line(line: str):
        split = line[:-1].split(':')
        return split[0].strip(), split[1].strip()

    def get_property(self, key):
        return self.conf_dict.get(key, None)

    @database_conf_not_allow
    def to_python(self, key):
        value = self.conf_dict.get(key, None)
        if value is None:
            return None
        if value.__contains__(';'):
            value = value.split(';')
            v_list = []
            for v in value:
                value1 = v.split(',')[0].strip()
                value2 = v.split(',')[1].strip()
                v_list.append((value1, value2))
            return v_list
        elif value.__contains__(','):
            v_list = []
            value1 = value.split(',')[0].strip()
            value2 = value.split(',')[1].strip()
            v_list.append((value1, value2))
            return v_list
        elif value.__contains__(' '):
            return [i for i in value.split(' ')]
        else:
            return value

    def get_database_config(self):
        default = {ENGINE: DEFAULT_ENGINE}
        is_sqlite = True
        for k in self.conf_dict.keys():
            if self.is_database_config(k):
                if k == 'HOST':
                    is_sqlite = False
                default[k] = self.get_property(k)
        if not is_sqlite:
            default[ENGINE] = POSTGRES_ENGINE
        return {'default': default}

    @staticmethod
    def is_database_config(key):
        return key in DATABASE_CONFIG
