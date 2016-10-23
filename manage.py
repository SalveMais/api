# encoding:utf-8
import sys

from flask_script import Manager

from salvemais import create_app

if __name__ == '__main__':
    try:
        env_name = sys.argv.pop(2)
    except:
        env_name = None
    app = create_app(env=env_name)

    manager = Manager(app)

    manager.run()
