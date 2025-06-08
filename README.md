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

## 🧪 Instalación y ejecución local

### 🔁 1. Clona el repositorio

```bash
git clone https://github.com/victoormga/SHAKAI.git
cd SHAKAI
```

### 🐍 2. Configura el entorno backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crea el archivo `.env`:

```bash
cp .env.example .env
```

Asegúrate de que `.env` contenga tus credenciales de PostgreSQL, secret key, etc.

Luego, prepara la base de datos:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Finalmente, ejecuta el servidor backend:

```bash
python manage.py runserver
```

El backend estará disponible en [http://localhost:8000](http://localhost:8000)

---

### ⚛️ 3. Configura el entorno frontend (React)

```bash
cd ../frontend
npm install
npm run dev
```

El frontend estará disponible en [http://localhost:5173](http://localhost:5173)

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

---

## 🛠️ En desarrollo

- Notificaciones (seguir, comentar, dar like)
- Recuperación de contraseña por email
- Búsqueda de usuarios
- Mejoras UI/UX

---

## 📁 Estructura del proyecto

```
SHAKAI/
├── backend/     # Proyecto Django (DRF + PostgreSQL)
├── frontend/    # Proyecto React + Tailwind + Vite
└── README.md
```

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT.

---

## 👤 Autor

VictooR MGA - [GitHub](https://github.com/victoormga)
