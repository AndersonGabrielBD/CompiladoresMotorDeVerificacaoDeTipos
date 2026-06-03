from type_checker import Type, SymbolTable, can_coerce, coerce, can_cast, apply_cast

_TYPE_MAP = {
    "int":    Type.INT,
    "float":  Type.FLOAT,
    "bool":   Type.BOOL,
    "string": Type.STRING,
}


def _parse_type(name: str) -> Type:
    t = _TYPE_MAP.get(name.lower())
    if t is None:
        raise ValueError(f"Tipo desconhecido: {name!r}")
    return t


class EvalResult:
    def __init__(self, value, type_: Type, notes: list[str] | None = None, error: str | None = None):
        self.value = value
        self.type = type_
        self.notes: list[str] = notes or []
        self.error = error

    @classmethod
    def err(cls, msg: str) -> "EvalResult":
        return cls(None, Type.ERROR, error=msg)


def evaluate(node: dict, sym_table: SymbolTable) -> EvalResult:
    # Literal leaf node: {"type": "int", "value": 3}
    if "type" in node and "value" in node and "op" not in node:
        t = _parse_type(node["type"])
        return EvalResult(node["value"], t)

    # Variable reference: {"var": "x"}
    if "var" in node:
        try:
            sym = sym_table.lookup(node["var"])
            return EvalResult(sym.value, sym.type)
        except KeyError as e:
            return EvalResult.err(str(e))

    op = node.get("op")
    if op is None:
        return EvalResult.err(f"Nó inválido: {node}")

    # Cast node: {"op": "cast", "to": "int", "expr": {...}}
    if op == "cast":
        inner = evaluate(node["expr"], sym_table)
        if inner.error:
            return inner
        to_type = _parse_type(node["to"])
        if not can_cast(inner.type, to_type):
            return EvalResult.err(f"Cast inválido: {inner.type.name} -> {to_type.name}")
        try:
            new_val = apply_cast(inner.value, inner.type, to_type)
            notes = [f"cast {inner.type.name} -> {to_type.name}"]
            return EvalResult(new_val, to_type, notes)
        except (TypeError, ValueError) as e:
            return EvalResult.err(str(e))

    # Binary operations
    if op not in ("+", "-", "*", "/"):
        return EvalResult.err(f"Operador desconhecido: {op!r}")

    left = evaluate(node["left"], sym_table)
    right = evaluate(node["right"], sym_table)

    if left.error:
        return left
    if right.error:
        return right

    notes: list[str] = []

    if left.type == right.type:
        result_type = left.type
    elif can_coerce(left.type, right.type):
        result_type = coerce(left.type, right.type)
        notes.append(f"coerção implícita: {left.type.name} e {right.type.name} -> {result_type.name}")
    else:
        return EvalResult.err(
            f"Tipos incompatíveis para '{op}': {left.type.name} e {right.type.name}"
        )

    if result_type == Type.STRING:
        if op != "+":
            return EvalResult.err(f"Operador '{op}' não suportado para STRING")
        return EvalResult(str(left.value) + str(right.value), Type.STRING, notes)

    lv = float(left.value) if result_type == Type.FLOAT else int(left.value)
    rv = float(right.value) if result_type == Type.FLOAT else int(right.value)

    if op == "/" and rv == 0:
        return EvalResult.err("Divisão por zero")

    ops = {"+": lv + rv, "-": lv - rv, "*": lv * rv, "/": lv / rv}
    raw = ops[op]

    # Keep INT as int
    if result_type == Type.INT:
        raw = int(raw)

    return EvalResult(raw, result_type, notes)
