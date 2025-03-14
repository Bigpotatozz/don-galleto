# Proyecto Django

Este proyecto utiliza Django como framework de desarrollo web. A continuación, se describen los comandos esenciales para configurar y migrar la base de datos.

## Activar el entorno virtual

Antes de ejecutar cualquier comando, es necesario activar el entorno virtual. Para hacerlo, usa el siguiente comando:

```sh
./env/Scripts/activate
```

Este comando activa el entorno virtual ubicado en la carpeta `env`, permitiendo el uso de las dependencias del proyecto.

## Generar archivos de migración

Para crear los archivos de migración a partir de los modelos definidos en el proyecto, ejecuta:

```sh
py ./manage.py makemigrations
```

Este comando genera archivos de migración en la carpeta `migrations` dentro de cada aplicación de Django.

## Aplicar migraciones a la base de datos

Para aplicar las migraciones y sincronizar la base de datos con los modelos de Django, usa:

```sh
py ./manage.py migrate --fake-initial
```

El parámetro `--fake-initial` es útil cuando la base de datos ya contiene las tablas y se quiere registrar el estado inicial sin aplicar cambios adicionales.

## Script de Base de Datos

El script de la base de datos se encuentra en el repositorio. Asegúrate de revisar los archivos correspondientes para su correcta implementación.

---

Para cualquier duda o problema, revisa la documentación oficial de Django o consulta con el equipo de desarrollo.

