import os
from flask import Flask
from flasgger import Swagger
from conf.swagger_template import template
from routes.users import users
from routes.auth import auth 
from routes.posts import posts

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(auth)
app.register_blueprint(posts)

# Generate key using (uuid.uuid4().hex)
secret_key = os.environ['APP_SECRET_KEY']
app.secret_key = secret_key
app.config['SWAGGER'] = {
    'title': 'API Microblog',
    'uiversion': 3,
    "specs_route": "/"
}

swagger = Swagger(app, template=template)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))