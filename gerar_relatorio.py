from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

OUTPUT = "Relatorio_Tecnico.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=3*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

styles = getSampleStyleSheet()

titulo = ParagraphStyle("titulo", parent=styles["Title"],
    fontSize=16, spaceAfter=6, alignment=TA_CENTER)
subtitulo = ParagraphStyle("subtitulo", parent=styles["Normal"],
    fontSize=11, spaceAfter=16, alignment=TA_CENTER, textColor=colors.grey)
h1 = ParagraphStyle("h1", parent=styles["Heading1"],
    fontSize=13, spaceBefore=18, spaceAfter=6,
    textColor=colors.HexColor("#1a1a1a"), borderPad=2)
h2 = ParagraphStyle("h2", parent=styles["Heading2"],
    fontSize=11, spaceBefore=12, spaceAfter=4)
body = ParagraphStyle("body", parent=styles["Normal"],
    fontSize=10, leading=15, spaceAfter=8, alignment=TA_JUSTIFY)
code = ParagraphStyle("code", parent=styles["Code"],
    fontSize=8.5, leading=13, leftIndent=12,
    backColor=colors.HexColor("#f5f5f5"), borderColor=colors.HexColor("#cccccc"),
    borderWidth=0.5, borderPad=6, spaceAfter=8)
caption = ParagraphStyle("caption", parent=styles["Normal"],
    fontSize=9, textColor=colors.grey, spaceAfter=10, alignment=TA_CENTER)

story = []

# ── Capa ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Motor de Verificação de Tipos", titulo))
story.append(Paragraph("Relatório Técnico — Projeto de Compiladores", subtitulo))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Disciplina: Construção de Compiladores", body))
story.append(Paragraph("Linguagem utilizada: Python 3.8+", body))
story.append(Spacer(1, 1.5*cm))

# ── 1. Introdução ─────────────────────────────────────────────────────────────
story.append(Paragraph("Introdução", h1))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "A verificação de tipos é uma das etapas mais críticas no processo de análise semântica "
    "de um compilador. Ela garante que as operações realizadas sobre dados sejam compatíveis "
    "com os tipos declarados ou inferidos pelo sistema, prevenindo erros em tempo de execução "
    "e produzindo mensagens de diagnóstico claras ao programador.", body))
story.append(Paragraph(
    "Este projeto implementa um <b>Motor de Verificação de Tipos</b> em Python que avalia "
    "expressões matemáticas representadas no formato JSON. O motor simula dois mecanismos "
    "fundamentais presentes em linguagens de programação modernas: a <b>coerção implícita</b> "
    "(conversão automática entre tipos compatíveis, como <i>int</i> para <i>float</i>) e o "
    "<b>cast explícito</b> (conversão forçada declarada pelo programador).", body))
story.append(Paragraph(
    "O sistema também mantém uma <b>tabela de símbolos</b>, estrutura essencial em "
    "compiladores para armazenar informações sobre variáveis declaradas no escopo atual, "
    "incluindo nome, tipo e valor.", body))
story.append(Paragraph(
    "O objetivo central do trabalho é aplicar, de forma prática, os conceitos de "
    "análise semântica, equivalência de tipos e propagação de erros estudados em sala, "
    "demonstrando como um compilador real tomaria decisões de tipo durante a fase de "
    "análise de um programa-fonte.", body))

# ── 2. Metodologia ────────────────────────────────────────────────────────────
story.append(Paragraph("Metodologia de Implementação", h1))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.1  Estrutura do Projeto", h2))
story.append(Paragraph(
    "O projeto foi dividido em três módulos Python com responsabilidades bem definidas:", body))

