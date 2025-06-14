from flask_restx import Api
from routes_swagger import auth_ns, coffee_ns, purchase_ns

def configure_swagger(app):
    api = Api(
        app,
        version='1.0',
        title='Coffee Shop API',
        description='API REST para gerenciar uma cafeteria com autenticação JWT',
        doc='/docs/',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Digite: Bearer <seu_token>"
            }
        },
        security='Bearer'
    )
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(coffee_ns, path='/coffee')
    api.add_namespace(purchase_ns, path='/purchase')
    
    return api 