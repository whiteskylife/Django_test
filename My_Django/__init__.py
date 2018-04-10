import pymysql
pymysql.install_as_MySQLdb()

from sg import custom_signal_name


def custom_signal(sender, **kwargs):
    print('custom_signal')
    print('custom_signal_args:', sender, kwargs)


custom_signal_name.connect(custom_signal)
