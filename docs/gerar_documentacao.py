# -*- coding: utf-8 -*-
"""
Gera o PDF unico de documentacao da GS (NutriMatch / CitizenTech).

Uso:   python docs/gerar_documentacao.py
Saida: docs/NutriMatch_Documentacao_GS.pdf

Edite as constantes INTEGRANTES, URL_GITHUB e URL_DEPLOY abaixo e gere novamente.
Dependencia: pip install reportlab
"""
import math
import os
import random

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

# ----------------------------------------------------------------------------------------------
# DADOS EDITAVEIS
# ----------------------------------------------------------------------------------------------
INTEGRANTES = [
    ("Erick Gabriel Ferreira dos Santos", "RM 565144"),
    ("Victor Henry Melchior Camara", "RM 564222"),
    ("Gabriel Akira Borges Kiyohara", "RM 565191"),
    ("Murilo Mendes Marques", "RM 564193"),
    ("Gustavo Francisco Santos", "RM 561820"),
]
SUBTITULO = "EcoQuiosque: transformando sobras de feira em acesso a alimento"
URL_GITHUB = "https://github.com/MuriloMendes7/cityzentech_GS.git"
URL_DEPLOY = "https://SEU-SERVICO.onrender.com   (substituir pelo link gerado no Render)"
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NutriMatch_Documentacao_GS.pdf")

ROSA = colors.HexColor("#E6007E")
ESCURO = colors.HexColor("#1A1A2E")
CINZA = colors.HexColor("#F2F2F6")
VERDE = colors.HexColor("#1E8E5A")

# ----------------------------------------------------------------------------------------------
# ESTILOS
# ----------------------------------------------------------------------------------------------
ss = getSampleStyleSheet()
corpo = ParagraphStyle("corpo", parent=ss["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15,
                       alignment=TA_JUSTIFY, spaceAfter=6)
peq = ParagraphStyle("peq", parent=corpo, fontSize=8.5, leading=11, alignment=0, spaceAfter=0)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=18, textColor=ESCURO,
                    spaceBefore=4, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, textColor=ROSA,
                    spaceBefore=7, spaceAfter=4)
cod = ParagraphStyle("cod", fontName="Courier", fontSize=7.6, leading=9.5, backColor=CINZA, borderPadding=6,
                     spaceAfter=8)
cap = ParagraphStyle("cap", parent=corpo, fontSize=8.5, textColor=colors.grey, alignment=TA_CENTER)
capa_t = ParagraphStyle("capa_t", fontName="Helvetica-Bold", fontSize=40, leading=44, textColor=colors.white,
                        alignment=TA_CENTER)
capa_s = ParagraphStyle("capa_s", fontName="Helvetica", fontSize=14, leading=19, textColor=colors.white,
                        alignment=TA_CENTER)
toc1 = ParagraphStyle("toc1", fontName="Helvetica-Bold", fontSize=11, leading=20, leftIndent=0)
toc2 = ParagraphStyle("toc2", fontName="Helvetica", fontSize=9.5, leading=16, leftIndent=18)
bul = ParagraphStyle("b", parent=corpo, leftIndent=14, firstLineIndent=-10, spaceAfter=2, alignment=0)


def P(t, s=corpo):
    return Paragraph(t, s)


def C(t):
    return "<font face='Courier'>%s</font>" % t


def bullets(itens):
    return [Paragraph("&bull;&nbsp;&nbsp;" + i, bul) for i in itens]


def tabela(dados, larguras, cab=True, fs=8.3, zebra=True):
    linhas = [[Paragraph(str(c), ParagraphStyle("t", parent=peq, fontSize=fs, leading=fs + 2.5,
                                                 textColor=colors.white if (cab and i == 0) else colors.black,
                                                 fontName="Helvetica-Bold" if (cab and i == 0) else "Helvetica"))
               for c in lin] for i, lin in enumerate(dados)]
    t = Table(linhas, colWidths=larguras, repeatRows=1 if cab else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C8C8D0")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if cab:
        est.append(("BACKGROUND", (0, 0), (-1, 0), ESCURO))
    if zebra:
        for r in range(1 if cab else 0, len(dados)):
            if r % 2 == 0:
                est.append(("BACKGROUND", (0, r), (-1, r), CINZA))
    t.setStyle(TableStyle(est))
    return t


# ----------------------------------------------------------------------------------------------
# DESENHOS (diagrama de classes, DER, wireframes)
# ----------------------------------------------------------------------------------------------
class Desenho(Flowable):
    def __init__(self, w, h, fn, escala=1.0):
        super().__init__()
        self.w, self.h, self.fn, self.escala = w, h, fn, escala

    def wrap(self, aw, ah):
        return self.w * self.escala, self.h * self.escala

    def draw(self):
        self.canv.scale(self.escala, self.escala)
        self.fn(self.canv)


def caixa_classe(c, x, y, w, titulo, atrib, metodos=(), estereotipo=None, cor=colors.HexColor("#FFF0F8")):
    """Classe UML com (x,y) = canto superior esquerdo. Retorna altura total."""
    lh = 10.5
    cab_h = 24 if estereotipo else 15
    h = cab_h + len(atrib) * lh + 6 + (len(metodos) * lh + 6 if metodos else 0)
    c.setFillColor(cor)
    c.setStrokeColor(ESCURO)
    c.setLineWidth(0.9)
    c.rect(x, y - h, w, h, fill=1)
    c.setFillColor(ESCURO)
    c.rect(x, y - cab_h, w, cab_h, fill=1)
    c.setFillColor(colors.white)
    if estereotipo:
        c.setFont("Helvetica-Oblique", 7.3)
        c.drawCentredString(x + w / 2, y - 9, estereotipo)
        c.setFont("Helvetica-Bold", 9.2)
        c.drawCentredString(x + w / 2, y - 20, titulo)
    else:
        c.setFont("Helvetica-Bold", 9.2)
        c.drawCentredString(x + w / 2, y - 11, titulo)
    c.setFillColor(colors.black)
    c.setFont("Courier", 7.0)
    yy = y - cab_h - 9
    for a in atrib:
        c.drawString(x + 4, yy, a)
        yy -= lh
    if metodos:
        c.setStrokeColor(ESCURO)
        c.line(x, yy + 7, x + w, yy + 7)
        yy -= 1
        for m in metodos:
            c.drawString(x + 4, yy, m)
            yy -= lh
    return h


def linha(c, pts, dash=False, seta=False):
    c.setStrokeColor(ESCURO)
    c.setLineWidth(0.9)
    c.setDash(3, 2) if dash else c.setDash()
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, stroke=1, fill=0)
    c.setDash()
    if seta:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        a = math.atan2(y2 - y1, x2 - x1)
        s = 6
        c.setFillColor(ESCURO)
        pa = c.beginPath()
        pa.moveTo(x2, y2)
        pa.lineTo(x2 - s * math.cos(a - 0.4), y2 - s * math.sin(a - 0.4))
        pa.lineTo(x2 - s * math.cos(a + 0.4), y2 - s * math.sin(a + 0.4))
        pa.close()
        c.drawPath(pa, fill=1, stroke=0)


