# app.py
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

# Configure the GraphQL endpoint with GraphiQL interface enabled
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable the GraphiQL interface for testing
    )
)

if __name__ == '__main__':
    app.run(debug=True)
