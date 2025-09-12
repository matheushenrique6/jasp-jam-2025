from pydantic import BaseModel
from typing import Optional

class QueixaOxidacaoData(BaseModel):
    # --- dados do demandante ---
    cpf_cnpj: Optional[str] = None
    nome_demandante: Optional[str] = None
    nome_social: Optional[str] = None
    email: Optional[str] = None
    confirmar_email: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[bool] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    # --- dados da queixa ---
    nome_autor: Optional[str] = None
    data_compra: Optional[str] = None
    produto: Optional[str] = None
    marca: Optional[str] = None
    valor_pago: Optional[float] = None
    loja: Optional[str] = None
    ordem_servico: Optional[str] = None
    data_ordem_servico: Optional[str] = None
    valor_indenizacao: Optional[float] = None