def diagrama_classes(c):
    # Linha superior: Controller -> BO -> DAO
    caixa_classe(c, 0, 580, 160, "CabazController",
                 ["- CabazBO cabazBO"],
                 ["+ cadastrar(CabazDTO)", "+ consultar(String)", "+ consultarPorCodigo(Long)",
                  "+ atualizar(Long, CabazDTO)", "+ reservar(Long)", "+ retirar(String)", "+ excluir(Long)"],
                 estereotipo="<<@RestController>>", cor=colors.HexColor("#FFF0F8"))
    caixa_classe(c, 180, 580, 165, "CabazBO",
                 ["- CabazDAO cabazDAO", "+ PRECO_MAXIMO_SIMBOLICO"],
                 ["+ consultar(String)", "+ consultarPorCodigo(Long)", "+ cadastrar(CabazDTO)",
                  "+ atualizar(Long, CabazDTO)", "+ reservar(Long)", "+ retirar(String)", "+ excluir(Long)"],
                 estereotipo="<<@Service>>", cor=colors.HexColor("#F0F4FF"))
    caixa_classe(c, 365, 580, 135, "CabazDAO",
                 [],
                 ["+ findByCodigo(Long)", "+ findByStatus(String)", "+ findByCodigoQr(String)",
                  "+ (JpaRepository)"],
                 estereotipo="<<interface JpaRepository>>", cor=colors.HexColor("#EEF7F1"))

    # Setas Controller -> BO -> DAO
    linha(c, [(160, 515), (180, 515)], seta=True)
    linha(c, [(345, 515), (365, 515)], seta=True)

    # Linha do meio: Entidade Cabaz + CabazDTO
    caixa_classe(c, 0, 410, 240, "Cabaz",
                 ["- Long codigo", "- String titulo", "- String categoria", "- Double pesoKg", "- Double preco",
                  "- String quiosque", "- String feirante", "- Boolean gratuitoOng", "- String status",
                  "- String codigoQr", "- LocalDate dataPublicacao", "- String urlImagem"],
                 ["+ Cabaz()", "+ Cabaz(CabazDTO)", "+ atualizar(CabazDTO)", "+ getters / setters"],
                 estereotipo="<<@Entity dddj_cabazes>>", cor=colors.HexColor("#FFF8E6"))

    caixa_classe(c, 265, 410, 235, "CabazDTO",
                 ["+ String titulo  (@NotBlank)", "+ String categoria  (@NotBlank)", "+ Double pesoKg  (@Positive)",
                  "+ Double preco  (@PositiveOrZero)", "+ String quiosque  (@NotBlank)",
                  "+ String feirante  (@NotBlank)", "+ Boolean gratuitoOng  (@NotNull)",
                  "+ LocalDate dataPublicacao (@PastOrPresent)", "+ String urlImagem"],
                 [], estereotipo="<<record>>", cor=colors.HexColor("#FFF8E6"))

    # Associacao Cabaz <- CabazDTO e DAO -> Cabaz
    linha(c, [(265, 340), (240, 340)], dash=True, seta=True)
    linha(c, [(432, 502), (432, 430), (120, 430), (120, 410)], dash=True, seta=True)

    # Linha inferior: Camada de Excecoes
    caixa_classe(c, 0, 178, 240, "GlobalExceptionHandler",
                 [],
                 ["+ tratarNaoEncontrado (404)", "+ tratarRegraNegocio (422)", "+ tratarValidacao (400)",
                  "+ tratarJsonInvalido (400)", "+ tratarTipoInvalido (400)", "+ tratarMetodoNaoSuportado (405)",
                  "+ tratarIntegridade (409)", "+ tratarErroGenerico (500)"],
                 estereotipo="<<@RestControllerAdvice>>", cor=colors.HexColor("#FFF0F8"))

    caixa_classe(c, 265, 178, 235, "Excecoes de Dominio",
                 ["RecursoNaoEncontradoException (404)", "RegraNegocioException (422)"],
                 [], estereotipo="<<RuntimeException>>", cor=colors.HexColor("#F0F4FF"))

    caixa_classe(c, 265, 112, 235, "ErroResponse",
                 ["+ LocalDateTime timestamp", "+ int status", "+ String erro", "+ String mensagem",
                  "+ String path", "+ List<String> detalhes"],
                 [], estereotipo="<<record>>", cor=colors.HexColor("#EEF7F1"))

    linha(c, [(240, 150), (265, 150)], dash=True, seta=True)
    linha(c, [(240, 76), (265, 76)], dash=True, seta=True)


