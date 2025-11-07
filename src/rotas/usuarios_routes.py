from flask import Blueprint, jsonify, request  # type: ignore
from flasgger import swag_from  # type: ignore
import jwt

from metodos.auth import autenticar_token, CHAVE_SECRETA
from services.db_usuarios import criar_usuario_admin, alterar_senha

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("", methods=["POST"])
@autenticar_token
@swag_from({
    "tags": ["Usuários"],
    "summary": "Criar novo usuário (somente administradores internos)",
    "description": """
    Cria um novo usuário no sistema.  
    Apenas usuários **internos** (administradores) podem executar esta operação.
    """,
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "username": "novo_usuario",
                    "senha": "123456",
                    "tipo": "interno"
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Usuário criado com sucesso.",
            "examples": {
                "application/json": {
                    "mensagem": "Usuário criado com sucesso!"
                }
            }
        },
        400: {
            "description": "Erro ao criar o usuário.",
            "examples": {
                "application/json": {
                    "erro": "Usuário já existe."
                }
            }
        },
        403: {
            "description": "Acesso negado — usuário sem permissão.",
            "examples": {
                "application/json": {
                    "erro": "Acesso negado"
                }
            }
        },
        401: {
            "description": "Token inválido ou expirado.",
            "examples": {
                "application/json": {
                    "erro": "Token inválido"
                }
            }
        },
    },
})
def criar_usuario():
    token = request.headers.get("Authorization").split(" ")[1]
    payload = jwt.decode(token, CHAVE_SECRETA, algorithms=["HS256"])

    if payload.get("tipo") != "interno":
        return jsonify({"erro": "Acesso negado"}), 403

    data = request.get_json()
    sucesso, msg = criar_usuario_admin(
        data.get("username"),
        data.get("senha"),
        data.get("tipo", "interno")
    )
    return jsonify({"mensagem" if sucesso else "erro": msg}), 200 if sucesso else 400


@usuarios_bp.route("/alterar_senha", methods=["POST"])
@autenticar_token
@swag_from({
    "tags": ["Usuários"],
    "summary": "Alterar senha do usuário logado",
    "description": """
    Permite que o usuário autenticado altere sua própria senha.  
    É necessário fornecer a senha atual e a nova senha.
    """,
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "senha_atual": "senha_antiga",
                    "nova_senha": "senha_nova"
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Senha alterada com sucesso.",
            "examples": {
                "application/json": {
                    "mensagem": "Senha atualizada com sucesso!"
                }
            }
        },
        400: {
            "description": "Erro ao alterar senha.",
            "examples": {
                "application/json": {
                    "erro": "Senha atual incorreta."
                }
            }
        },
        401: {
            "description": "Token inválido ou expirado.",
            "examples": {
                "application/json": {
                    "erro": "Token inválido"
                }
            }
        },
    },
})
def alterar_senha_usuario():
    token = request.headers.get("Authorization").split(" ")[1]
    payload = jwt.decode(token, CHAVE_SECRETA, algorithms=["HS256"])
    username = payload["username"]

    data = request.get_json()
    sucesso, msg = alterar_senha(
        username,
        data.get("senha_atual"),
        data.get("nova_senha")
    )
    return jsonify({"mensagem" if sucesso else "erro": msg}), 200 if sucesso else 400
