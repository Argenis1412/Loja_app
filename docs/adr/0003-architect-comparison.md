# ADR 0003: Architect Model Comparison

## Contexto
Durante la fase de desarrollo del agente `Architect`, se evaluaron dos modelos: Gemini Flash (usado por el Scout) y Claude Sonnet (`claude-sonnet-4-6`). El objetivo del Architect es recibir los hallazgos del `Scout` (en formato JSON), validarlos, detectar falsos positivos, priorizarlos y generar un plan de implementación robusto.

Se ejecutó un script `compare_architects.py` que envió la misma entrada (output del Scout) a ambos modelos para analizar sus respuestas.

### Resultados de la Comparativa

| Métrica | Gemini Flash | Claude Sonnet (`claude-sonnet-4-6`) |
| :--- | :--- | :--- |
| **Tiempo de ejecución** | 25.96s | 43.26s |
| **Tokens (In / Out)** | 720 / 1165 | 762 / 2222 |
| **Costo** | $0.00040 | $0.03562 |
| **Tareas identificadas**| 5 | 6 |
| **Falsos positivos** | 0 | 2 |

#### Hallazgos Clave
1. **Profundidad de Análisis**: Gemini Flash proporcionó resúmenes de alto nivel sobre los hallazgos del Scout, pero Claude Sonnet detalló el porqué de los riesgos (ej. falta de validación cruzada, contratos frontend-backend implícitos, mutación de modelos de dominio por la capa de servicio).
2. **Detección de Falsos Positivos**: Claude Sonnet identificó correctamente 2 falsos positivos del Scout:
   - Notó que `recibo_models.py` es un artefacto downstream de la preocupación de idempotencia en `pagamentos_api.py`, no un hotspot independiente.
   - Rebajó la severidad de `settings.py`, señalando que es un rol arquitectónico (riesgo latente) y no un defecto activo a menos que cause un fallo conocido.
3. **Análisis de Dependencias y Archivos**: Claude fue capaz de identificar archivos afectados adicionales que no fueron listados por Gemini (ej. `postgres_recibo_repository.py`).
4. **Blockers y Riesgos Sistémicos**: Los blockers propuestos por Claude fueron accionables y secuenciales (ej. "T-03 debe estar completo antes de T-05", "ausencia de tests bloquea modificaciones de alto riesgo"), mientras que Gemini dio blockers más genéricos.

## Decisión
Se ha decidido utilizar **Claude Sonnet** como el modelo principal y exclusivo para el rol de `Architect`. 

Aunque el costo de Claude Sonnet es significativamente mayor (~88x más caro que Gemini Flash), su capacidad de razonamiento justifica completamente la inversión en esta etapa crítica del pipeline. 

## Consecuencias
- **Eficacia**: Se asegura una fase de planificación mucho más robusta. Claude evita que el Executor trabaje sobre falsos positivos, reduciendo el retrabajo.
- **Costo**: Se incrementa el presupuesto gastado por corrida en esta etapa (a ~$0.035), pero se mantiene un enfoque económicamente viable al usar Gemini Flash para el `Scout` (exploración masiva) y DeepSeek para el `Executor` en tareas mecánicas.
- **Mantenimiento**: El rol de diseño arquitectónico, la priorización de tareas secuenciales y la validación lógica compleja quedan estrictamente reservados para Claude.
