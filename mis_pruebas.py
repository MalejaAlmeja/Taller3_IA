from src.logic_core import Atom
from src.logic_core import Implies
from src.model_checking import get_all_models
from src.model_checking import check_entailment

# Prueba implementación get all_models
models = get_all_models({'p', 'q'})
print(f"Número de modelos: {len(models)}")
for m in models:
    print(f"  {m}")

# Modus ponens: {p → q, p} |= q
kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
print(f"Modus ponens: {check_entailment(kb, Atom('q'))}")

# No se puede derivar q solo de p → q
kb = [Implies(Atom('p'), Atom('q'))]
print(f"Solo implicación: {check_entailment(kb, Atom('q'))}")