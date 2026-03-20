# Reusable Templates Project

Este proyecto está diseñado para proporcionar una estructura reutilizable de plantillas HTML y estilos CSS, facilitando la creación de aplicaciones web modulares y mantenibles.

## Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

```
reusable-templates-project
├── src
│   ├── templates
│   │   ├── base
│   │   │   ├── layout.html        # Estructura básica del HTML
│   │   │   ├── head.html          # Encabezado con metadatos y enlaces a estilos
│   │   │   └── scripts.html       # Scripts necesarios para la aplicación
│   │   ├── components
│   │   │   ├── form
│   │   │   │   ├── form.html      # Estructura general de un formulario
│   │   │   │   ├── field.html     # Campo genérico para formularios
│   │   │   │   ├── input.html     # Campo de entrada
│   │   │   │   ├── select.html    # Campo de selección
│   │   │   │   ├── textarea.html   # Área de texto
│   │   │   │   └── button.html    # Botón
│   │   │   ├── table
│   │   │   │   ├── table.html     # Estructura general de una tabla
│   │   │   │   ├── thead.html     # Cabecera de la tabla
│   │   │   │   └── tbody.html     # Cuerpo de la tabla
│   │   │   └── feedback
│   │   │       ├── alert.html     # Mensaje de alerta
│   │   │       └── validation.html # Mensaje de validación
│   │   ├── modules
│   │   │   ├── users
│   │   │   │   ├── list.html      # Plantilla para listar usuarios
│   │   │   │   ├── create.html    # Plantilla para crear un nuevo usuario
│   │   │   │   └── edit.html      # Plantilla para editar un usuario existente
│   │   │   ├── products
│   │   │   │   ├── list.html      # Plantilla para listar productos
│   │   │   │   ├── create.html    # Plantilla para crear un nuevo producto
│   │   │   │   └── edit.html      # Plantilla para editar un producto existente
│   │   │   └── shared
│   │   │       ├── filters.html    # Estructura de filtros reutilizables
│   │   │       └── modal-form.html # Estructura de un formulario en un modal
│   │   └── pages
│   │       ├── dashboard.html      # Plantilla para el panel de control
│   │       └── settings.html       # Plantilla para la configuración
│   ├── styles
│   │   ├── base.css                # Estilos básicos
│   │   ├── components.css          # Estilos para componentes
│   │   ├── modules.css             # Estilos para módulos
│   │   └── utilities.css           # Estilos utilitarios
│   └── types
│       └── index.ts                # Definiciones de tipos y interfaces
├── package.json                    # Configuración de npm
├── tsconfig.json                   # Configuración de TypeScript
└── README.md                       # Documentación del proyecto
```

## Instalación

Para instalar las dependencias del proyecto, ejecuta:

```
npm install
```

## Uso

Para iniciar el proyecto, puedes utilizar el siguiente comando:

```
npm start
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.