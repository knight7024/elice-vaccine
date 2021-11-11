from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        JSON_AS_ASCII = False
    )
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import search
    app.register_blueprint(search.bp)
    
    import update_data
    update_data.start(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app