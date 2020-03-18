# Hitmen project

## Comenzando 🚀
_Instrucciones que te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local._

### Pre-requisitos 📋

- _Python 3_

### Instalación 🔧

Usar el adminstrador de paquetes [pip](https://pip.pypa.io/en/stable/).

```bash
pip install virtualenv
```
_Crear un entorno virtual para la instalación de las dependencias._

```bash
virtualenv env_hitmen --python=python3
```
_Activamos el entorno virtual_
```bash
source env_hitmen/bin/activate
```
_Nos dirigimos a la raíz del proyecto y ejecutamos:_
```bash
pip install -r requirements.txt
```
_Ejecutamos el archivo initial_run.sh para aplicar migraciones y cargar los datos iniciales de la base de datos:_
```bash
sh initial_run.sh
```
_para correr el servidor ejecutamos el siguiente comando:_
```bash
python manage.py runserver 0.0.0.0:8000 --settings settings.local --insecure
```

## Usage

```
La base de datos que se carga en local es sqlite.

Los usuarios creados se envio en un documento a su correo con sus usuarios y contraseñas.
```

