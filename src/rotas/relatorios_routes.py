from flask import Blueprint, jsonify, request  # type: ignore
from flasgger import swag_from  # type: ignore

from metodos.auth import autenticar_token
from metodos.relatorios import gerar_relatorio_csv, gerar_relatorio_pdf

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@relatorios_bp.route("/pedidos", methods=["GET"])
@autenticar_token
@swag_from({
    "tags": ["Relatórios"],
    "summary": "Gerar relatório de pedidos",
    "description": """
    Gera um relatório de pedidos no formato CSV (padrão) ou PDF.  
    É necessário estar autenticado para acessar esta rota.
    """,
    "parameters": [
        {
            "name": "formato",
            "in": "query",
            "type": "string",
            "required": False,
            "enum": ["csv", "pdf"],
            "default": "csv",
            "description": "Formato desejado do relatório.",
        }
    ],
    "responses": {
        200: {
            "description": "Relatório gerado com sucesso.",
            "examples": {
                "application/json": {
                    "mensagem": "Relatório gerado com sucesso: relatorio_pedidos.csv"
                }
            },
        },
        404: {
            "description": "Nenhum dado encontrado para gerar o relatório.",
            "examples": {
                "application/json": {"erro": "Sem dados para gerar relatório."}
            },
        },
        401: {
            "description": "Token ausente ou inválido.",
            "examples": {
                "application/json": {"erro": "Token inválido ou expirado"}
            },
        },
    },
})
def gerar_relatorio():
    formato = request.args.get("formato", "csv")
    arquivo = gerar_relatorio_pdf() if formato == "pdf" else gerar_relatorio_csv()

    if not arquivo:
        return jsonify({"erro": "Sem dados para gerar relatório."}), 404

    return jsonify({"mensagem": f"Relatório gerado com sucesso: {arquivo}"})