def diagrama_der(c):
    # Tabela fisica Oracle DDDJ_CABAZES em detalhe
    x, y, w = 85, 255, 330
    cols = [
        ("PK", "codigo", "NUMBER (IDENTITY)  NOT NULL"),
        ("", "titulo", "VARCHAR2(120)  NOT NULL"),
        ("", "categoria", "VARCHAR2(60)  NOT NULL"),
        ("", "peso_kg", "FLOAT(53)  NOT NULL"),
        ("", "preco", "FLOAT(53)  NOT NULL"),
        ("", "quiosque", "VARCHAR2(120)  NOT NULL"),
        ("", "feirante", "VARCHAR2(120)  NOT NULL"),
        ("", "gratuito_ong", "NUMBER(1)  NOT NULL  (0 ou 1)"),
        ("", "status", "VARCHAR2(20)  NOT NULL"),
        ("UK", "codigo_qr", "VARCHAR2(36)  NULL (unico)"),
        ("", "data_publicacao", "DATE  NOT NULL"),
        ("", "url_imagem", "VARCHAR2(255)  NULL"),
    ]
    lh = 15.5
    h = 24 + len(cols) * lh + 8
    c.setFillColor(colors.white)
    c.setStrokeColor(ESCURO)
    c.setLineWidth(1.2)
    c.rect(x, y - h, w, h, fill=1)
    c.setFillColor(ROSA)
    c.rect(x, y - 24, w, 24, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + w / 2, y - 16, "DDDJ_CABAZES")
    yy = y - 24 - 13
    for tag, col, tipo in cols:
        c.setFillColor(ROSA if tag else colors.black)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 8, yy, tag)
        c.setFillColor(colors.black)
        c.setFont("Courier-Bold", 8.5)
        c.drawString(x + 34, yy, col)
        c.setFillColor(colors.HexColor("#444444"))
        c.setFont("Courier", 7.8)
        c.drawRightString(x + w - 8, yy, tipo)
        yy -= lh
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawCentredString(x + w / 2, y - h - 18,
                        "PK = Chave Primaria (Identity)    |    UK = Chave Unica    |    status IN ('DISPONIVEL', 'RESERVADO', 'RETIRADO')")


# ---------------- Wireframes -----------------------------------------------------------------
def moldura(c, x, y, w, h, titulo, totem=False):
    c.setFillColor(colors.HexColor("#FAFAFC"))
    c.setStrokeColor(ESCURO)
    c.setLineWidth(1.4)
    c.roundRect(x, y, w, h, 12 if not totem else 5, fill=1)
    c.setFillColor(ESCURO)
    c.rect(x + 1, y + h - 22, w - 2, 21, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(x + w / 2, y + h - 15, titulo)


def botao(c, x, y, w, h, t, cor=ROSA, tc=colors.white):
    c.setFillColor(cor)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=0)
    c.setFillColor(tc)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x + w / 2, y + h / 2 - 2.5, t)


def campo(c, x, y, w, rot, val=""):
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 6.5)
    c.drawString(x, y + 14, rot)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#999999"))
    c.setLineWidth(0.7)
    c.rect(x, y, w, 12, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawString(x + 3, y + 3.5, val)


def qr(c, x, y, s):
    random.seed(7)
    n = 17
    cell = s / n
    c.setFillColor(colors.black)
    for i in range(n):
        for j in range(n):
            canto = (i < 5 and j < 5) or (i < 5 and j > n - 6) or (i > n - 6 and j < 5)
            if canto:
                ii = i if i < 5 else i - (n - 5)
                jj = j if j < 5 else j - (n - 5)
                if ii in (0, 4) or jj in (0, 4) or (ii == 2 and jj == 2):
                    c.rect(x + j * cell, y + (n - 1 - i) * cell, cell, cell, fill=1, stroke=0)
            elif random.random() > 0.5:
                c.rect(x + j * cell, y + (n - 1 - i) * cell, cell, cell, fill=1, stroke=0)


def tela1(c):
    x, y, w, h = 0, 0, 235, 300
    moldura(c, x, y, w, h, "TELA 1 - Totem EcoQuiosque (feirante)", totem=True)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 12, y + h - 40, "Deposite as sobras na balanca IoT")
    c.setFillColor(colors.HexColor("#E8F6EE"))
    c.setStrokeColor(VERDE)
    c.roundRect(x + 12, y + h - 92, w - 24, 42, 6, fill=1)
    c.setFillColor(VERDE)
    c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(x + w / 2, y + h - 76, "4,5 kg")
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(x + w / 2, y + h - 88, "pesoKg registrado automaticamente pela balanca")
    campo(c, x + 12, y + h - 130, w - 24, "Titulo do cabaz", "Cabaz Surpresa de Verduras")
    campo(c, x + 12, y + h - 163, 100, "Categoria", "Hortifruti")
    campo(c, x + 123, y + h - 163, 100, "Feirante", "Banca da Maria")
    campo(c, x + 12, y + h - 196, 100, "Preco simbolico (<= R$10)", "R$ 5,00")
    campo(c, x + 123, y + h - 196, 100, "Gratuito para ONG?", "[ ] Sim  [X] Nao")
    botao(c, x + 12, y + 22, w - 24, 26, "PUBLICAR CABAZ SURPRESA")
    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(x + 12, y + 10, "POST /cabazes   |   PUT /cabazes/{codigo}")


