import json
import sys
from pathlib import Path

from type_checker import SymbolTable
from evaluator import evaluate, _TYPE_MAP


def _load_expressions(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _build_symbol_table(vars_def: list[dict] | None) -> SymbolTable:
    st = SymbolTable()
    for v in (vars_def or []):
        t = _TYPE_MAP[v["type"].lower()]
        st.declare(v["name"], t, v["value"])
    return st


def _format_result(res) -> str:
    if res.error:
        return f"ERRO: {res.error}"
    note_str = f"  [{', '.join(res.notes)}]" if res.notes else ""
    return f"{res.value!r} ({res.type.name}){note_str}"


def main():
    path = Path(__file__).parent / "expressions.json"
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

    expressions = _load_expressions(path)

    print("=" * 60)
    print(" Motor de Verificação de Tipos")
    print("=" * 60)

    for i, item in enumerate(expressions, 1):
        desc = item.get("description", f"Expr {i}")
        sym_table = _build_symbol_table(item.get("vars"))
        result = evaluate(item["expr"], sym_table)
        print(f"\nExpr {i}: {desc}")
        print(f"  => {_format_result(result)}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
