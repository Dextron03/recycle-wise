# RecycleWise: Revolucionando el reciclaje através de la tecnología

RecycleWise es una aplicación web basada en Django que tiene como objetivo mejorar los esfuerzos de reciclaje en todo el mundo. Mediante la integración de algoritmos de machine learning, nuestro proyecto ofrece un sistema de detección inteligente que identifica con precisión varios tipos de materiales reciclables a partir de video en tiempo real. Este proyecto no solo busca hacer que el reciclaje sea más accesible y eficiente, sino que también tiene como objetivo educar e involucrar a la comunidad sobre la importancia del reciclaje para la sostenibilidad ambiental.

## Características principales

- **Detección Avanzada de Materiales**: En el corazón de RecycleWise está su potente capacidad de detección de materiales, impulsada por un modelo de machine learning (`modelos/best.pt`). Este modelo puede distinguir entre diferentes materiales reciclables, como plásticos, metales, vidrio y papel, con una precisión media-alta.

- **Interfaz de Usuario Interactiva**: La aplicación cuenta con una interfaz web fácil de usar que simplifica el proceso de detección de materiales. Está diseñada para garantizar una experiencia fluida para usuarios de todas las edades.

## Especificaciones técnicas

- **Framework Backend**: Django 5.0.6, elegido por su escalabilidad y facilidad de uso en la construcción de aplicaciones web complejas.
- **Biblioteca de Aprendizaje Automático**: PyTorch, utilizado para entrenar e implementar el modelo de detección de materiales.
- **Tecnologías Frontend**: HTML5, CSS3 y JavaScript, asegurando una interfaz web moderna y receptiva.
- **Base de Datos**: SQLite (por defecto), con soporte para PostgreSQL en entornos de producción.

## Comenzando con RecycleWise

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:
- Python 3.8 o superior
- Django 5.0.6
- PyTorch (para ejecutar el modelo de aprendizaje automático)
- Otras dependencias listadas en `requirements.txt`

### Guía de Instalación

1. **Clonar el Repositorio del Proyecto**:
   ```sh
   git clone https://github.com/tuusuario/RecycleWise.git
   ```

2. **Navegar al Directorio del Proyecto**:
   ```sh
   cd RecycleWise
   ```

3. **Instalar Paquetes Python Requeridos**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Configuración de la Base de Datos**:
   Aplica las migraciones de Django para configurar el esquema de tu base de datos:
   ```sh
   python manage.py migrate
   ```

5. **Iniciar el Servidor de Desarrollo**:
   Corre la aplicación localmente:
   ```sh
   python manage.py runserver
   ```

## Cómo usar la app

Después de correr el servidor puedes acceder a la aplicación yendo a la URL `http://127.0.0.1:8000/` en el navegador. La detección de objetos es en vivo, por lo que solo debes poner un objeto delante de la cámara y será reconocido y clasificado deacuerdo al material.

## Desarrollo y personalización

- **Modelos**: Mejora o personaliza los modelos de base de datos dentro de `detection/models.py` para ajustarse a tus requisitos específicos.
- **Vistas**: Implementa o modifica la lógica de la aplicación en `detection/views.py` para controlar cómo se procesan y presentan los datos.
- **Archivos Estáticos**: Puedes actualizar el aspecto y la sensación de la app modificando los estilos CSS en `static/css/style.css`.

## Contribuir a RecycleWise

Damos la bienvenida a las contribuciones de desarrolladores, ambientalistas y cualquier persona apasionada por el reciclaje. Ya sean correcciones de errores, mejoras de características o mejoras en la documentación, su aporte es valioso. Puedes hacer un fork del repositorio o crear un pull request para ser revisado y aprobado.
