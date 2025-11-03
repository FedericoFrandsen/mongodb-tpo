// Empresas

db.empresas.insertMany([
  {
    "nombre": "Tech Solutions",
    "industria": "Software",
    "descripcion": "Empresa dedicada al desarrollo de aplicaciones web y móviles.",
    "contacto": {
      "direccion": "Av. Corrientes 1234, CABA, Argentina",
      "email": "contacto@techsolutions.com",
      "telefono": "011-1234-5678"
    },
    "empleados_rrhh": [
      { "nombre": "Laura Gómez", "email": "laura@techsolutions.com", "rol": "RRHH" }
    ],
    "fecha_creacion": ISODate("2023-01-15")
  },
  {
    "nombre": "Data Corp",
    "industria": "Consultoría",
    "descripcion": "Consultoría especializada en análisis de datos y BI.",
    "contacto": {
      "direccion": "El Salvador 5860, CABA, Argentina",
      "email": "info@datacorp.com",
      "telefono": "011-9876-5432"
    },
    "empleados_rrhh": [
      { "nombre": "Miguel Torres", "email": "miguel@datacorp.com", "rol": "RRHH" }
    ],
    "fecha_creacion": ISODate("2022-05-10")
  },
  {
    "nombre": "Innovatech",
    "industria": "Tecnología",
    "descripcion": "Startup enfocada en inteligencia artificial y soluciones IoT.",
    "contacto": {
      "direccion": "Av. Libertador 789, CABA, Argentina",
      "email": "contacto@innovatech.ai",
      "telefono": "011-5678-1234"
    },
    "empleados_rrhh": [
      { "nombre": "Sofía Ramírez", "email": "sofia@innovatech.ai", "rol": "RRHH" }
    ],
    "fecha_creacion": ISODate("2024-03-20")
  }
])

// Ofertas 

db.ofertas.insertMany([
  {
    "empresa_id": db.empresas.findOne({ nombre: "Tech Solutions" })._id,
    "puesto": "Desarrollador Backend",
    "descripcion": "Se busca desarrollador con experiencia en Node.js y MongoDB.",
    "requerimientos": [
      { habilidad: "Node.js", nivel: 7 },
      { habilidad: "Express", nivel: 6 },
      { habilidad: "MongoDB", nivel: 6 },
      { habilidad: "APIs REST", nivel: 6 }
    ],
    "ubicacion": "Remoto",
    "modalidad": "remoto",
    "estado": "abierta",
    "fecha_creacion": ISODate("2025-10-01")
  },
  {
    "empresa_id": db.empresas.findOne({ nombre: "Data Corp" })._id,
    "puesto": "Analista de Datos",
    "descripcion": "Analista para proyectos de BI y dashboards con SQL y Power BI.",
    "requerimientos": [
      { habilidad: "SQL", nivel: 8 },
      { habilidad: "Power BI", nivel: 7 },
      { habilidad: "Python", nivel: 6 },
      { habilidad: "Estadística", nivel: 7 }
    ],
    "ubicacion": "CABA",
    "modalidad": "presencial",
    "estado": "abierta",
    "fecha_creacion": ISODate("2025-09-20")
  },
  {
    "empresa_id": db.empresas.findOne({ nombre: "Innovatech" })._id,
    "puesto": "Especialista en IA",
    "descripcion": "Desarrollar soluciones de inteligencia artificial y machine learning.",
    "requerimientos": [
      { habilidad: "Machine Learning", nivel: 7 },
      { habilidad: "Python", nivel: 8 },
      { habilidad: "TensorFlow", nivel: 6 },
      { habilidad: "Análisis de datos", nivel: 7 }
    ],
    "ubicacion": "CABA",
    "modalidad": "híbrido",
    "estado": "abierta",
    "fecha_creacion": ISODate("2025-09-25")
  }
])

// Candidatos 

