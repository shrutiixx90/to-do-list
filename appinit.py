from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from keycloak import KeycloakOpenID
from .schema import schema
import stripe

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="your_client_id",
    realm_name="your_realm",
    client_secret_key="your_client_secret"
)

stripe.api_key = "your_stripe_secret_key"

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

from . import routes
