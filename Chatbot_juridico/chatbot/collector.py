from pydantic import BaseModel
from typing import Optional

class QueixaOxidacaoData(BaseModel):
    nome_autor: Optional[str] = None
    data_compra: Optional[str] = None
    produto: Optional[str] = None
    marca: Optional[str] = None
    valor_pago: Optional[float] = None
    loja: Optional[str] = None
    ordem_servico: Optional[str] = None
    data_ordem_servico: Optional[str] = None
    valor_indenizacao: Optional[float] = None
