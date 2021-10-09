from flask import Flask
from flask_cors import CORS
from home import home

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, supports_credentials=True)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#注册蓝图
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=2050)

