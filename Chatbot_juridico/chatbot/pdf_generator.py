from fpdf import FPDF
import os
import unicodedata
import re

class PDF(FPDF):
    def __init__(self, titulo="Documento"):
        super().__init__()
        self.titulo = titulo

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, self.titulo, ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 10)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def limpar_texto_seguro(texto):
    texto = unicodedata.normalize("NFKC", texto)
    texto = ''.join(c if ord(c) <= 0xFFFF else '-' for c in texto)
    texto = re.sub(r'[\x00-\x1F\x7F]', '', texto)
    return texto

def quebrar_paragrafo(paragrafo, pdf, largura_maxima):
    indent = len(paragrafo) - len(paragrafo.lstrip(" "))
    espaco_indent = " " * indent
    palavras = paragrafo.strip().split(" ")
    linhas = []
    linha_atual = espaco_indent

    for palavra in palavras:
        teste_linha = f"{linha_atual} {palavra}".strip()
        if pdf.get_string_width(teste_linha) <= largura_maxima:
            linha_atual = teste_linha
        else:
            if linha_atual.strip():
                linhas.append(linha_atual)
            while pdf.get_string_width(palavra) > largura_maxima:
                for i in range(1, len(palavra)+1):
                    if pdf.get_string_width(palavra[:i]) > largura_maxima:
                        linhas.append(palavra[:i-1])
                        palavra = palavra[i-1:]
                        break
            linha_atual = palavra
    if linha_atual.strip():
        linhas.append(linha_atual)
    return linhas

def ajustar_fonte_automaticamente(pdf, texto, largura_maxima, altura_maxima, tamanho_inicial=12, tamanho_minimo=8):
    tamanho = tamanho_inicial
    pdf.set_font("DejaVu", size=tamanho)
    linhas_totais = []
    for paragrafo in texto.split("\n"):
        paragrafo = limpar_texto_seguro(paragrafo.strip())
        if not paragrafo:
            linhas_totais.append("")
            continue
        linhas_totais.extend(quebrar_paragrafo(paragrafo, pdf, largura_maxima))

    while (len(linhas_totais) * 6) > altura_maxima and tamanho > tamanho_minimo:
        tamanho -= 1
        pdf.set_font("DejaVu", size=tamanho)
        linhas_totais = []
        for paragrafo in texto.split("\n"):
            paragrafo = limpar_texto_seguro(paragrafo.strip())
            if not paragrafo:
                linhas_totais.append("")
                continue
            linhas_totais.extend(quebrar_paragrafo(paragrafo, pdf, largura_maxima))
    return linhas_totais, tamanho

def formatar_dados_cadastrais(dados):
    campos = [
        ("CPF/CNPJ", dados.get("cpf_cnpj", "")),
        ("Nome completo ou Razão Social", dados.get("nome_completo", "")),
        ("Nome Social", dados.get("nome_social", "")),
        ("E-mail", dados.get("email", "")),
        ("Telefone", dados.get("telefone", "")),
        ("CEP", dados.get("cep", "")),
        ("Logradouro", dados.get("logradouro", "")),
        ("Número", dados.get("numero", "")),
        ("Complemento", dados.get("complemento", "")),
        ("Bairro", dados.get("bairro", "")),
        ("Cidade", dados.get("cidade", "")),
        ("UF", dados.get("uf", "")),
    ]

    linhas = ["DADOS DO DEMANDANTE:\n"]
    for label, valor in campos:
        linhas.append(f"{label}: {valor}")
    linhas.append("\n")  # espaço antes da petição
    return "\n".join(linhas)

def gerar_pdf_com_cadastro(user_data, peticao, nome_arquivo="documento.pdf", titulo="Documento"):
    """
    Gera o PDF incluindo os dados cadastrais do demandante antes da petição.
    - user_data: dict com os dados cadastrais
    - peticao: texto da petição gerado pelo Gemini
    """
    pdf = PDF(titulo=titulo)

    fonte_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    if not os.path.isfile(fonte_path):
        raise FileNotFoundError(f"Fonte DejaVuSans.ttf não encontrada em {fonte_path}.")

    pdf.add_font("DejaVu", "", fonte_path, uni=True)
    pdf.add_font("DejaVu", "B", fonte_path, uni=True)
    pdf.add_font("DejaVu", "I", fonte_path, uni=True)

    pdf.add_page()

    largura_maxima = pdf.w - 2 * pdf.l_margin
    altura_maxima = pdf.h - pdf.t_margin - pdf.b_margin

    # Combina dados cadastrais com petição
    texto_final = formatar_dados_cadastrais(user_data) + peticao

    linhas, tamanho_final = ajustar_fonte_automaticamente(pdf, texto_final, largura_maxima, altura_maxima)

    pdf.set_font("DejaVu", size=tamanho_final)
    for linha in linhas:
        pdf.multi_cell(largura_maxima, 6, linha)
        pdf.ln(2)

    pdf.output(nome_arquivo)
    return nome_arquivo
