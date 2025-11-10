from flask import Flask # type: ignore
from dotenv import load_dotenv # type: ignore
from flasgger import swag_from  # type: ignore
import os

from rotas.auth_routes import auth_bp
from rotas.usuarios_routes import usuarios_bp
from rotas.clientes_routes import clientes_bp
from rotas.pedidos_routes import pedidos_bp
from rotas.relatorios_routes import relatorios_bp

from metodos.swagger_init import configurar_swagger
from metodos.versao_projeto import obter_versao_atual_projeto

from migration import inicializar_csv


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "default-secret")


def setup_inicial():
    print("Inicializando dados do sistema...")
    inicializar_csv()
    print("Inicialização concluída!")


setup_inicial()
#  Inicializa o Swagger
configurar_swagger(app)


# @app.before_request
# def setup():


@app.route("/")
@swag_from({
  "tags": ["Sistema"],
  "summary": "Status da API",
  "description": "Retorna o status do projeto e a versão.",
  "responses": {
    200: {
      "description": "Retorna o status atual da API",
      "schema": {
        "type": "object",
        "properties": {
          "status": {"type": "string", "example": "ok"},
          "mensagem": {"type": "string", "example": "Servidor rodando!"},
          "versao": {"type": "string", "example": "1.0.0"}
        }
      }
    }
  }
})
def status():
    return {"status": "ok", "mensagem": "Servidor rodando!", "versao": obter_versao_atual_projeto()}, 200


#  Registrar as rotas
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(relatorios_bp)


if __name__ == "__main__":
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    print(f"Projeto inicializado na versão {obter_versao_atual_projeto()}! Debug={DEBUG} no Host={HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
