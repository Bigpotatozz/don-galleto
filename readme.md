# Proyecto Django

Este proyecto utiliza Django como framework de desarrollo web. A continuación, se describen los pasos para configurar y ejecutar el proyecto correctamente.

## Requisitos previos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

- Python 3
- pip (administrador de paquetes de Python)
- virtualenv (opcional pero recomendado)
- MySql

## Configuración del entorno

### 1. Clonar el repositorio
```sh
 git clone <URL_DEL_REPOSITORIO>
 cd <NOMBRE_DEL_PROYECTO>
```

### 2. Crear y activar un entorno virtual
```sh
python -m venv env
source env/bin/activate  # En macOS/Linux
env\Scripts\activate  # En Windows
```

### 3. Instalar dependencias
```sh
pip install -r requirements.txt
```

## Configuración de la base de datos

### 4. Configurar el archivo `.env`
Crea un archivo `.env` en la raíz del proyecto con las variables necesarias, por ejemplo:
```env
DATABASE_NAME=nombre_de_la_base
DATABASE_USER=usuario
DATABASE_PASSWORD=contraseña
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Asegúrate de que la base de datos está creada antes de continuar.

## Migraciones

### 5. Ejecutar migraciones en el orden específico
Ejecuta los siguientes comandos en este orden:
```sh
py ./manage.py makemigrations proovedores
py ./manage.py makemigrations inventario_insumos
py ./manage.py makemigrations galletas
py ./manage.py makemigrations usuarios
py ./manage.py makemigrations produccion
py ./manage.py makemigrations ventas
py ./manage.py migrate
```

## Ejecutar el servidor

### 6. Iniciar el servidor de desarrollo
```sh
py ./manage.py runserver
```

El servidor se ejecutará en `http://127.0.0.1:8000/` por defecto.

## Superusuario

### 7. Crear un superusuario
```sh
py ./manage.py createsuperuser
```
Sigue las instrucciones en la terminal para configurar las credenciales del administrador.

## ¡Listo para trabajar!
Ahora puedes acceder al panel de administración en `http://127.0.0.1:8000/admin/` e iniciar sesión con el superusuario creado.

Para más información, consulta la documentación oficial de Django: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

Hola
Hola 3