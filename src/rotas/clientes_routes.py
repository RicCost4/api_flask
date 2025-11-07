from flask import Blueprint, jsonify, request  # type: ignore
from flasgger import swag_from  # type: ignore

from metodos.auth import autenticar_token
from services.db_clientes import (
    ler_todos,
    adicionar_cliente,
    obter_cliente,
    atualizar_cliente,
    excluir_cliente,
    filtrar_clientes,
    exportar_excel,
)
from services.db_pedidos import listar_pedidos_por_cliente

MSN_CLIENTE_NAO_ENCONTRADO = "Cliente não encontrado"

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.route("", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Listar todos os clientes",
    "responses": {
        200: {
            "description": "Lista de clientes retornada com sucesso",
            "examples": {
                "application/json": [
                    {"id": 1, "nome": "João", "email": "joao@email.com", "idade": 30, "cidade": "SP"}
                ]
            },
        }
    },
})
def listar_clientes():
    df = ler_todos()
    return jsonify(df.to_dict(orient="records"))


@clientes_bp.route("", methods=["POST"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Criar um novo cliente",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "idade": {"type": "integer"},
                    "cidade": {"type": "string"},
                    "telefone": {"type": "string"}
                },
                "required": ["nome", "email", "idade", "cidade"],
            },
        }
    ],
    "responses": {
        201: {"description": "Cliente criado com sucesso"},
        400: {"description": "Campos obrigatórios faltando"},
    },
})
def criar_cliente():
    dados = request.json
    if not dados or not all(k in dados for k in ["nome", "email", "idade", "cidade", "telefone"]):
        return jsonify({"erro": "Campos obrigatórios: nome, email, idade, cidade, telefone"}), 400

    cliente = adicionar_cliente(**dados)
    return jsonify(cliente), 201


@clientes_bp.route("/<int:id_cliente>", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Obter informações de um cliente específico",
    "parameters": [
        {"name": "id_cliente", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Cliente encontrado"},
        404: {"description": "Cliente não encontrado"},
    },
})
def get_cliente(id_cliente):
    cliente = obter_cliente(id_cliente)
    if cliente:
        return jsonify(cliente)
    return jsonify({"erro": MSN_CLIENTE_NAO_ENCONTRADO}), 404


@clientes_bp.route("/<int:id_cliente>", methods=["PUT"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Atualizar informações de um cliente",
    "parameters": [
        {"name": "id_cliente", "in": "path", "type": "integer", "required": True},
        {
            "name": "body", 
            "in": "body", 
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "idade": {"type": "integer"},
                    "cidade": {"type": "string"},
                    "telefone": {"type": "string"}
                }
            }
        },
    ],
    "responses": {
        200: {"description": "Cliente atualizado com sucesso"},
        404: {"description": "Cliente não encontrado"},
    },
})
def update_cliente(id_cliente):
    dados = request.json
    cliente = atualizar_cliente(id_cliente, dados)
    if cliente:
        return jsonify(cliente)
    return jsonify({"erro": MSN_CLIENTE_NAO_ENCONTRADO}), 404


@clientes_bp.route("/<int:id_cliente>", methods=["DELETE"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Excluir um cliente",
    "parameters": [
        {"name": "id_cliente", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Cliente removido com sucesso"},
        404: {"description": "Cliente não encontrado"},
    },
})
def delete_cliente(id_cliente):
    ok = excluir_cliente(id_cliente)
    if ok:
        return jsonify({"mensagem": "Cliente removido com sucesso"})
    return jsonify({"erro": MSN_CLIENTE_NAO_ENCONTRADO}), 404


@clientes_bp.route("/filtro", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Filtrar clientes por cidade e faixa etária",
    "parameters": [
        {"name": "cidade", "in": "query", "type": "string"},
        {"name": "idade_min", "in": "query", "type": "integer"},
        {"name": "idade_max", "in": "query", "type": "integer"},
    ],
    "responses": {200: {"description": "Clientes filtrados retornados com sucesso"}},
})
def filtrar():
    cidade = request.args.get("cidade")
    idade_min = request.args.get("idade_min", type=int)
    idade_max = request.args.get("idade_max", type=int)
    resultado = filtrar_clientes(cidade, idade_min, idade_max)
    return jsonify(resultado)


@clientes_bp.route("/exportar", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Exportar lista de clientes em Excel",
    "responses": {
        200: {"description": "Exportação concluída"},
    },
})
def exportar():
    caminho = exportar_excel()
    return jsonify({"mensagem": "Exportação concluída", "arquivo": caminho})


@clientes_bp.route("/<int:cliente_id>/pedidos", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Clientes"],
    "summary": "Listar pedidos de um cliente",
    "parameters": [
        {"name": "cliente_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Pedidos retornados com sucesso"},
        404: {"description": "Nenhum pedido encontrado"},
    },
})
def listar_pedidos_cliente(cliente_id):
    pedidos = listar_pedidos_por_cliente(cliente_id)
    if not pedidos:
        return jsonify({"mensagem": "Nenhum pedido encontrado para este cliente."})
    return jsonify(pedidos)
