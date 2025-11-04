# ap1-acoplada-nlb (AWS Academy Compatible)

## Arquitectura
API Gateway → NLB → EC2 (Flask + Gunicorn) → DynamoDB

## Despliegue
1. Sube este proyecto a GitHub (https://github.com/enrique-eg/ap1-acoplada).
2. Sube `cloudformation.yaml` a AWS CloudFormation.
3. Espera hasta que el estado sea CREATE_COMPLETE.
4. Prueba el endpoint en `Outputs > ApiURL`.

## Endpoints CRUD
- GET /items
- POST /items
- GET /items/<id>
- PUT /items/<id>
- DELETE /items/<id>
