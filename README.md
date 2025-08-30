# FastAPI Backstage Demo

API de ejemplo en FastAPI para demostrar la integración con Backstage y herramientas de DevOps.

## 🚀 Características

- **FastAPI** con documentación automática OpenAPI
- **Health checks** para Kubernetes
- **Metrics endpoint** para Prometheus
- **CORS** habilitado
- **Docker** ready
- **Kubernetes manifests** incluidos
- **Backstage catalog** configurado

## 📋 Endpoints

- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /metrics` - Métricas básicas
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc
- `GET /items` - Listar items
- `POST /items` - Crear item
- `GET /items/{id}` - Obtener item por ID
- `PUT /items/{id}` - Actualizar item
- `DELETE /items/{id}` - Eliminar item

## 🛠️ Desarrollo Local

### Prerequisitos
- Python 3.11+
- pip

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar
```bash
# Desarrollo
uvicorn main:app --reload

# Producción
python main.py
```

La API estará disponible en: http://localhost:8000

## 🐳 Docker

### Build
```bash
docker build -t fastapi-backstage-demo .
```

### Run
```bash
docker run -p 8000:8000 fastapi-backstage-demo
```

## ☸️ Kubernetes

### Desplegar en K3s
```bash
kubectl apply -f k8s/
```

### Verificar deployment
```bash
kubectl get pods -l app=fastapi-backstage-demo
kubectl get svc fastapi-backstage-demo
kubectl get ingress fastapi-backstage-demo
```

### Acceder a la aplicación
- **Local**: http://localhost:8000
- **Kubernetes**: https://fastapi-demo.cloud-it.com.ar

## 📊 Monitoreo

### Health Check
```bash
curl https://fastapi-demo.cloud-it.com.ar/health
```

### Métricas
```bash
curl https://fastapi-demo.cloud-it.com.ar/metrics
```

## 🎯 Integraciones Backstage

Este proyecto está configurado para integrarse con:

- ✅ **Backstage Catalog** - Registro automático de componente
- ⏳ **ArgoCD** - Deployment automation
- ⏳ **Grafana** - Métricas y dashboards
- ⏳ **Kubecost** - Cost monitoring
- ⏳ **Service Mesh** - Traffic management

## 📝 TODO: Próximas Integraciones

1. **CI/CD Pipeline** (GitHub Actions)
2. **ArgoCD Application** 
3. **Grafana Dashboard**
4. **Prometheus ServiceMonitor**
5. **Service Mesh annotations**
6. **Cost tracking labels**

## 🏗️ Arquitectura

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Backstage │    │     K3s      │    │   Traefik   │
│   Catalog   │───▶│   Cluster    │◀───│   Ingress   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                   ┌───────▼────────┐
                   │  FastAPI Demo  │
                   │      App       │
                   └────────────────┘
```