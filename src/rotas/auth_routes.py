from flask import Blueprint, request, jsonify   # type: ignore
from flasgger import swag_from   # type: ignore

from metodos.auth import gerar_tokens, renovar_token
from services.db_usuarios import validar_usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Realiza o login de um usuário interno ou externo",
    "description": "Valida o usuário e senha e retorna tokens JWT (access e refresh).",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["username", "senha"],
                "properties": {
                    "username": {"type": "string"},
                    "senha": {"type": "string"},
                    "tipo": {"type": "string", "enum": ["interno", "externo"]}
                }
            }
        }
    ],
    "responses": {
      200: {
        "description": "Login realizado com sucesso, retorna tokens JWT",
        "schema": {
            "type": "object",
            "properties": {
                "access_token": {"type": "string"},
                "refresh_token": {"type": "string"},
                "expira_em_min": {"type": "integer"}
            }
        }
      },
      401: {
        "description": "Usuário ou senha inválidos",
        "schema": {
            "type": "object",
            "properties": {
                "erro": {"type": "string"}
            }
        }
      }
    }
})
def login():
    dados = request.json
    username = dados.get("username")
    senha = dados.get("senha")
    tipo = dados.get("tipo", "interno")

    if validar_usuario(username, senha, tipo):
        access_token, refresh_token = gerar_tokens(username, tipo)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expira_em_min": 60
        })
    return jsonify({"erro": "Usuário ou senha inválidos"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Gera um novo par de tokens JWT usando o refresh token",
    "description": "Recebe um refresh token válido e retorna um novo access e refresh token.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["refresh_token"],
                "properties": {
                    "refresh_token": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
      200: {
        "description": "Novo par de tokens JWT gerado com sucesso",
        "schema": {
            "type": "object",
            "properties": {
                "access_token": {"type": "string"},
                "refresh_token": {"type": "string"}
            }
        },
      },
      400: {
        "description": "Refresh token inválido ou expirado",
        "schema": {
            "type": "object",
            "properties": {
                "erro": {"type": "string"}
            }
        }
      }
    }
})
def refresh():
    dados = request.json
    token = dados.get("refresh_token")
    novo = renovar_token(token)
    if not novo:
        return jsonify({"erro": "Refresh token inválido ou expirado"}), 401
    return jsonify(novo)
