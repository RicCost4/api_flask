import jwt
from datetime import datetime, timedelta, timezone
import time
from functools import wraps
from flask import request, jsonify # type: ignore
from dotenv import load_dotenv # type: ignore
import os

from services.db_tokens import salvar_token, token_valido, revogar_token

load_dotenv()

CHAVE_SECRETA = os.getenv("APP_SECRET_KEY", "default-secret")

ACCESS_TOKEN_TTL = 60 * 60      # 60 minutos
REFRESH_TOKEN_TTL = 60 * 60 * 24 * 7  # 7 dias


def gerar_tokens(username: str, tipo: str):
    agora = datetime.now(timezone.utc)
    exp_access = agora + timedelta(seconds=ACCESS_TOKEN_TTL)
    exp_refresh = agora + timedelta(seconds=REFRESH_TOKEN_TTL)

    access_payload = {
        "username": username,
        "tipo": tipo,
        "exp": exp_access,
        "tipo_token": "access"
    }
    refresh_payload = {
        "username": username,
        "tipo": tipo,
        "exp": exp_refresh,
        "tipo_token": "refresh"
    }

    access_token = jwt.encode(access_payload, CHAVE_SECRETA, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, CHAVE_SECRETA, algorithm="HS256")

    # salvar no CSV de tokens
    salvar_token(refresh_token, username, tipo, time.time() + REFRESH_TOKEN_TTL)

    return access_token, refresh_token


def autenticar_token(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401
        try:
            payload = jwt.decode(token, CHAVE_SECRETA, algorithms=["HS256"])
            if payload.get("tipo_token") != "access":
                return jsonify({"erro": "Token inválido"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorador


def renovar_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, CHAVE_SECRETA, algorithms=["HS256"])
        if payload.get("tipo_token") != "refresh":
            return None
        if not token_valido(refresh_token):
            return None
        novo_access, novo_refresh = gerar_tokens(payload["username"], payload["tipo"])
        revogar_token(refresh_token)
        return {"access_token": novo_access, "refresh_token": novo_refresh}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
