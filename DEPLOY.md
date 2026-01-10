# Vampire VTT - Guia de Deploy

**Objetivo:** Deploy gratuito para jogar com amigos

---

## Arquitetura Recomendada (Gratuita)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Vercel      │     │    Railway      │     │   PostgreSQL    │
│   (Frontend)    │────▶│   (Backend)     │────▶│   (Railway)     │
│     GRÁTIS      │     │  $5/mês grátis  │     │     GRÁTIS      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Por que essa arquitetura?

| Requisito | Por que não Vercel pro backend? |
|-----------|--------------------------------|
| WebSockets | Vercel é serverless, não mantém conexões |
| SQLite/PostgreSQL | Vercel não tem storage persistente |
| Long-running | Funções Vercel têm timeout de 10s |

---

## 1. Preparar Repositório GitHub

Se ainda não tem:
```bash
cd "F:\Vampire VTT\vampire-vtt"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/vampire-vtt.git
git push -u origin main
```

---

## 2. Deploy do Frontend (Vercel)

### Passo a passo:
1. Acesse [vercel.com](https://vercel.com) e crie conta
2. Clique "Add New Project"
3. Importe o repositório do GitHub
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### Variável de ambiente:
```
VITE_API_URL=https://seu-backend.railway.app
```
(Adicionar depois de ter a URL do Railway)

### Arquivo opcional `frontend/vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

---

## 3. Deploy do Backend (Railway)

### Passo a passo:
1. Acesse [railway.app](https://railway.app) e crie conta
2. "New Project" → "Deploy from GitHub repo"
3. Selecione o repositório
4. Configure Root Directory: `backend`

### Criar arquivo `backend/Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Criar arquivo `backend/runtime.txt`:
```
python-3.12
```

### Criar arquivo `backend/railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

### Variáveis de ambiente no Railway:
```
ENVIRONMENT=production
JWT_SECRET=gerar-uma-chave-secreta-muito-forte-aqui
CORS_ORIGINS=https://seu-frontend.vercel.app
DATABASE_URL=(Railway fornece automaticamente com PostgreSQL)
```

---

## 4. Adicionar PostgreSQL no Railway

1. No projeto Railway, clique "New"
2. Selecione "Database" → "PostgreSQL"
3. Railway automaticamente cria `DATABASE_URL`

---

## 5. Modificar Backend para PostgreSQL

### Atualizar `backend/requirements.txt`:
Adicionar:
```
asyncpg
psycopg2-binary
```

### Atualizar `backend/app/database.py`:

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Pegar URL do ambiente ou usar SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./vampire_vtt.db")

# Railway usa postgres://, mas SQLAlchemy precisa de postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Configurar engine baseado no tipo de banco
if DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True
    )

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Atualizar `backend/app/config.py`:
```python
import os

class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # JWT
    jwt_secret = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    jwt_algorithm = "HS256"
    jwt_expire_minutes = 60 * 24 * 7  # 7 dias

    # CORS
    cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

    # Discord OAuth (opcional)
    discord_client_id = os.getenv("DISCORD_CLIENT_ID", "")
    discord_client_secret = os.getenv("DISCORD_CLIENT_SECRET", "")
    discord_redirect_uri = os.getenv("DISCORD_REDIRECT_URI", "")

    # Frontend URL
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

settings = Settings()
```

---

## 6. Adicionar Health Check

### Criar `backend/app/api/health.py`:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Registrar em `backend/app/main.py`:
```python
from app.api import health
app.include_router(health.router, prefix="/api", tags=["health"])
```

---

## 7. Checklist Pré-Deploy

### Backend
- [ ] Criar `Procfile`
- [ ] Criar `runtime.txt`
- [ ] Criar `railway.toml`
- [ ] Atualizar `database.py` para PostgreSQL
- [ ] Atualizar `config.py` para variáveis de ambiente
- [ ] Adicionar `asyncpg` e `psycopg2-binary` ao requirements.txt
- [ ] Criar endpoint `/api/health`
- [ ] Gerar JWT_SECRET forte: `python -c "import secrets; print(secrets.token_hex(32))"`

### Frontend
- [ ] Criar `vercel.json` (opcional)
- [ ] Testar build: `npm run build`
- [ ] Verificar se não há erros de TypeScript

### Git
- [ ] Commitar todas as mudanças
- [ ] Push para GitHub

---

## 8. Ordem de Deploy

1. **Railway primeiro** (backend)
   - Deploy e pegar URL (ex: `vampire-vtt-backend.railway.app`)

2. **Vercel depois** (frontend)
   - Configurar `VITE_API_URL` com URL do Railway
   - Deploy

3. **Atualizar CORS no Railway**
   - Adicionar URL do Vercel em `CORS_ORIGINS`

---

## Custos Estimados

| Serviço | Plano | Custo | Limite |
|---------|-------|-------|--------|
| Vercel | Hobby | Grátis | 100GB bandwidth/mês |
| Railway | Trial | Grátis | $5 crédito/mês |
| PostgreSQL | Railway | Incluso | 1GB storage |

**Total mensal: R$ 0** (para uso casual com amigos)

---

## Alternativas de Deploy

### Se Railway não for suficiente:

| Serviço | Prós | Contras |
|---------|------|---------|
| **Render.com** | Free tier | Dorme após 15min inativo |
| **Fly.io** | 3 VMs grátis | Config mais complexa |
| **DigitalOcean** | $4/mês droplet | Pago |
| **Heroku** | Fácil | Não tem mais free tier |

---

## Troubleshooting

### CORS Error
- Verificar se URL do frontend está em `CORS_ORIGINS`
- Incluir protocolo: `https://seu-site.vercel.app`

### WebSocket não conecta
- Railway suporta WebSockets nativamente
- Verificar URL: `wss://seu-backend.railway.app/ws/...`

### Database connection error
- Verificar se PostgreSQL está rodando no Railway
- Verificar se `DATABASE_URL` está configurada

### Build falha no Vercel
- Verificar erros de TypeScript: `npm run build` local
- Verificar se todas as dependências estão no package.json

---

## Comandos Úteis

### Gerar JWT Secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Testar build local:
```bash
# Frontend
cd frontend && npm run build

# Backend
cd backend && pip install -r requirements.txt
```

### Ver logs Railway:
```bash
railway logs
```

### Ver logs Vercel:
```bash
vercel logs seu-projeto.vercel.app
```
