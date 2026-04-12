"""
caso_nuevo_bono.py — El Robo del Parcial en WUAIRA
 
La noche del martes, alguien entró a la sala WUAIRA de la facultad y copió el archivo
con las preguntas del parcial de Estructuras de Datos antes de que el profesor lo publicara.
Al día siguiente, cuatro estudiantes sacaron notas sospechosamente perfectas sin haber
asistido a las monitorías: Valentina (la mejor amiga del monitor), Sebastián (repitiendo el curso
y necesitaba pasar sí o sí), Daniela (presidenta del consejo estudiantil, con llave del
salón) y Camilo (compañero de Valentina que vive cerca de la universidad).
El profesor revisó los logs del sistema y encontró que alguien accedió al archivo desde el
computador número 7 de WUAIRA esa noche. Las huellas en el teclado del computador 7 coinciden
con las de Sebastián. Daniela tiene coartada verificada porque estaba en una reunión del consejo
grabada en video hasta las 11 PM, hora en que ocurrió el acceso. Valentina acusa a Camilo.
Camilo acusa a Sebastián. El monitor del curso declara que Sebastián le pidió el código de
acceso a WUAIRA esa tarde.
 
Revisando los hechos, llegué a las siguientes conclusiones:
Quien tiene coartada verificada por medios objetivos queda descartado como sospechoso.
Quien necesitaba urgentemente aprobar el curso tenía motivo suficiente para robar el parcial.
Quien tiene huellas en el objeto del crimen tiene evidencia física en su contra.
Quien tiene motivo y evidencia física en su contra es culpable.
Cuando el culpable señala a otra persona, esa acusación es un intento de desviar la investigación.
Quien le dio acceso al culpable al lugar del crimen es cómplice.
Quien declara algo que confirma la culpabilidad de otro es testigo clave.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import KnowledgeBase, Predicate, Rule, Term, ExistsGoal
 
 
def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()
 
    # Constantes del caso
    valentina  = Term("valentina")
    sebastian  = Term("sebastian")
    daniela    = Term("daniela")
    camilo     = Term("camilo")
    monitor    = Term("monitor")
    computador_7 = Term("computador_7")
 
    # === HECHOS ===
 
    # "Daniela tiene coartada verificada porque estaba en una reunión grabada en video"
    kb.add_fact(Predicate("coartada_verificada", (daniela,)))
 
    # "Sebastián está repitiendo el curso y necesitaba pasar sí o sí"
    kb.add_fact(Predicate("necesitaba_aprobar", (sebastian,)))
 
    # "Las huellas en el teclado del computador 7 coinciden con las de Sebastián"
    kb.add_fact(Predicate("huellas_en_objeto", (sebastian, computador_7)))
 
    # "El computador 7 es desde donde se copió el parcial"
    kb.add_fact(Predicate("es_objeto_crimen", (computador_7,)))
 
    # "Valentina acusa a Camilo"
    kb.add_fact(Predicate("acusa", (valentina, camilo)))
 
    # "Camilo acusa a Sebastián"
    kb.add_fact(Predicate("acusa", (camilo, sebastian)))
 
    # "El monitor dice que Sebastián le pidió el código de acceso a WUAIRA esa tarde"
    kb.add_fact(Predicate("dio_acceso", (monitor, sebastian)))
 
    # "El monitor del curso le dio el código de acceso a Sebastián"
    kb.add_fact(Predicate("declara_sobre", (monitor, sebastian)))
 
    # === REGLAS ===
    x = Term("$X")
    y = Term("$Y")
    obj = Term("$O")
 
    # "Alguien que tiene coartada verificada queda descartado"
    kb.add_rule(Rule(
        head=Predicate("descartado", (x,)),
        body=[Predicate("coartada_verificada", (x,))]
    ))
 
    # "Alguien que necesitaba aprobar tenía motivo para robar el parcial"
    kb.add_rule(Rule(
        head=Predicate("tiene_motivo", (x,)),
        body=[Predicate("necesitaba_aprobar", (x,))]
    ))
 
    # "Alguien que  tiene huellas en el objeto del crimen tiene evidencia física en su contra"
    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (x,)),
        body=[
            Predicate("huellas_en_objeto", (x, obj)),
            Predicate("es_objeto_crimen", (obj,)),
        ]
    ))
 
    # "Alguien que tiene motivo y evidencia física en su contra es culpable"
    kb.add_rule(Rule(
        head=Predicate("culpable", (x,)),
        body=[
            Predicate("tiene_motivo", (x,)),
            Predicate("evidencia_fisica", (x,)),
        ]
    ))
 
    # "Cuando el culpable señala a otra persona, es un intento de desviar la investigación"
    kb.add_rule(Rule(
        head=Predicate("distracción", (x, y)),
        body=[
            Predicate("culpable", (x,)),
            Predicate("acusa", (x, y)),
        ]
    ))
 
    # "Alguien que le dio acceso al culpable al lugar del crimen es cómplice"
    kb.add_rule(Rule(
        head=Predicate("complice", (x,)),
        body=[
            Predicate("dio_acceso", (x, y)),
            Predicate("culpable", (y,)),
        ]
    ))
 
    # "Alguien que declara algo que confirma la culpabilidad de otro es testigo clave"
    kb.add_rule(Rule(
        head=Predicate("testigo_clave", (x,)),
        body=[
            Predicate("declara_sobre", (x, y)),
            Predicate("culpable", (y,)),
        ]
    ))
 
 
    return kb
 
 
CASE = CrimeCase(
    id="robo_parcial_sala_computo",
    title="El Robo del Parcial en WUAIRA",
    suspects=("valentina", "sebastian", "daniela", "camilo"),
    narrative=__doc__,
    description=(
        "Alguien robó el archivo del parcial de Estructuras de Datos desde WUAIRA. "
        "Sebastián, repitente del curso, tiene las huellas en el computador 7 y le pidió el código "
        "de acceso a WUAIRA al monitor esa misma tarde. Daniela tiene coartada verificada en video."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Daniela está descartada como sospechosa?",
            goal=Predicate("descartado", (Term("daniela"),)),
        ),
        QuerySpec(
            description="¿Sebastián tenía motivo para robar el parcial?",
            goal=Predicate("tiene_motivo", (Term("sebastian"),)),
        ),
        QuerySpec(
            description="¿Hay evidencia física contra Sebastián?",
            goal=Predicate("evidencia_fisica", (Term("sebastian"),)),
        ),
        QuerySpec(
            description="¿Sebastián es culpable?",
            goal=Predicate("culpable", (Term("sebastian"),)),
        ),
        QuerySpec(
            description="¿La acusación de Camilo contra Sebastián es una distracción?",
            goal=Predicate("distracción", (Term("camilo"), Term("sebastian"))),
        ),
        QuerySpec(
            description="¿El monitor del curso es cómplice?",
            goal=Predicate("complice", (Term("monitor"),)),
        ),
        QuerySpec(
            description="¿El monitor del curso es testigo clave?",
            goal=Predicate("testigo_clave", (Term("monitor"),)),
        ),
        QuerySpec(
            description="¿Existe alguien que sea cómplice en el caso?",
            goal=ExistsGoal("$X", Predicate("complice", (Term("$X"),))),
        ),
    ),
)