def tela2(c):
    x, y, w, h = 0, 0, 235, 300
    moldura(c, x, y, w, h, "TELA 2 - App: Cabazes disponiveis")
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#999999"))
    c.rect(x + 10, y + h - 50, w - 20, 15, fill=1)
    c.setFillColor(colors.HexColor("#888888"))
    c.setFont("Helvetica", 7)
    c.drawString(x + 14, y + h - 45.5, "Filtrar por status: [DISPONIVEL v]")
    itens = [("Cabaz de Verduras", "EQ-001 Mercado Central", "4,5 kg", "R$ 5,00"),
             ("Cabaz Solidario Frutas", "EQ-002 Feira da Vila", "6,0 kg", "Gratis (ONG)"),
             ("Cabaz Paes e Massas", "EQ-001 Mercado Central", "3,2 kg", "R$ 4,00")]
    yy = y + h - 62
    for t, l, p, v in itens:
        yy -= 62
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#BBBBBB"))
        c.roundRect(x + 10, yy, w - 20, 56, 5, fill=1)
        c.setFillColor(colors.HexColor("#DDDDE6"))
        c.rect(x + 15, yy + 8, 38, 40, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 60, yy + 40, t)
        c.setFont("Helvetica", 6.7)
        c.drawString(x + 60, yy + 29, l + " - " + p)
        c.setFillColor(VERDE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 60, yy + 16, v)
        botao(c, x + w - 70, yy + 8, 54, 17, "RESERVAR")
    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(x + 10, y + 10, "GET /cabazes?status=DISPONIVEL   |   PUT /cabazes/{codigo}/reservar")


def tela3(c):
    x, y, w, h = 0, 0, 235, 300
    moldura(c, x, y, w, h, "TELA 3 - App: Reserva e QR Code")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 12, y + h - 42, "Cabaz Surpresa de Verduras")
    c.setFont("Helvetica", 7)
    c.drawString(x + 12, y + h - 53, "EcoQuiosque EQ-001 - Mercado Central")
    c.drawString(x + 12, y + h - 63, "Peso: 4,5 kg   |   Preco: R$ 5,00   |   Status: RESERVADO")
    qr(c, x + w / 2 - 55, y + h - 185, 110)
    c.setFont("Helvetica", 6.3)
    c.drawCentredString(x + w / 2, y + h - 197, "codigoQr: 3f0a9c2e-....-b81d")
    botao(c, x + 12, y + 40, w - 24, 24, "APRESENTAR NO ECOQUIOSQUE")
    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(x + 12, y + 10, "GET /cabazes/{codigo}   |   PUT /cabazes/{codigo}/reservar")


def tela4(c):
    x, y, w, h = 0, 0, 235, 300
    moldura(c, x, y, w, h, "TELA 4 - Totem: Retirada por QR Code", totem=True)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 12, y + h - 40, "Aproxime o QR Code na leitora")
    c.setStrokeColor(ROSA)
    c.setDash(3, 2)
    c.rect(x + 12, y + h - 122, 100, 74)
    c.setDash()
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawCentredString(x + 62, y + h - 87, "[ leitora QR ]")
    c.setFillColor(colors.black)
    campo(c, x + 122, y + h - 92, 101, "ou digite codigoQr", "3f0a9c2e-...")
    botao(c, x + 122, y + h - 122, 101, 22, "CONFIRMAR RETIRADA")
    c.setFillColor(colors.HexColor("#E8F6EE"))
    c.setStrokeColor(VERDE)
    c.roundRect(x + 12, y + 42, w - 24, 88, 6, fill=1)
    c.setFillColor(VERDE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x + 20, y + 114, "RETIRADA CONFIRMADA!")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7.3)
    c.drawString(x + 20, y + 96, "Cabaz #1 - Cabaz Surpresa de Verduras")
    c.drawString(x + 20, y + 82, "Peso salvo do desperdicio: 4,5 kg")
    c.drawString(x + 20, y + 68, "Novo status: RETIRADO  (ODS 2, 10 e 11)")
    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(x + 12, y + 10, "PUT /cabazes/retirar/{codigoQr}   |   DELETE /cabazes/{codigo}")


def grade_telas(c):
    for fn, (tx, ty) in ((tela1, (0, 305)), (tela2, (255, 305)), (tela3, (0, 0)), (tela4, (255, 0))):
        c.saveState()
        c.translate(tx, ty)
        fn(c)
        c.restoreState()