tabela_arqs = [
    ["Arquivo", "Responsabilidade"],
    ["type_checker.py", "Define o enum Type, a classe SymbolTable (hash map), as\nregras de coerção implícita e as regras de cast explícito."],
    ["evaluator.py",    "Percorre recursivamente os nós JSON da expressão e retorna\no valor avaliado, o tipo inferido e notas de coerção."],
    ["main.py",         "Entry point: lê expressions.json, invoca o avaliador\ne imprime o relatório formatado no terminal."],
    ["expressions.json","Arquivo de casos de teste com 8 expressões cobrindo\ntodos os cenários relevantes."],
]
t = Table(tabela_arqs, colWidths=[4.5*cm, 10.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#2c3e50")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f2f2f2")]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("2.2  Representação de Tipos (type_checker.py)", h2))
story.append(Paragraph(
    "Os tipos suportados pelo motor são definidos como um <b>Enum</b>: "
    "<i>INT, FLOAT, BOOL, STRING</i> e <i>ERROR</i> (estado sentinela para propagação de falhas). "
    "As regras de coerção implícita são armazenadas em um dicionário Python — equivalente a um "
    "hash map — cujas chaves são tuplas <i>(tipo_origem, tipo_destino)</i> e cujos valores "
    "correspondem ao tipo resultante da operação:", body))
story.append(Preformatted(
    "COERCION_RULES = {\n"
    "    (Type.INT,   Type.FLOAT):  Type.FLOAT,   # int op float  -> float\n"
    "    (Type.FLOAT, Type.INT):    Type.FLOAT,   # float op int  -> float\n"
    "    (Type.INT,   Type.BOOL):   Type.INT,     # int op bool   -> int\n"
    "    (Type.BOOL,  Type.FLOAT):  Type.FLOAT,   # bool op float -> float\n"
    "    ...\n"
    "}", code))
story.append(Paragraph(
    "As regras de cast explícito são armazenadas em outro dicionário com valor booleano, "
    "indicando se a conversão é permitida. Por exemplo, <i>STRING → INT</i> é marcada como "
    "<i>False</i>, representando um cast inválido que o motor deve rejeitar com mensagem de erro.", body))

story.append(Paragraph("2.3  Tabela de Símbolos (SymbolTable)", h2))
story.append(Paragraph(
    "A classe <b>SymbolTable</b> encapsula um dicionário Python "
    "(<i>dict[str, Symbol]</i>) que mapeia nomes de variáveis a objetos <b>Symbol</b>, "
    "os quais carregam <i>nome</i>, <i>tipo</i> e <i>valor</i>. "
    "Os métodos <i>declare()</i> e <i>lookup()</i> simulam as operações de inserção e "
    "consulta típicas da tabela de símbolos de um compilador real.", body))

story.append(Paragraph("2.4  Avaliador de Expressões (evaluator.py)", h2))
story.append(Paragraph(
    "A função central <b>evaluate(node, sym_table)</b> implementa uma travessia recursiva "
    "da árvore de expressão representada em JSON. Cada chamada retorna um objeto "
    "<b>EvalResult</b> contendo o valor calculado, o tipo inferido, notas de coerção aplicadas "
    "e uma mensagem de erro caso a operação seja inválida.", body))
story.append(Paragraph("Os tipos de nó reconhecidos pelo avaliador são:", body))

tabela_nos = [
    ["Tipo de nó",       "Formato JSON",                                          "Comportamento"],
    ["Literal",          '{"type": "int", "value": 3}',                          "Retorna valor e tipo diretamente."],
    ["Variável",         '{"var": "x"}',                                         "Consulta a SymbolTable; erro se não declarada."],
    ["Operação binária", '{"op": "+", "left": {...}, "right": {...}}',           "Avalia filhos; aplica coerção se necessário."],
    ["Cast explícito",   '{"op": "cast", "to": "float", "expr": {...}}',        "Verifica regra de cast; converte ou retorna erro."],
]
t2 = Table(tabela_nos, colWidths=[3*cm, 6*cm, 6*cm])
t2.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#2c3e50")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f2f2f2")]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
]))
story.append(t2)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph(
    "A propagação de erros é feita por curto-circuito: ao detectar um <i>EvalResult.error</i> "
    "em qualquer subexpressão, o avaliador retorna imediatamente o erro sem continuar a "
    "avaliação, evitando exceções não tratadas e garantindo saídas previsíveis.", body))

