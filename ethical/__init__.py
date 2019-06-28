import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ethical.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        return render_template('index.html')

    # create the basic database tables
    from . import db
    db.init_app(app)

    # setup the unhashed authentication blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    # setup the unsalted, hashed authentication blueprints
    from . import hauth
    app.register_blueprint(hauth.bp)

    # setup the salted, hashed authentication blueprints
    from . import shauth
    app.register_blueprint(shauth.bp)

    return app
