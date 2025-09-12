from fpdf import FPDF

def gerar_pdf(peticao_texto, nome_arquivo="peticao.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for linha in peticao_texto.split("\n"):
        pdf.multi_cell(0, 6, linha)

    pdf.output(nome_arquivo)
    return nome_arquivo
