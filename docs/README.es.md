<div align="center">

# Antifragile Decision Loop

### Revisión semanal antifrágil: decisión asistida por el contexto macro

**Recopilar. Verificar. Debatir. Arbitrar. Revisar. Evolucionar.**

Un bucle semanal de investigación evidencia-primero, adaptable a cualquier mercado, con un consejo de expertos y auto-mejora acotada. Los factores macro verificados ajustan el presupuesto de riesgo — nunca fabrican una operación.

[English](../README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-00d992.svg)](../LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-00d992.svg?logo=python&logoColor=101010)](https://www.python.org/)
[![Mercado: adaptadores](https://img.shields.io/badge/Mercado-adaptadores_intercambiables-00d992.svg)](#l%C3%ADmites)
[![Modo: solo investigaci%C3%B3n](https://img.shields.io/badge/Modo-solo_investigaci%C3%B3n-1a1a1a.svg)](#l%C3%ADmites)

</div>

> [!IMPORTANT]
> Solo para investigación cuantitativa y apoyo a decisiones. No conecta con brókers ni envía órdenes. No constituye asesoramiento de inversión.

## Idea central

El proyecto convierte una revisión semanal en un proceso auditable:

1. Mide la semana desde la primera apertura real hasta el último cierre real.
2. Verifica precio, volumen, fecha y acuerdo entre fuentes antes de interpretar.
3. Tras los controles de riesgo, da prioridad a la evidencia histórica BOLL (bandas de Bollinger); después revisa precio-volumen, flujos de 5/10/20 días, comunicados y, por último, el contexto macro ajusta el presupuesto de riesgo.
4. Una narrativa sin fuente verificable y fechada no es una razón de trading.
5. Una revisión solo puede usar información pública antes de `evidence_cutoff`; un anuncio posterior es un evento nuevo, no una predicción fallida del informe anterior.

## Consejo de expertos

Ocho roles, un responsable por etapa, todo pasa por el relé central:

```mermaid
flowchart TD
    L["Líder de evolución · relé central"] --> S1
    subgraph WEEKLY["Pipeline semanal"]
        S1["① Recopilar — observaciones fechadas: mercado, informes, noticias, macro, materias primas"] --> S2["② Verificar — acuerdo de fuentes, marcas de tiempo, datos faltantes y conflictos"]
        S2 --> S3["③ Sintetizar — comparar perspectivas, explicitar supuestos"]
        S3 --> S4["④ Arbitrar — filtros duros de supervivencia + jerarquía de señales"]
        S4 --> S5["⑤ Decidir — comprobaciones condicionales y controles de riesgo"]
        S5 --> S6["⑥ Publicar — informe Markdown/HTML auditable"]
    end
    S6 --> R["⑦ Revisar — decisiones vs resultados"] --> E["⑧ Evolucionar — promover solo reglas recurrentes"] --> L
```

| Etapa | Rol | Responsabilidad |
|---|---|---|
| Relé | **Líder de evolución** | Despacho central, puertas de etapa, promoción de reglas |
| ① | **Recopilador** | Extracción única de mercado / informes / noticias / macro / materias primas |
| ② | **Verificador** | Validación cruzada en ventanas de 168h + 120h → tabla de hechos |
| ③ | **Sintetizador de evidencia** | Puntuación de seis lentes fusionada vía MCDA (TOPSIS + VIKOR) |
| ④ | **Arbitrador de señales** | Motor de reglas + zona gris de filosofía antifrágil → 🟢🟡🔴 |
| ⑤ | **Decisor** | Traduce el semáforo en zonas de disparo, ajustes de posición y controles |
| ⑥ | **Editor de investigación** | Markdown → informe HTML autocontenido |
| ⑦ | **Experto en revisión** | Decisiones previas vs resultados → retrospectiva estructurada |
| ⑧ | **Líder de evolución** | Cierra el bucle: consolida, promueve reglas, evoluciona prompts |

Contrato público completo: [`docs/expert-team.md`](expert-team.md).

## Auto-mejora acotada

**W1 generar → W2 revisar → W2.5 puerta humana/de política → W3 evolucionar → W1**. Los cambios en reglas, umbrales, roles, prompts, fuentes o cadenas de respaldo requieren la puerta W2.5; los arreglos de presentación pueden promoverse automáticamente.

<img src="../assets/readme/evolution-loop.png" alt="Bucle de evolución con puerta humana y promoción reversible" width="100%" />

Reglas de promoción: [`evolution-loop.md`](evolution-loop.md).

## Inicio rápido

```bash
git clone https://github.com/marqosjiang-gif/antifragile-decision-loop.git
cd antifragile-decision-loop
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

cp watchlist.example.json watchlist.local.json
python3 quant_loop.py --watchlist watchlist.local.json
```

Configure solo sus propios símbolos en `watchlist.local.json`. El archivo está ignorado por Git: no incluya posiciones, costes, cuentas ni credenciales.

## Jerarquía de señales

El orden es la disciplina. Una historia macro no invalida evidencia BOLL válida; un resultado BOLL no invalida un conflicto de datos, un backtest con poca muestra o un filtro de riesgo de supervivencia.

| Capa | Pregunta | Regla |
|---|---|---|
| Integridad de datos | ¿Precio, volumen, fechas y fuentes son utilizables? | Un desacuerdo de precio sin resolver bloquea conclusiones direccionales. |
| BOLL histórico | ¿Esta configuración semanal/mensual funcionó con suficientes observaciones? | Es la entrada técnica de mayor peso, no una garantía. |
| Confirmación | ¿Precio-volumen y flujos de 5/10/20 días coinciden? | Un movimiento de un día no borra una señal de medio plazo. |
| Evidencia corporativa | ¿Hay un comunicado fechado que cambie la tesis? | Los eventos posteriores nunca rellenan el informe previo. |
| Contexto macro | ¿Un factor verificado cambia el presupuesto de riesgo? | El contexto puede restringir el riesgo, no fabricar una operación. |

## Límites

La salida es un andamiaje de investigación con estado `research_only`. Las decisiones reales requieren datos actuales verificados y las restricciones de riesgo del usuario. No publique listas personales, posiciones, informes generados, cachés, correos electrónicos, tokens o claves API.

El núcleo público es adaptable a mercados: calendarios, liquidación, límites de precio, ventas en corto y acciones corporativas pertenecen al adaptador del mercado; no se copian entre mercados de forma implícita. Los ejemplos usan símbolos sintéticos.

Reglas completas: [`PUBLIC_PROTOCOL.md`](../PUBLIC_PROTOCOL.md).

## Licencia

[MIT License](../LICENSE)
