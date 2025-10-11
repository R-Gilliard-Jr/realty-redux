import os

from flask import Flask

from realty_redux.ui import index, report


def create_app(test_config: dict = None, **kwargs) -> Flask:
    app = Flask(__name__, instance_relative_config=True, **kwargs)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")
    app.register_blueprint(report.bp)

    return app
