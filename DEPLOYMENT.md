# Guía de Despliegue — Loja App (Vercel + Supabase)

Este documento explica cómo desplegar el proyecto completo (Frontend y Backend) en **Vercel**, utilizando **Supabase** como base de datos de alto rendimiento.

## Paso 1: Base de Datos — Supabase

Vercel no mantiene archivos locales persistentes (como `test.db`), por lo que usaremos una base de datos PostgreSQL en la nube.

1.  Crea un proyecto en [Supabase](https://supabase.com/).
2.  Ve a **Settings** → **Database** → **Connection String**.
3.  Copia la pestaña **URI** (que empieza por `postgresql://`).
4.  Reemplaza `[YOUR-PASSWORD]` con la contraseña que elegiste al crear el proyecto.
5.  **Guarda esta URL**, la necesitarás en el Paso 2.

---

## Paso 2: Despliegue en Vercel

Vercel detectará automáticamente la configuración en la raíz del proyecto para desplegar tanto el Frontend (Vite) como el Backend (FastAPI).

1.  Ve a tu dashboard de [Vercel](https://vercel.com/) y haz clic en **"Add New"** → **"Project"**.
2.  Importa este repositorio desde GitHub.
3.  **Configuración del Proyecto**:
    *   Vercel detectará que es un proyecto de Vite. No cambies el `Root Directory`, déjalo en la raíz `/`.
4.  **Variables de Entorno (Environment Variables)**:
    Añade las siguientes variables antes de dar a "Deploy":

    | Key | Value |
    | :--- | :--- |
    | `DATABASE_URL` | La URL de Supabase obtenida en el Paso 1 |
    | `ENVIRONMENT` | `production` |

5.  Haz clic en **"Deploy"**.

---

## Estructura del Proyecto en Vercel

*   **Frontend**: Se compila automáticamente desde la carpeta `frontend/`.
*   **Backend**: Se ejecuta como funciones de Python desde la carpeta `api/index.py`, la cual conecta con la lógica en `backend/`.
*   **Rutas**:
    *   Las peticiones a `/api/*` se dirigen automáticamente al backend.
    *   El resto de peticiones sirven el frontend de React.

---

## Desarrollo Local con Base de Datos Cloud

Si quieres probar tu código localmente usando la base de datos de Supabase en lugar de SQLite:

1.  Crea un archivo `.env` en la carpeta `backend/` con tu `DATABASE_URL`.
2.  Ejecuta el backend como lo haces normalmente.

---

## Solución de Problemas

*   **Cold Starts**: En el plan gratuito de Vercel, la primera petición al backend después de un tiempo de inactividad puede tardar de 2 a 5 segundos en responder mientras la función "despierta".
*   **CORS**: El sistema está configurado para permitir peticiones desde cualquier origen, pero al estar el frontend y el backend bajo el mismo dominio de Vercel, no deberías tener problemas.
*   **Timeout**: Las funciones gratuitas de Vercel tienen un límite de ejecución de 10 segundos.
