# ap1-acoplada

Aplicación CRUD en Flask + SQLAlchemy (Python 3.12) con SQLite local y lista para desplegar en AWS (EC2 + ALB + API Gateway).

## Ejecución local
```bash
pip install -r requirements.txt
python app.py
```
Accede en http://127.0.0.1:8000/health

## Despliegue AWS
1. Configura tus credenciales AWS.
2. Ejecuta:
```bash
aws cloudformation deploy --template-file cloudformation.yaml --stack-name ap1-acoplada --capabilities CAPABILITY_NAMED_IAM
```
3. Obtén las URLs del API Gateway y ALB desde los *Outputs* del stack.
