from flasgger import Swagger # type: ignore

from metodos.versao_projeto import obter_versao_atual_projeto


def configurar_swagger(app):
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API",
            "description": "Documentação interativa da API (com JWT Auth)",
            "version": obter_versao_atual_projeto()
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Insira o token JWT: Bearer {token}"
            }
        },
        "security": [{"Bearer": []}]
    }
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "docs",
                "route": "/docs.json",
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/"
    }

    Swagger(app, config=swagger_config, template=swagger_template)