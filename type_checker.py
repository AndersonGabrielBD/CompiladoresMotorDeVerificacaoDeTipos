from enum import Enum, auto


class Type(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    ERROR = auto()


# (source_type, target_type) -> result_type for implicit coercion
COERCION_RULES: dict[tuple["Type", "Type"], "Type"] = {
    (Type.INT,   Type.FLOAT):  Type.FLOAT,
    (Type.FLOAT, Type.INT):    Type.FLOAT,
    (Type.INT,   Type.BOOL):   Type.INT,
    (Type.BOOL,  Type.INT):    Type.INT,
    (Type.BOOL,  Type.FLOAT):  Type.FLOAT,
    (Type.FLOAT, Type.BOOL):   Type.FLOAT,
    (Type.INT,   Type.INT):    Type.INT,
    (Type.FLOAT, Type.FLOAT):  Type.FLOAT,
    (Type.BOOL,  Type.BOOL):   Type.BOOL,
    (Type.STRING, Type.STRING): Type.STRING,
}

# Explicit cast rules: (from_type, to_type) -> allowed
CAST_RULES: dict[tuple["Type", "Type"], bool] = {
    (Type.INT,    Type.FLOAT):  True,
    (Type.FLOAT,  Type.INT):    True,
    (Type.BOOL,   Type.INT):    True,
    (Type.INT,    Type.BOOL):   True,
    (Type.BOOL,   Type.FLOAT):  True,
    (Type.FLOAT,  Type.BOOL):   True,
    (Type.INT,    Type.STRING): True,
    (Type.FLOAT,  Type.STRING): True,
    (Type.BOOL,   Type.STRING): True,
    (Type.STRING, Type.INT):    False,  # inválido: string -> int sem parse
    (Type.STRING, Type.FLOAT):  False,
    (Type.STRING, Type.BOOL):   False,
}


def can_coerce(t1: Type, t2: Type) -> bool:
    return (t1, t2) in COERCION_RULES


def coerce(t1: Type, t2: Type) -> Type:
    return COERCION_RULES.get((t1, t2), Type.ERROR)


def can_cast(from_type: Type, to_type: Type) -> bool:
    return CAST_RULES.get((from_type, to_type), False)


def apply_cast(value, from_type: Type, to_type: Type):
    if not can_cast(from_type, to_type):
        raise TypeError(f"Cast inválido: {from_type.name} -> {to_type.name}")
    converters = {
        Type.INT:    int,
        Type.FLOAT:  float,
        Type.BOOL:   bool,
        Type.STRING: str,
    }
    return converters[to_type](value)


class Symbol:
    def __init__(self, name: str, type_: Type, value):
        self.name = name
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Symbol({self.name!r}, {self.type.name}, {self.value!r})"


class SymbolTable:
    def __init__(self):
        self._table: dict[str, Symbol] = {}

    def declare(self, name: str, type_: Type, value) -> Symbol:
        sym = Symbol(name, type_, value)
        self._table[name] = sym
        return sym

    def lookup(self, name: str) -> Symbol:
        if name not in self._table:
            raise KeyError(f"Variável '{name}' não declarada")
        return self._table[name]