# ── 3. Casos de Teste ─────────────────────────────────────────────────────────
story.append(Paragraph("Casos de Teste", h1))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Os casos de teste foram definidos em <i>expressions.json</i> e executados com o comando "
    "<b>python main.py</b>. A seguir são apresentadas as entradas (nós JSON) e as saídas "
    "produzidas pelo motor.", body))

casos = [
    (
        "Caso 1 — INT + INT (mesmo tipo)",
        '{"op": "+", "left": {"type": "int", "value": 10},\n'
        '            "right": {"type": "int", "value": 5}}',
        "=> 15 (INT)",
        "Operação entre tipos idênticos. Nenhuma coerção necessária."
    ),
    (
        "Caso 2 — INT + FLOAT (coerção implícita)",
        '{"op": "+", "left": {"type": "int",   "value": 3},\n'
        '            "right": {"type": "float", "value": 2.5}}',
        "=> 5.5 (FLOAT)  [coercao implicita: INT e FLOAT -> FLOAT]",
        "INT é promovido a FLOAT automaticamente. A nota de coerção é registrada."
    ),
    (
        "Caso 3 — Cast explícito FLOAT -> INT",
        '{"op": "cast", "to": "int",\n'
        ' "expr": {"type": "float", "value": 9.7}}',
        "=> 9 (INT)  [cast FLOAT -> INT]",
        "Conversão válida; valor é truncado para 9 (comportamento de int())."
    ),
    (
        "Caso 4 — Cast inválido STRING -> INT",
        '{"op": "cast", "to": "int",\n'
        ' "expr": {"type": "string", "value": "hello"}}',
        "=> ERRO: Cast invalido: STRING -> INT",
        "STRING -> INT é explicitamente proibido nas regras. Motor retorna erro sem excecao."
    ),
    (
        "Caso 5 — Variável da SymbolTable (x * 2)",
        'vars: [{"name": "x", "type": "int", "value": 7}]\n'
        '{"op": "*", "left": {"var": "x"},\n'
        '            "right": {"type": "int", "value": 2}}',
        "=> 14 (INT)",
        "Variavel x e consultada na SymbolTable; operacao realizada com tipo INT."
    ),
    (
        "Caso 6 — Divisão por zero",
        '{"op": "/", "left": {"type": "int", "value": 8},\n'
        '            "right": {"type": "int", "value": 0}}',
        "=> ERRO: Divisao por zero",
        "Detectado antes da divisao; motor retorna EvalResult.error sem lancar excecao."
    ),
    (
        "Caso 7 — Concatenação STRING + STRING",
        '{"op": "+", "left": {"type": "string", "value": "Hello, "},\n'
        '            "right": {"type": "string", "value": "World!"}}',
        "=> 'Hello, World!' (STRING)",
        "Operador + e o unico permitido para STRING; resultado e a concatenacao."
    ),
    (
        "Caso 8 — BOOL * FLOAT (coerção implícita)",
        '{"op": "*", "left": {"type": "bool",  "value": true},\n'
        '            "right": {"type": "float", "value": 3.14}}',
        "=> 3.14 (FLOAT)  [coercao implicita: BOOL e FLOAT -> FLOAT]",
        "BOOL e promovido a FLOAT (True=1.0). Resultado: 1.0 * 3.14 = 3.14."
    ),
]

for titulo_caso, entrada, saida, explicacao in casos:
    story.append(Paragraph(titulo_caso, h2))
    story.append(Paragraph("<b>Entrada (JSON):</b>", body))
    story.append(Preformatted(entrada, code))
    story.append(Paragraph("<b>Saída:</b>", body))
    story.append(Preformatted(saida, code))
    story.append(Paragraph(f"<i>{explicacao}</i>", caption))

story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Todos os 8 casos foram executados com sucesso: os 5 casos válidos produziram valores e "
    "tipos corretos, e os 3 casos de erro retornaram mensagens descritivas sem lançar exceções "
    "não tratadas, demonstrando robustez do motor.", body))

doc.build(story)
print(f"PDF gerado: {OUTPUT}")
