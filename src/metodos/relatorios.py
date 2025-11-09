import pandas as pd # type: ignore
from fpdf import FPDF # type: ignore
from services.db_pedidos import listar_pedidos_com_clientes


def gerar_relatorio_csv(caminho="../data/relatorio_pedidos.csv"):
    dados = listar_pedidos_com_clientes()
    if not dados:
        return None
    df = pd.DataFrame(dados)
    df.to_csv(caminho, index=False)
    return caminho


def gerar_relatorio_pdf(caminho="../data/relatorio_pedidos.pdf"):
    dados = listar_pedidos_com_clientes()
    if not dados:
        return None
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Relatório de Pedidos", ln=True, align="C")

    pdf.set_font("Arial", "", 10)
    for d in dados:
        linha = f"Cliente: {d['nome']} | Valor: R$ {d['valor']:.2f} | Data: {d['data']}"
        pdf.cell(200, 8, linha, ln=True)

    pdf.output(caminho)
    return caminho
