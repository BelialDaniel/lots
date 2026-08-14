from collections import defaultdict

from itertools import groupby
 
 
# Block 1

print("Block 1:", end=" ")
 
payload = {

    "external_id": "res_001",

    "balance_cents": 0,

    "email": None

}
 
balance = payload.get("balance_cents") or 9999

email = payload.get("email") or "missing@example.com"
 
print(f"balance={balance}, email={email}")
 
 
# Block 2

print("Block 2:", end=" ")
 
def add_error(error, errors=[]):

    errors.append(error)

    return errors
 
a = add_error("missing email")

b = add_error("invalid balance")
 
print(f"a={a}, b={b}, same={a is b}")
 
 
# Block 3

print("Block 3:", end=" ")
 
numbers = [1, 2, 3, 4, 5]

filtered = (n for n in numbers if n > 2)
 
count = sum(1 for _ in filtered)

values = list(filtered)
 
print(f"count={count}, values={values}")
 
 
# Block 4

print("Block 4:", end=" ")
 
validators = []
 
for field in ["external_id", "property_id", "email"]:

    validators.append(lambda record: bool(record.get(field)))
 
record = {
    "external_id": "res_001",
    "property_id": "",
    "email": "ana@example.com"
}
results = [validator(record) for validator in validators] 
print(f"results={results}")

# Block 5
print("Block 5:", end=" ")
 
status_by_id = defaultdict(lambda: "pending")

status_by_id["res_001"] = "processed"
missing = status_by_id["res_999"]
print(f"status_by_id={dict(status_by_id)}, missing={missing}")

# Block 6
print("Block 6:", end=" ")
events = [
    {"property_id": "p1", "amount": 100},
    {"property_id": "p2", "amount": 200},
    {"property_id": "p1", "amount": 300},
    {"property_id": "p2", "amount": 400},
]

totals = {
    property_id: sum(event["amount"] for event in grouped)
    for property_id, grouped in groupby(events, key=lambda e: e["property_id"])
}
print(f"totals={totals}")
 
# Block 7
print("Block 7:", end=" ")
 
records = [
    {"external_id": "res_001", "balance_cents": "1000"},
    {"external_id": "res_002", "balance_cents": None},
    {"external_id": "res_003"},
]
 
valid = []

invalid = []
 
for record in records:
    try:
        balance = int(record["balance_cents"])
        valid.append(record["external_id"])
    except Exception:
        invalid.append(record["external_id"])
 
print(f"valid={valid}, invalid={invalid}")
 
Qué evalúa cada bloque
Block 1: uso peligroso de or para defaults. 0 es válido, pero se reemplaza por 9999.
Block 2: argumento mutable por defecto. La lista errors se comparte entre llamadas.
Block 3: los generators se consumen una sola vez.
Block 4: late binding en lambdas. Todos los validators usan el último valor de field, que es "email".
Block 5: defaultdict crea una key al acceder a una inexistente.
Block 6: groupby solo agrupa elementos consecutivos. Como la lista no está ordenada, el resultado final sobreescribe grupos anteriores.
Block 7: except Exception oculta causas distintas: TypeError para None y KeyError para campo faltante.
 