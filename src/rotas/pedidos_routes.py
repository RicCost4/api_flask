from flask import Blueprint, jsonify, request  # type: ignore
from flasgger import swag_from  # type: ignore

from metodos.auth import autenticar_token
from services.db_pedidos import adicionar_pedido, listar_pedidos_com_clientes

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")


@pedidos_bp.route("/", methods=["POST"])
@autenticar_token
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Criar um novo pedido",
    "description": "Cria um novo pedido associado a um cliente.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "cliente_id": {"type": "integer", "example": 1},
                    "valor": {"type": "number", "example": 250.75},
                    "data": {"type": "string", "format": "date", "example": "2025-11-07"},
                },
                "required": ["cliente_id", "valor", "data"],
            },
        }
    ],
    "responses": {
        201: {
            "description": "Pedido criado com sucesso",
            "examples": {"application/json": {"mensagem": "Pedido criado com sucesso"}},
        },
        400: {
            "description": "Erro de validação nos dados enviados",
            "examples": {"application/json": {"erro": "Campos obrigatórios: cliente_id, valor, data"}},
        },
    },
})
def criar_pedido():
    dados = request.json
    if not dados or not all(k in dados for k in ["cliente_id", "valor", "data"]):
        return jsonify({"erro": "Campos obrigatórios: cliente_id, valor, data"}), 400
    try:
        adicionar_pedido(dados["cliente_id"], float(dados["valor"]), dados["data"])
        return jsonify({"mensagem": "Pedido criado com sucesso"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@pedidos_bp.route("", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Listar todos os pedidos",
    "description": "Retorna todos os pedidos, incluindo informações do cliente associado.",
    "responses": {
        200: {
            "description": "Lista de pedidos retornada com sucesso",
            "examples": {
                "application/json": [
                    {
                        "id": 1,
                        "cliente_id": 1,
                        "cliente_nome": "João da Silva",
                        "valor": 250.75,
                        "data": "2025-11-07",
                    }
                ]
            },
        }
    },
})
def listar_pedidos():
    pedidos = listar_pedidos_com_clientes()
    return jsonify(pedidos)
