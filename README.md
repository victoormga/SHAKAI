# SHAKAI - Red Social Simple

SHAKAI es una red social desarrollada con **Django REST Framework** en el backend y **React + Tailwind** en el frontend. Permite a los usuarios registrarse, iniciar sesión, compartir publicaciones, comentar, dar me gusta, seguir a otros usuarios y más.

---

## 🚀 Tecnologías principales

- Backend: Django + Django REST Framework + JWT (SimpleJWT)
- Frontend: React + Vite + Tailwind CSS
- Base de datos: MySQL
- Autenticación: JWT + Usuarios personalizados
- Otras librerías: Lucide React, React Router, Context API

---

## ⚙️ Requisitos

- Python 3.10+
- Node.js 18+
- MySQL
- [pip](https://pip.pypa.io/en/stable/installation/) y [npm](https://www.npmjs.com/get-npm)

---

##  Instalación y ejecución con docker-compose

###  1. Clona el repositorio

```bash
git clone https://github.com/victoormga/SHAKAI.git
cd SHAKAI
```

###  2. Construye y levanta los contenedores:

```bash
docker-compose up --build -d
```
###  3. Aplica migraciones y crea el superusuario (solo una vez):

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

###  4. Accede a la app, teniendo estos dos puertos abiertos necesariamente (entrando por el del Frontend):

```bash
Backend (API): http://localhost:8000

Frontend: http://localhost:5173
```
### Para eliminar los contenedores:

```bash
docker-compose down
```

---

## ✅ Funcionalidades actuales

- Registro e inicio de sesión con JWT
- Feed público de publicaciones
- Likes y comentarios
- Perfiles de usuario con biografía
- Edición de perfil
- Seguir y dejar de seguir usuarios
- Modales para ver publicaciones
- Gestión de privacidad en perfiles
- Subida de imágenes y videos
- Notificaciones (seguir, comentar, dar like)
- Búsqueda de usuarios

---

## 📁 Estructura del proyecto

```
SHAKAI/
├── backend/     # Proyecto Django (DRF + MySql + Django  
├── frontend/    # PRpyecto React + Vite y React Dockerfile
├── venv/
├── docker-compose.yml
└── README.md
```

---

## 👤 Autor

victoormga - [GitHub](https://github.com/victoormga)
