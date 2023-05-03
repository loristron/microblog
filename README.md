# Microblog API

Aplicação backend de microblog 

## Projeto
- GCP: `microblog`
- GCP ID: `microblog-loristron`
- Cloud Run Service name: `microblog-api`
- URL: https://microblog-api-iacvkh5bga-rj.a.run.app/

## Tecnologias
- Python
- Docker
- CloudSQL

## Instruções

### Deploy

1. Na pasta `src/`
```
gcloud run deploy

```
```
Service name (src): microblog-api
```
### Local

```
ptyhon3 -m venv env
```

```
source env/bin/activate 
```

```
cd src/
```
```
source secrets_reveal.sh
```

```
python3 main.py
```

