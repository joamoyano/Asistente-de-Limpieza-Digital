
# 🧹 Asistente de Limpieza Digital

**Proyecto en Python para organizar, limpiar y controlar archivos de manera automática y personalizable**. Ideal para mantener carpetas personales, de trabajo o descargas limpias y ordenadas. Incluye simulación, log de acciones, filtros, exclusiones, limpieza total ¡y una consola interactiva mejorada!

---

## 🚀 Funcionalidades principales

- ✅ Organización automática de archivos por tipo (documentos, imágenes, videos, etc.)
- 🎯 Filtros por palabra clave y fecha de modificación
- 🧪 Modo simulación para revisar sin mover archivos
- 📦 Categorías personalizadas desde archivo `.json`
- 🧾 Log completo de acciones realizadas
- 📂 Soporte para subcarpetas (organización profunda)
- 🔁 Modo **Limpieza Total**: ejecuta todo en una sola pasada
- ❌ Detección y eliminación de archivos duplicados
- 🧱 Limpieza de archivos grandes o antiguos
- 🧼 Eliminación de archivos basura o vacíos
- 🔒 Exclusión de rutas sensibles desde `exclusiones.txt`
- 🎨 Interfaz de consola estilizada, organizada por submenús

---

## 🛠️ Tecnologías usadas

- Python 3
- Módulos estándar: `os`, `shutil`, `datetime`, `json`, `hashlib`, `csv`
- Librería externa: [`colorama`](https://pypi.org/project/colorama/) (para colores en consola)
- Compilación opcional con [`PyInstaller`](https://www.pyinstaller.org/) para generar `.exe`

---

## ▶️ Cómo usarlo

1. Cloná el repositorio:

   ```bash
   git clone https://github.com/joamoyano/Asistente-de-Limpieza-Digital.git
   cd Asistente-de-Limpieza-Digital
   ```

2. Instalá el requerimiento:

   ```bash
   pip install colorama
   ```

3. Ejecutá el asistente:

   ```bash
   python main.py
   ```

---

## 🧹 Limpieza Total (Modo automático)

Ejecutá una limpieza completa con:

- Eliminación de duplicados
- Limpieza de archivos grandes y antiguos
- Limpieza de archivos vacíos y basura
- Análisis del uso de espacio
- Log de acciones + resumen del espacio recuperado

---

## ⚙️ Estructura del proyecto

```
Asistente-de-Limpieza-Digital/
├── main.py
├── organizador.py
├── duplicados.py
├── grandes_antiguos.py
├── basura_espacio.py
├── limpieza_total.py
├── utils.py
├── categorias_personalizadas.json
├── exclusiones.txt
├── registro_organizacion.txt
└── README.md
```

---

## 💡 Ideas futuras

- ⌛ Interfaz gráfica con PySimpleGUI o Tkinter
- 📊 Generación de reporte HTML o PDF
- 🛡️ Modo protección: solo mostrar sin modificar
- 📦 Modo batch `.bat` para limpieza automática

---

## 📦 Versión portable

Podés generar el `.exe` con:

```bash
pyinstaller --onefile --console --icon=iconAsis.ico main.py
```

> El ejecutable se guarda en la carpeta `dist/`.

---

## 👨‍💻 Autor

**Joaquín Moyano**  
📌 [LinkedIn](https://www.linkedin.com/in/joaquin-moyano-cba)  
💻 Desarrollador en formación, apasionado por la automatización y las soluciones simples, útiles y reutilizables.

---

## 📜 Licencia

MIT – libre para estudiar, modificar y compartir.
