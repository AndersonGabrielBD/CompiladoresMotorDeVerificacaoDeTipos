# Motor de Verificação de Tipos

Simulador de verificação e coerção de tipos para expressões matemáticas representadas em JSON.

## Requisitos

- Python 3.8 ou superior
- Sem dependências externas

## Como executar

```bash
python main.py
```

Ou passando um arquivo de expressões customizado:

```bash
python main.py expressions.json
```

## Saída esperada

```
============================================================
 Motor de Verificação de Tipos
============================================================

Expr 1: INT + INT (mesmo tipo)
  => 15 (INT)

Expr 2: INT + FLOAT (coerção implícita)
  => 5.5 (FLOAT)  [coerção implícita: INT e FLOAT -> FLOAT]

Expr 3: Cast explícito FLOAT -> INT
  => 9 (INT)  [cast FLOAT -> INT]

Expr 4: Cast inválido STRING -> INT
  => ERRO: Cast inválido: STRING -> INT

Expr 5: Operação com variável da symbol table (x * 2)
  => 14 (INT)

Expr 6: Divisão por zero
  => ERRO: Divisão por zero
...
```

## Estrutura do projeto

| Arquivo             | Descrição                                              |
|---------------------|--------------------------------------------------------|
| `type_checker.py`   | Enum de tipos, SymbolTable, regras de coerção e cast   |
| `evaluator.py`      | Avaliação recursiva de nós de expressão JSON           |
| `main.py`           | Entry point: lê JSON, avalia e imprime relatório       |
| `expressions.json`  | Casos de teste                                         |

## Formato das expressões JSON

Cada item do array pode conter:

- `"description"`: descrição textual do teste
- `"vars"` *(opcional)*: lista de variáveis para a symbol table
- `"expr"`: nó raiz da expressão

### Tipos de nó

**Literal:**
```json
{"type": "int", "value": 42}
```

**Referência a variável:**
```json
{"var": "x"}
```

**Operação binária (`+`, `-`, `*`, `/`):**
```json
{"op": "+", "left": {...}, "right": {...}}
```

**Cast explícito:**
```json
{"op": "cast", "to": "float", "expr": {...}}
```