# ----------------------------------------------------------------------------------------------
# DOCUMENTO
# ----------------------------------------------------------------------------------------------
class Doc(BaseDocTemplate):
    def __init__(self, nome, **kw):
        super().__init__(nome, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.2 * cm,
                         bottomMargin=2 * cm, title="NutriMatch - Documentacao GS 2026.2",
                         author="CitizenTech - FIAP", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([
            PageTemplate(id="capa", frames=[frame], onPage=self.pagina_capa),
            PageTemplate(id="miolo", frames=[frame], onPage=self.pagina_miolo)])

    def pagina_capa(self, c, d):
        w, h = A4
        c.setFillColor(ESCURO)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(ROSA)
        c.rect(0, h - 14, w, 14, fill=1, stroke=0)
        c.rect(0, 0, w, 14, fill=1, stroke=0)

    def pagina_miolo(self, c, d):
        w, h = A4
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(2.2 * cm, 1.1 * cm, "FIAP - Global Solution 2026.2 - Domain Driven Design (Java) - NutriMatch")
        c.drawRightString(w - 2.2 * cm, 1.1 * cm, "Pagina %d" % d.page)
        c.setStrokeColor(ROSA)
        c.setLineWidth(1.2)
        c.line(2.2 * cm, h - 1.5 * cm, w - 2.2 * cm, h - 1.5 * cm)

    def afterFlowable(self, f):
        if isinstance(f, Paragraph):
            if f.style.name == "h1":
                self.notify("TOCEntry", (0, f.getPlainText(), self.page))
            elif f.style.name == "h2":
                self.notify("TOCEntry", (1, f.getPlainText(), self.page))


def construir():
    s = []

    # ------------------------------ CAPA ------------------------------
    s += [Spacer(1, 2.4 * cm), P("FIAP - Global Solution 2026.2", capa_s), Spacer(1, 0.3 * cm),
          P("Domain Driven Design - Java", capa_s), Spacer(1, 1.8 * cm),
          P("NUTRI<font color='#E6007E'>MATCH</font>", capa_t), Spacer(1, 0.4 * cm), P(SUBTITULO, capa_s),
          Spacer(1, 0.5 * cm), P("CitizenTech - Tecnologia para pessoas", capa_s), Spacer(1, 2.2 * cm)]
    st1 = ParagraphStyle("i", fontName="Helvetica-Bold", fontSize=10.5, textColor=colors.white, alignment=TA_CENTER)
    st2 = ParagraphStyle("i2", fontName="Helvetica", fontSize=10.5, textColor=colors.white, alignment=TA_CENTER)
    t = Table([[Paragraph(n, st1), Paragraph(rm, st2)] for n, rm in INTEGRANTES], colWidths=[10.0 * cm, 3.2 * cm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, ROSA), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    s += [t, NextPageTemplate("miolo"), PageBreak()]

    # ------------------------------ INDICE ------------------------------
    s.append(P("Sumario", ParagraphStyle("sumario", parent=h1)))
    toc = TableOfContents()
    toc.levelStyles = [toc1, toc2]
    s += [toc, PageBreak()]

    # ------------------------------ 1. SOLUCAO ------------------------------
    s.append(P("1. Descritivo da solucao", h1))
    s.append(P(
        "O <b>NutriMatch</b> e uma plataforma que conecta o desperdicio de alimentos de mercados e feiras a quem "
        "mais precisa deles. A solucao e composta por um <b>EcoQuiosque</b> (totem de autoatendimento com balanca "
        "IoT acoplada) instalado em mercados e feiras, por uma <b>API RESTful</b> (este projeto, desenvolvido em "
        "Java com Spring Boot e banco de dados Oracle da FIAP) e por um aplicativo movel para os cidadaos."))
    s.append(P(
        "No final do dia, o feirante coloca as sobras na balanca do EcoQuiosque. O sistema registra o peso "
        "automaticamente e publica um <b>Cabaz Surpresa</b> na plataforma a preco simbolico (ou gratuito para ONGs "
        "verificadas). Os cidadaos da regiao visualizam os cabazes disponiveis no aplicativo, realizam a reserva "
        "(que gera um <b>QR Code</b> unico) e retiram o cabaz no quiosque."))
    s.append(P("Fluxo principal", h2))
    s += bullets([
        "<b>Publicacao (EcoQuiosque):</b> feirante pesa as sobras e publica o cabaz via %s." % C("POST /cabazes"),
        "<b>Descoberta (App):</b> cidadao ou ONG lista cabazes disponiveis via %s."
        % C("GET /cabazes?status=DISPONIVEL"),
        "<b>Reserva (App):</b> usuario reserva o cabaz via %s e recebe o %s gerado automaticamente."
        % (C("PUT /cabazes/{codigo}/reservar"), C("codigoQr")),
        "<b>Retirada (EcoQuiosque):</b> o totem le o QR Code e confirma a retirada via %s."
        % C("PUT /cabazes/retirar/{codigoQr}")])
    s.append(P("Regras de negocio (camada BO)", h2))
    s += bullets([
        "O preco do cabaz e <b>simbolico</b>: no maximo R$ 10,00 (regra validada em %s)." % C("CabazBO"),
        "Se %s for %s, o sistema garante %s (gratuito para ONGs verificadas)."
        % (C("gratuitoOng"), C("true"), C("preco = 0.0")),
        "Todo cabaz nasce com status <b>DISPONIVEL</b> e %s nulo." % C("codigoQr"),
        "Somente cabazes <b>DISPONIVEIS</b> podem ser editados (%s) ou reservados (%s)."
        % (C("PUT /cabazes/{codigo}"), C("PUT /cabazes/{codigo}/reservar")),
        "Ao reservar, o status muda para <b>RESERVADO</b> e um %s (UUID) unico e gerado." % C("codigoQr"),
        "Ao retirar pelo QR Code, somente cabazes <b>RESERVADOS</b> podem passar para <b>RETIRADO</b>.",
        "Cabazes com status <b>RESERVADO</b> nao podem ser excluidos (HTTP 422)."])

    s.append(P("2. Justificativa", h1))
    s.append(P(
        "Toneladas de alimentos proprios para consumo sao descartadas diariamente em feiras e mercados enquanto "
        "milhoes de pessoas convivem com a inseguranca alimentar. O NutriMatch parte desse problema real do "
        "cotidiano (tema <b>CitizenTech - Tecnologia para pessoas</b> da Global Solution 2026.2) para aproximar "
        "quem tem excedente de quem precisa, usando a balanca IoT do EcoQuiosque, uma API simples e confiavel e a "
        "retirada rastreavel por QR Code."))

    s.append(PageBreak())
    s.append(P("3. Objetivos do projeto", h1))
    s.append(P("Objetivo geral", h2))
    s.append(P("Reduzir o desperdicio de alimentos em feiras e mercados e ampliar o acesso a alimentacao digna por "
               "meio da publicacao, reserva e retirada de cabazes surpresa a preco simbolico (ou gratuito para ONGs)."))
    s.append(P("Objetivos especificos", h2))
    s += bullets([
        "Disponibilizar uma API RESTful em Java (Spring Boot) seguindo os padroes trabalhados em aula.",
        "Estruturar a aplicacao nas camadas Model (Entity e DTO), DAO, BO, Controller e Tratamento de Excecoes.",
        "Persistir os cabazes no banco de dados Oracle da FIAP (tabela %s)." % C("DDDJ_CABAZES"),
        "Publicar a aplicacao em nuvem via Docker no servidor Render.com."])
    s.append(P("Alinhamento com os ODS", h2))
    s.append(tabela([
        ["ODS", "Contribuicao do NutriMatch"],
        ["<b>2 - Fome Zero e Agricultura Sustentavel</b>", "Redireciona sobras proprias para consumo a quem precisa."],
        ["<b>10 - Reducao das Desigualdades</b>", "Preco simbolico (ate R$ 10,00) e gratuidade para ONGs verificadas."],
        ["<b>11 - Cidades e Comunidades Sustentaveis</b>", "Reduz residuos organicos urbanos em mercados e feiras."]],
        [5.6 * cm, 11 * cm]))
    s.append(PageBreak())

    # ------------------------------ 4. ARQUITETURA ------------------------------
    s.append(P("4. Arquitetura e tecnologias", h1))
    s.append(P(
        "O projeto foi refatorado diretamente a partir do projeto base <i>Pokemon</i> desenvolvido em aula "
        "(Spring Boot 3.2.5, Java 21, Spring Data JPA, Bean Validation, Oracle FIAP via variaveis de ambiente e "
        "Dockerfile para o Render), adaptado para uma API RESTful com as camadas <b>Controller</b>, <b>BO</b>, "
        "<b>DAO</b>, <b>Model</b> e <b>Exception</b>."))
    s.append(tabela([
        ["Pacote (br.com.fiap)", "Classes e responsabilidade"],
        [C("controller"), C("CabazController") + ": endpoints REST (GET, POST, PUT, DELETE) em /cabazes."],
        [C("model.bo"), C("CabazBO") + ": regras de negocio e controle transacional (@Service)."],
        [C("model.dao"), C("CabazDAO") + ": acesso ao Oracle via Spring Data JPA (JpaRepository)."],
        [C("model.entity"), C("Cabaz") + ": entidade JPA mapeada para a tabela DDDJ_CABAZES."],
        [C("model.dto"), C("CabazDTO") + ": record de entrada com Bean Validation (@NotBlank, @Positive, etc.)."],
        [C("exception"), C("GlobalExceptionHandler") + ", " + C("ErroResponse") + ", "
                         + C("RecursoNaoEncontradoException") + ", " + C("RegraNegocioException") + "."]],
        [4.5 * cm, 12.1 * cm]))

    s.append(P("Tratamento de excecoes", h2))
    s.append(tabela([
        ["Situacao", "Excecao", "HTTP"],
        ["Codigo ou QR Code nao encontrado", "RecursoNaoEncontradoException", "404 Not Found"],
        ["Regra de negocio violada (ex.: preco > R$ 10)", "RegraNegocioException", "422 Unprocessable Entity"],
        ["Bean Validation, JSON invalido ou parametro invalido",
         "MethodArgumentNotValidException, HttpMessageNotReadableException, MethodArgumentTypeMismatchException",
         "400 Bad Request"],
        ["Metodo HTTP nao suportado", "HttpRequestMethodNotSupportedException", "405 Method Not Allowed"],
        ["Conflito de integridade no banco", "DataIntegrityViolationException", "409 Conflict"],
        ["Erro inesperado", "Exception", "500 Internal Server Error"]], [6 * cm, 7.4 * cm, 3.2 * cm]))
    s.append(P("Corpo JSON padrao retornado em erros (%s):" % C("ErroResponse"), corpo))
    s.append(Preformatted(
        '{\n  "timestamp": "2026-11-18T23:15:10.214",\n  "status": 422,\n  "erro": "Unprocessable Entity",\n'
        '  "mensagem": "O preco do cabaz deve ser simbolico (maximo R$ 10,00)",\n'
        '  "path": "/cabazes",\n  "detalhes": []\n}', cod))
    s.append(PageBreak())

    # ------------------------------ 5. DIAGRAMA DE CLASSES ------------------------------
    s.append(P("5. Diagrama de Classes", h1))
    s.append(P("Diagrama completo refletindo fielmente as classes Java do pacote %s (Controller, BO, DAO, Entity, "
               "DTO e Exception)." % C("br.com.fiap")))
    s.append(Desenho(500, 595, diagrama_classes, 0.94))
    s.append(P("Figura 1 - Diagrama de classes do projeto NutriMatch (CitizenTech).", cap))
    s.append(PageBreak())

    # ------------------------------ 6. DER ------------------------------
    s.append(P("6. Diagrama Entidade-Relacionamento (DER)", h1))
    s.append(P("Banco de dados <b>Oracle (FIAP)</b>. A tabela %s segue a convencao do projeto base Pokemon e e "
               "gerada automaticamente pelo Hibernate (%s). O script SQL equivalente esta em %s."
               % (C("DDDJ_CABAZES"), C("ddl-auto=update"), C("docs/ddl-oracle.sql"))))
    s.append(Spacer(1, 0.5 * cm))
    s.append(Desenho(500, 270, diagrama_der, 1.0))
    s.append(P("Figura 2 - Diagrama Entidade-Relacionamento da tabela DDDJ_CABAZES (Oracle).", cap))
    s.append(P("Dicionario de colunas", h2))
    s.append(tabela([
        ["Coluna", "Tipo Oracle", "Obrigatoria", "Descricao"],
        [C("codigo"), "NUMBER (IDENTITY)", "Sim (PK)", "Identificador sequencial unico do cabaz."],
        [C("titulo"), "VARCHAR2(120)", "Sim", "Nome resumido do cabaz surpresa."],
        [C("categoria"), "VARCHAR2(60)", "Sim", "Categoria dos alimentos (Hortifruti, Frutas, Padaria...)."],
        [C("peso_kg"), "FLOAT(53)", "Sim", "Peso em kg capturado pela balanca IoT do EcoQuiosque."],
        [C("preco"), "FLOAT(53)", "Sim", "Preco simbolico em R$ (0.0 quando gratuito para ONG)."],
        [C("quiosque"), "VARCHAR2(120)", "Sim", "Identificacao/local do EcoQuiosque."],
        [C("feirante"), "VARCHAR2(120)", "Sim", "Feirante ou banca que depositou as sobras."],
        [C("gratuito_ong"), "NUMBER(1)", "Sim", "1 = gratuito para ONG verificada; 0 = preco simbolico."],
        [C("status"), "VARCHAR2(20)", "Sim", "Ciclo de vida: DISPONIVEL, RESERVADO ou RETIRADO."],
        [C("codigo_qr"), "VARCHAR2(36)", "Nao (UK)", "UUID gerado na reserva para retirada no totem."],
        [C("data_publicacao"), "DATE", "Sim", "Data em que o cabaz foi publicado."],
        [C("url_imagem"), "VARCHAR2(255)", "Nao", "URL opcional da foto do cabaz."]],
        [3.1 * cm, 3.4 * cm, 2.2 * cm, 7.9 * cm], fs=7.8))
    s.append(PageBreak())

    # ------------------------------ 7. PROTOTIPOS ------------------------------
    s.append(P("7. Prototipos de tela (front-end)", h1))
    s.append(P("Prototipos de baixa fidelidade das telas do EcoQuiosque (totem) e do aplicativo movel que consomem "
               "os endpoints da API RESTful."))
    s.append(Desenho(490, 610, grade_telas, 0.82))
    s.append(P("Figura 3 - Prototipos das telas (Totem e App) com os endpoints utilizados.", cap))
    s.append(P("Relacao telas x endpoints", h2))
    s.append(tabela([
        ["Tela", "Endpoints consumidos"],
        ["1 - Totem: publicar cabaz", "POST /cabazes, PUT /cabazes/{codigo}"],
        ["2 - App: listar cabazes disponiveis", "GET /cabazes?status=DISPONIVEL, PUT /cabazes/{codigo}/reservar"],
        ["3 - App: reserva e QR Code", "GET /cabazes/{codigo}, PUT /cabazes/{codigo}/reservar"],
        ["4 - Totem: retirada por QR Code", "PUT /cabazes/retirar/{codigoQr}, DELETE /cabazes/{codigo}"]],
        [5.5 * cm, 11.1 * cm]))
    s.append(PageBreak())

    # ------------------------------ 8. ENDPOINTS ------------------------------
    s.append(P("8. Tabela de endpoints", h1))
    s.append(P("URL base local: %s. Formato JSON. Colecao pronta para importar no Insomnia em %s."
               % (C("http://localhost:8080"), C("insomnia/citizentech-insomnia.json"))))
    E = [
        ["Metodo", "Endpoint", "Descricao", "Sucesso", "Erros"],
        ["POST", "/cabazes", "Publica um novo cabaz (nasce DISPONIVEL)", "201 Created", "400, 422"],
        ["GET", "/cabazes", "Lista todos os cabazes cadastrados", "200 OK", "-"],
        ["GET", "/cabazes?status=DISPONIVEL", "Filtra por status (DISPONIVEL, RESERVADO, RETIRADO)", "200 OK", "422"],
        ["GET", "/cabazes/{codigo}", "Busca um cabaz pelo codigo", "200 OK", "400, 404"],
        ["PUT", "/cabazes/{codigo}", "Atualiza um cabaz DISPONIVEL", "200 OK", "400, 404, 422"],
        ["PUT", "/cabazes/{codigo}/reservar", "Reserva o cabaz e gera codigoQr (UUID)", "200 OK", "404, 422"],
        ["PUT", "/cabazes/retirar/{codigoQr}", "Confirma a retirada no EcoQuiosque via QR", "200 OK", "404, 422"],
        ["DELETE", "/cabazes/{codigo}", "Exclui um cabaz (nao permite se RESERVADO)", "204 No Content", "404, 422"],
    ]
    s.append(tabela(E, [1.6 * cm, 4.9 * cm, 5.5 * cm, 2.3 * cm, 2.3 * cm], fs=7.8))

    s.append(P("Exemplos de requisicao e resposta (JSON)", h2))
    s.append(Preformatted(
        'POST /cabazes  (e tambem PUT /cabazes/1)\n'
        '{\n'
        '  "titulo": "Cabaz Surpresa de Verduras",\n'
        '  "categoria": "Hortifruti",\n'
        '  "pesoKg": 4.5,\n'
        '  "preco": 5.0,\n'
        '  "quiosque": "EcoQuiosque EQ-001 - Mercado Central",\n'
        '  "feirante": "Banca da Maria",\n'
        '  "gratuitoOng": false,\n'
        '  "dataPublicacao": "2026-11-18",\n'
        '  "urlImagem": "https://exemplo.com/cabaz-verduras.png"\n'
        '}\n\n'
        'Resposta 201 Created:\n'
        '{\n'
        '  "codigo": 1,\n'
        '  "titulo": "Cabaz Surpresa de Verduras",\n'
        '  "categoria": "Hortifruti",\n'
        '  "pesoKg": 4.5,\n'
        '  "preco": 5.0,\n'
        '  "quiosque": "EcoQuiosque EQ-001 - Mercado Central",\n'
        '  "feirante": "Banca da Maria",\n'
        '  "gratuitoOng": false,\n'
        '  "status": "DISPONIVEL",\n'
        '  "codigoQr": null,\n'
        '  "dataPublicacao": "2026-11-18",\n'
        '  "urlImagem": "https://exemplo.com/cabaz-verduras.png"\n'
        '}', cod))
    s.append(PageBreak())

    # ------------------------------ 9. INSTRUCOES ------------------------------
    bul9 = ParagraphStyle("b9", parent=bul, fontSize=9.6, leading=13.2, spaceAfter=1.5)
    b9 = lambda itens: [Paragraph("&bull;&nbsp;&nbsp;" + i, bul9) for i in itens]
    s.append(P("9. Instrucoes para executar o projeto", h1))
    s.append(P("Ferramentas utilizadas", h2))
    s += b9([
        "<b>IntelliJ IDEA</b> (IDE), <b>Maven Wrapper</b> (%s incluso) e <b>Git / GitHub</b>." % C("mvnw"),
        "<b>Insomnia</b> para testar os endpoints REST; <b>Docker</b> e <b>Render.com</b> para o deploy; "
        "<b>Oracle SQL Developer</b> (opcional) para consultar a tabela."])
    s.append(P("Versoes necessarias", h2))
    s.append(tabela([
        ["Item", "Versao"],
        ["Java JDK", "21 (LTS)"],
        ["Spring Boot", "3.2.5 (Web, Data JPA, Bean Validation)"],
        ["Banco de dados", "Oracle (FIAP) - driver ojdbc11"],
        ["Maven", "Wrapper incluso (%s)" % C("./mvnw")],
        ["Imagem Docker", "eclipse-temurin:21-jdk-alpine"]], [5 * cm, 11.6 * cm], fs=8.0))
    s.append(P("Links do projeto", h2))
    s.append(tabela([
        ["GitHub", URL_GITHUB],
        ["Deploy (Render)", URL_DEPLOY]], [3.6 * cm, 13 * cm], cab=False, fs=8.0))
    s.append(P("Passo a passo - execucao local", h2))
    s += b9([
        "Clone o repositorio (%s) e abra a pasta do projeto no IntelliJ." % C("git clone " + URL_GITHUB),
        "No IntelliJ, va em <b>Run &gt; Edit Configurations &gt; Environment variables</b> e configure: "
        "%s (ex.: %s), %s (seu RM) e %s (sua senha do Oracle)."
        % (C("DB_URL"), C("jdbc:oracle:thin:@oracle.fiap.com.br:1521:ORCL"), C("DB_USER"), C("DB_PASSWORD")),
        "Execute a classe %s (ou rode %s no terminal). A tabela %s e criada automaticamente."
        % (C("CitizentechApplication"), C("./mvnw spring-boot:run"), C("DDDJ_CABAZES")),
        "Importe %s no Insomnia e teste em %s na ordem: cadastro, consulta, atualizar, reservar, retirar por QR e "
        "excluir." % (C("insomnia/citizentech-insomnia.json"), C("http://localhost:8080")),
        "Para rodar os testes automatizados (usam H2 em memoria, sem tocar no Oracle): %s." % C("./mvnw test")])
    s.append(P("Passo a passo - deploy no Render", h2))
    s += b9([
        "Suba o codigo para o GitHub (lembre: commits apos o prazo zeram a nota da parte tecnica).",
        "No <b>render.com</b>, clique em <b>New &gt; Web Service</b> e conecte o repositorio do GitHub.",
        "Deixe <b>Root Directory</b> em branco (o %s esta na raiz do repositorio)." % C("Dockerfile"),
        "Selecione o runtime <b>Docker</b> (o Render compila e executa o %s automaticamente)." % C("Dockerfile"),
        "Em <b>Environment Variables</b>, adicione %s, %s e %s. A variavel %s e fornecida pelo proprio Render."
        % (C("DB_URL"), C("DB_USER"), C("DB_PASSWORD"), C("PORT")),
        "Clique em <b>Create Web Service</b>, aguarde o deploy finalizar e teste %s."
        % C("GET https://seu-servico.onrender.com/cabazes")])
    return s


def main():
    doc = Doc(SAIDA)
    doc.multiBuild(construir())
    print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    main()