db.candidatos.insertMany([
  {
    "informacion_personal": {
      "nombre_apellido": "Rosario Martinez",
      "fecha_nacimiento": ISODate("2000-02-17"),
      "email": "rosario.martinez@hotmail.com",
      "celular": "342-4301-885",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_rosario"
    },
    "estado": "activo",
    "experiencia_laboral": [
      {
        "empresa_id": db.empresas.findOne({ nombre: "Tech Solutions" })._id,
        "puesto": "Junior Backend Developer",
        "fecha_desde": ISODate("2023-03-01"),
        "fecha_hasta": ISODate("2024-12-31"),
        "descripcion": "Desarrollo de APIs y mantenimiento de bases de datos MongoDB."
      }
    ],
    "experiencia_academica": [
      {
        "titulo": "Licenciatura en Sistemas",
        "grado": "Licenciado",
        "institucion": "Universidad Nacional de Buenos Aires",
        "estado": "finalizado",
        "fecha_desde": ISODate("2018-03-01"),
        "fecha_hasta": ISODate("2022-12-15")
      }
    ],
    "habilidades": {
      "tecnicas": [
        { nombre: "SQL", nivel: 7 },
        { nombre: "Power BI", nivel: 6 },
        { nombre: "Excel", nivel: 5 },
        { nombre: "Python", nivel: 6 }
      ],
      "blandas": [
        { "nombre": "Trabajo en equipo", "nivel": 8 },
        { "nombre": "Comunicación", "nivel": 7 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-05") },
    "fecha_creacion": ISODate("2025-10-01"),
    "fecha_ultima_actualizacion": ISODate("2025-10-05")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Marcos Pereyra",
      "fecha_nacimiento": ISODate("1995-07-12"),
      "email": "marcos.pereyra@gmail.com",
      "celular": "011-4511-667",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_marcos"
    },
    "estado": "activo",
    "experiencia_laboral": [
      {
        "empresa_id": db.empresas.findOne({ nombre: "Data Corp" })._id,
        "puesto": "Analista Junior",
        "fecha_desde": ISODate("2022-01-15"),
        "fecha_hasta": ISODate("2024-08-31"),
        "descripcion": "Análisis de datos, generación de reportes y dashboards en Power BI."
      }
    ],
    "experiencia_academica": [
      {
        "titulo": "Ingeniería en Sistemas",
        "grado": "Ingeniero",
        "institucion": "Universidad Tecnológica Nacional",
        "estado": "finalizado",
        "fecha_desde": ISODate("2015-03-01"),
        "fecha_hasta": ISODate("2020-12-15")
      }
    ],
    "habilidades": {
      "tecnicas": [
        { nombre: "Node.js", nivel: 7 },
        { nombre: "JavaScript", nivel: 7 },
        { nombre: "MongoDB", nivel: 6 },
        { nombre: "APIs REST", nivel: 6 }
      ],
      "blandas": [
        { "nombre": "Análisis crítico", "nivel": 9 },
        { "nombre": "Resolución de problemas", "nivel": 8 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-09-22") },
    "fecha_creacion": ISODate("2025-09-20"),
    "fecha_ultima_actualizacion": ISODate("2025-09-22")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Camila Gebara",
      "fecha_nacimiento": ISODate("1998-11-03"),
      "email": "camilagebara@gmail.com",
      "celular": "342-3440-934",
      "residencia": "Santa Fe",
      "foto": null,
      "CV": "gridfs://cv_camila"
    },
    "estado": "activo",
    "experiencia_laboral": [
      {
        "empresa_id": db.empresas.findOne({ nombre: "Innovatech" })._id,
        "puesto": "Data Scientist",
        "fecha_desde": ISODate("2023-05-01"),
        "fecha_hasta": ISODate("2025-09-15"),
        "descripcion": "Desarrollo de modelos de Machine Learning y análisis de datos."
      }
    ],
    "experiencia_academica": [
      {
        "titulo": "Maestría en Inteligencia Artificial",
        "grado": "Magíster",
        "institucion": "Universidad de Buenos Aires",
        "estado": "finalizado",
        "fecha_desde": ISODate("2021-03-01"),
        "fecha_hasta": ISODate("2023-12-15")
      }
    ],
    "habilidades": {
      "tecnicas": [
        { nombre: "Machine Learning", nivel: 7 },
        { nombre: "Python", nivel: 8 },
        { nombre: "TensorFlow", nivel: 6 },
        { nombre: "Data Analysis", nivel: 7 }
      ],
      "blandas": [
        { "nombre": "Creatividad", "nivel": 9 },
        { "nombre": "Trabajo en equipo", "nivel": 8 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-09-28") },
    "fecha_creacion": ISODate("2025-09-25"),
    "fecha_ultima_actualizacion": ISODate("2025-09-28")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Lucía Fernández",
      "fecha_nacimiento": ISODate("1999-05-10"),
      "email": "lucia.fernandez@gmail.com",
      "celular": "11-6789-1122",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_lucia"
    },
    "estado": "activo",
    "habilidades": {
      "tecnicas": [
        { "nombre": "Node.js", "nivel": 7 },
        { "nombre": "Express", "nivel": 6 },
        { "nombre": "MongoDB", "nivel": 5 },
        { "nombre": "APIs REST", "nivel": 7 }
      ],
      "blandas": [
        { "nombre": "Trabajo en equipo", "nivel": 8 },
        { "nombre": "Comunicación", "nivel": 7 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-20") },
    "fecha_creacion": ISODate("2025-10-20"),
    "fecha_ultima_actualizacion": ISODate("2025-10-20")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Julián Torres",
      "fecha_nacimiento": ISODate("1997-09-18"),
      "email": "julian.torres@gmail.com",
      "celular": "11-4322-9987",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_julian"
    },
    "estado": "activo",
    "habilidades": {
      "tecnicas": [
        { "nombre": "SQL", "nivel": 8 },
        { "nombre": "Power BI", "nivel": 7 },
        { "nombre": "Python", "nivel": 6 },
        { "nombre": "Estadística", "nivel": 8 }
      ],
      "blandas": [
        { "nombre": "Pensamiento analítico", "nivel": 9 },
        { "nombre": "Responsabilidad", "nivel": 8 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-18") },
    "fecha_creacion": ISODate("2025-10-18"),
    "fecha_ultima_actualizacion": ISODate("2025-10-18")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Tomás Herrera",
      "fecha_nacimiento": ISODate("1996-01-27"),
      "email": "tomas.herrera@outlook.com",
      "celular": "341-550-2211",
      "residencia": "Santa Fe",
      "foto": null,
      "CV": "gridfs://cv_tomas"
    },
    "estado": "activo",
    "habilidades": {
      "tecnicas": [
        { "nombre": "Machine Learning", "nivel": 7 },
        { "nombre": "Python", "nivel": 8 },
        { "nombre": "TensorFlow", "nivel": 6 },
        { "nombre": "Data Analysis", "nivel": 7 }
      ],
      "blandas": [
        { "nombre": "Creatividad", "nivel": 9 },
        { "nombre": "Trabajo en equipo", "nivel": 8 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-19") },
    "fecha_creacion": ISODate("2025-10-19"),
    "fecha_ultima_actualizacion": ISODate("2025-10-19")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Valentina Ruiz",
      "fecha_nacimiento": ISODate("2000-03-12"),
      "email": "valentina.ruiz@gmail.com",
      "celular": "11-5566-7788",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_valentina"
    },
    "estado": "activo",
    "habilidades": {
      "tecnicas": [
        { "nombre": "Node.js", "nivel": 6 },
        { "nombre": "Express", "nivel": 5 },
        { "nombre": "MongoDB", "nivel": 6 },
        { "nombre": "APIs REST", "nivel": 5 }
      ],
      "blandas": [
        { "nombre": "Comunicación", "nivel": 8 },
        { "nombre": "Trabajo en equipo", "nivel": 7 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-21") },
    "fecha_creacion": ISODate("2025-10-21"),
    "fecha_ultima_actualizacion": ISODate("2025-10-21")
  },
  {
    "informacion_personal": {
      "nombre_apellido": "Santiago López",
      "fecha_nacimiento": ISODate("1998-08-05"),
      "email": "santiago.lopez@gmail.com",
      "celular": "11-9988-7766",
      "residencia": "CABA",
      "foto": null,
      "CV": "gridfs://cv_santiago"
    },
    "estado": "activo",
    "habilidades": {
      "tecnicas": [
        { "nombre": "SQL", "nivel": 7 },
        { "nombre": "Power BI", "nivel": 6 },
        { "nombre": "Python", "nivel": 5 },
        { "nombre": "Estadística", "nivel": 7 }
      ],
      "blandas": [
        { "nombre": "Resolución de problemas", "nivel": 8 },
        { "nombre": "Análisis crítico", "nivel": 7 }
      ]
    },
    "ultimo_evento_seleccion": { "estado": "aplicado", "fecha": ISODate("2025-10-22") },
    "fecha_creacion": ISODate("2025-10-22"),
    "fecha_ultima_actualizacion": ISODate("2025-10-22")
  }
])

// Postulaciones

db.postulaciones.insertMany([
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id,
    empresa_id: db.empresas.findOne({ nombre: "Tech Solutions" })._id,
    trabajo_id: db.ofertas.findOne({ puesto: "Desarrollador Backend" })._id,
    estado: "aplicado",
    fecha_creacion: ISODate("2025-10-05")
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id,
    empresa_id: db.empresas.findOne({ nombre: "Data Corp" })._id,
    trabajo_id: db.ofertas.findOne({ puesto: "Analista de Datos" })._id,
    estado: "en proceso",
    fecha_creacion: ISODate("2025-09-22")
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id,
    empresa_id: db.empresas.findOne({ nombre: "Innovatech" })._id,
    trabajo_id: db.ofertas.findOne({ puesto: "Especialista en IA" })._id,
    estado: "rechazado",
    fecha_creacion: ISODate("2025-09-28")
  },
    {
    "candidato_id": db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Lucía Fernández" })._id,
    "empresa_id": db.empresas.findOne({ "nombre": "Tech Solutions" })._id,
    "trabajo_id": db.ofertas.findOne({ "puesto": "Desarrollador Backend" })._id,
    "estado": "en proceso",
    "fecha_creacion": ISODate("2025-10-20")
  },
  {
    "candidato_id": db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Julián Torres" })._id,
    "empresa_id": db.empresas.findOne({ "nombre": "Data Corp" })._id,
    "trabajo_id": db.ofertas.findOne({ "puesto": "Analista de Datos" })._id,
    "estado": "aplicado",
    "fecha_creacion": ISODate("2025-10-18")
  },
  {
    "candidato_id": db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Tomás Herrera" })._id,
    "empresa_id": db.empresas.findOne({ "nombre": "Innovatech" })._id,
    "trabajo_id": db.ofertas.findOne({ "puesto": "Especialista en IA" })._id,
    "estado": "aplicado",
    "fecha_creacion": ISODate("2025-10-19")
  },
  {
    "candidato_id": db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Valentina Ruiz" })._id,
    "empresa_id": db.empresas.findOne({ "nombre": "Tech Solutions" })._id,
    "trabajo_id": db.ofertas.findOne({ "puesto": "Desarrollador Backend" })._id,
    "estado": "aplicado",
    "fecha_creacion": ISODate("2025-10-21")
  },
  {
    "candidato_id": db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Santiago López" })._id,
    "empresa_id": db.empresas.findOne({ "nombre": "Data Corp" })._id,
    "trabajo_id": db.ofertas.findOne({ "puesto": "Analista de Datos" })._id,
    "estado": "en proceso",
    "fecha_creacion": ISODate("2025-10-22")
  }
])

// Entrevistas

db.entrevistas.insertMany([
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id,
    postulacion_id: db.postulaciones.findOne({ candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id })._id,
    tipo: "presentacion",
    fecha: ISODate("2025-10-06"),
    feedback: "Buena presentación, interesado en el proyecto.",
    entrevistador: { nombre: "Laura Gómez", email: "laura@techsolutions.com" }
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id,
    postulacion_id: db.postulaciones.findOne({ candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id })._id,
    tipo: "tecnica",
    fecha: ISODate("2025-09-25"),
    feedback: "Habilidades técnicas adecuadas, requiere entrenamiento en Power BI avanzado.",
    entrevistador: { nombre: "Miguel Torres", email: "miguel@datacorp.com" }
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id,
    postulacion_id: db.postulaciones.findOne({ candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id })._id,
    tipo: "cierre",
    fecha: ISODate("2025-09-29"),
    feedback: "Candidato no seleccionado: falta experiencia práctica en producción para el puesto requerido.",
    entrevistador: { nombre: "Sofía Ramírez", email: "sofia@innovatech.ai" }
  }
])

// Versiones_Perfil

db.versiones_perfil.insertMany([
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id,
    version: 1,
    fecha: ISODate("2025-10-01"), 
    cambio: "Creación de perfil inicial",
    diff: null
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id,
    version: 2,
    fecha: ISODate("2025-10-05"), 
    cambio: "Actualización de experiencia laboral y habilidades",
    diff: { experiencia_laboral: "Se agregó experiencia en Tech Solutions", habilidades: ["Node.js", "MongoDB"] }
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id,
    version: 1,
    fecha: ISODate("2025-09-20"), 
    cambio: "Creación de perfil inicial",
    diff: null
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id,
    version: 2,
    fecha: ISODate("2025-09-22"), 
    cambio: "Actualización de experiencia y habilidades técnicas",
    diff: { experiencia_laboral: "Se agregó Data Corp", habilidades: ["SQL", "Power BI"] }
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id,
    version: 1,
    fecha: ISODate("2025-09-25"), 
    cambio: "Creación de perfil inicial",
    diff: null
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id,
    version: 2,
    fecha: ISODate("2025-09-28"), 
    cambio: "Actualización de habilidades técnicas",
    diff: { habilidades: ["Python", "Machine Learning"]}
  }
])

// Cursos

db.cursos.insertMany([
  {
    "titulo": "Node.js Avanzado",
    "formato": "video",
    "duracion_h": 15,
    "etiquetas": "Node.js, Backend, JavaScript",
    "contenido_url": "https://example.com/nodejs"
  },
  {
    "titulo": "Power BI Avanzado",
    "formato": "video",
    "duracion_h": 10,
    "etiquetas": "Power BI, BI, Dashboard",
    "contenido_url": "https://example.com/powerbi"
  },
  {
    "titulo": "Machine Learning con Python",
    "formato": "pdf",
    "duracion_h": 20,
    "etiquetas": "Python, Machine Learning, IA",
    "contenido_url": "https://example.com/mlpython"
  },
  {
    "titulo": "SQL Intermedio",
    "formato": "live",
    "duracion_h": 12,
    "etiquetas": "SQL, Base de Datos, Consultas",
    "contenido_url": "https://example.com/sql"
  },
  {
    "titulo": "Comunicación Efectiva",
    "formato": "video",
    "duracion_h": 5,
    "etiquetas": "Habilidades Blandas, Comunicación, Trabajo en equipo",
    "contenido_url": "https://example.com/comunicacion"
  }
])

// Inscripciones

db.inscripciones.insertMany([
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Rosario Martinez" })._id,
    curso_id: db.cursos.findOne({ titulo: "Node.js Avanzado" })._id,
    progreso: 100,
    nota: 9,
    fecha_inicio: ISODate("2025-10-01"),
    fecha_fin: ISODate("2025-10-15")
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Marcos Pereyra" })._id,
    curso_id: db.cursos.findOne({ titulo: "Power BI Avanzado" })._id,
    progreso: 80,
    nota: null,
    fecha_inicio: ISODate("2025-09-21"),
    fecha_fin: null
  },
  {
    candidato_id: db.candidatos.findOne({ "informacion_personal.nombre_apellido": "Camila Gebara" })._id,
    curso_id: db.cursos.findOne({ titulo: "Machine Learning con Python" })._id,
    progreso: 50,
    nota: null,
    fecha_inicio: ISODate("2025-09-28"),
    fecha_fin: null
  }
])




