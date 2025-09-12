from fpdf import FPDF
import os
import unicodedata
import re

def limpar_texto_seguro(texto):
    """
    Remove ou substitui caracteres que não podem ser renderizados.
    - Mantém letras, números, pontuação e acentos.
    - Substitui caracteres não suportados (como emojis) por '-'.
    """
    texto = unicodedata.normalize("NFKC", texto)
    texto = ''.join(c if ord(c) <= 0xFFFF else '-' for c in texto)
    texto = re.sub(r'[\x00-\x1F\x7F]', '', texto)
    return texto

def quebrar_linhas(texto, pdf, largura_maxima):
    """
    Quebra o texto em linhas que cabem na largura máxima da página,
    evitando erro "Not enough horizontal space".
    """
    linhas = []
    for paragrafo in texto.split("\n"):
        paragrafo = limpar_texto_seguro(paragrafo.strip())
        if not paragrafo:
            continue

        palavras = paragrafo.split(" ")
        linha_atual = ""
        for palavra in palavras:
            teste_linha = f"{linha_atual} {palavra}".strip()
            if pdf.get_string_width(teste_linha) <= largura_maxima:
                linha_atual = teste_linha
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                # palavra sozinha maior que largura_maxima, forçar quebra
                while pdf.get_string_width(palavra) > largura_maxima:
                    for i in range(1, len(palavra)+1):
                        if pdf.get_string_width(palavra[:i]) > largura_maxima:
                            linhas.append(palavra[:i-1])
                            palavra = palavra[i-1:]
                            break
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)
    return linhas

def gerar_pdf(texto, nome_arquivo="documento.pdf"):
    """
    Gera PDF UTF-8 robusto, quebrando linhas longas automaticamente.
    """
    pdf = FPDF()
    pdf.add_page()

    fonte_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    if not os.path.isfile(fonte_path):
        raise FileNotFoundError(
            f"Fonte DejaVuSans.ttf não encontrada em {fonte_path}. "
            "Coloque o arquivo no diretório do script."
        )

    pdf.add_font("DejaVu", "", fonte_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    max_width = pdf.w - 2 * pdf.l_margin

    for linha in quebrar_linhas(texto, pdf, max_width):
        pdf.multi_cell(max_width, 6, linha)

    pdf.output(nome_arquivo)
    return nome_arquivo
