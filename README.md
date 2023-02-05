## APP DE CHAT CON DJANGO Y JAVASCRIPT

Este proyecto es una aplicación de chat en tiempo real que permite a los usuarios registrarse y conectarse con otros usuarios de la aplicación. Utiliza las tecnologías de Python, Django, JavaScript, AJAX y está conectado a una base de datos PostgreSQL.

### Funcionalidades

- Registro e inicio de sesión como usuario de la aplicación
- Ver contactos
- Agregar nuevos contactos
- Buscar contactos por filtro
- Ver todos los usuarios de la aplicación
- Eliminar contactos
- Eliminar cuenta propia
- Acceder/crear nueva conversación
- Agregar contacto a la conversación si aún no es un contacto
- Eliminar conversación (esto eliminará automáticamente todos los mensajes en la base de datos)

**TecnologíAs Utilizadas**

- Python
- Django
- JavaScript
- AJAX
- PostgreSQL

**Instalación y configuración**

- Instalar Python y Django en tu equipo siguiendo los pasos en la documentación oficial.
- Instalar PostgreSQL (o el sistema de gestión que desee utilizar) y crear una base de datos para la aplicación. 
- Clonar este repositorio en tu equipo y acceder al directorio de la aplicación.
- Configurar la conexión a la base de datos en el archivo settings.py de Django.
- Ejecutar python manage.py makemigrations y python manage.py migrate para aplicar las migraciones a la base de datos.
- Ejecutar python manage.py runserver para iniciar el servidor de desarrollo.

**Uso**

- Accede a http://127.0.0.1:8000/ en tu navegador para iniciar sesión o registrarte como usuario de la aplicación.
- Una vez registrado, puedes ver tus contactos, agregar nuevos contactos, iniciar conversaciones y más.
- Abre una ventana de incógnito del navegador accediendo al mismo servidor local, crea un usuário, inicia sesión, agrega el contacto con el que hayas iniciado sesión anteriormente e inicia una conversación a tiempo real.

**Consideraciones**

- Este proyecto es solo una base para una aplicación de chat y puede ser modificado y mejorado según las necesidades del usuario.
- La funcionalidad de mensajería en tiempo real es implementada con JavaScript y AJAX.
- Se recomienda tener conocimientos básicos en Python, Django, JavaScript y AJAX antes de modificar este proyecto.
- El diseño no es responsive

Super usuário: 
username: admin.chat
password: adminchat
