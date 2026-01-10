# Vampire VTT

Virtual Tabletop completo para Vampire: The Masquerade, suportando V5 e V20.

## Tecnologias

### Backend
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 (async) - SQLite/PostgreSQL
- WebSockets para tempo real
- JWT + Discord OAuth para autenticacao

### Frontend
- React 18 + TypeScript
- Vite
- Zustand para estado
- TanStack Query
- Tailwind CSS (tema gotico)

## Estrutura do Projeto

```
vampire-vtt/
├── backend/
│   ├── app/
│   │   ├── api/           # 12 modulos de endpoints
│   │   ├── core/          # Engine de regras (V5/V20)
│   │   ├── game_data/     # Dados estaticos (clas, disciplinas)
│   │   ├── models/        # 13 models do banco
│   │   ├── schemas/       # Schemas Pydantic
│   │   ├── services/      # Logica de negocio
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── alembic/           # Migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         # 10 paginas principais
│   │   ├── components/    # Organizados por feature
│   │   ├── stores/        # Estado Zustand
│   │   ├── lib/           # API client, utils
│   │   ├── types/         # TypeScript types
│   │   └── hooks/
│   └── package.json
├── docker-compose.yml
├── DEPLOY.md              # Guia de deploy
└── ESTADO_ATUAL.md        # Status do projeto
```

## Como Executar

### Desenvolvimento Local (Recomendado)

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Acessar
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

### Com Docker

```bash
cp backend/.env.example backend/.env
docker-compose up -d
```

## Funcionalidades Implementadas

### Sistema de Autenticacao
- Login com Email/Senha
- Discord OAuth
- Recuperacao de senha por email
- JWT tokens persistentes

### Cronicas e Campanhas
- Criar/gerenciar cronicas (V5 ou V20)
- Codigos de convite para jogadores
- Papeis: Narrador (ST) e Jogadores

### Personagens
- Fichas completas V5 e V20
- Sistema de aprovacao pelo Narrador
- Mudancas pendentes para fichas aprovadas
- Notificacoes de alteracoes
- Historico de modificacoes

### Sessoes de Jogo
- Iniciar/encerrar sessoes formais
- Rastrear participantes
- XP automatico ao encerrar sessao

### Sistema de XP
- Requisicoes de gasto de XP
- Aprovacao pelo Narrador
- Historico de transacoes
- XP aplicado direto na ficha

### Rolagem de Dados

#### V5 (5th Edition)
- Hunger Dice integrado
- Messy Criticals e Bestial Failures
- Rouse Checks
- Frenzy Checks
- Remorse Checks
- Blood Potency

#### V20 (20th Anniversary)
- Sistema classico de dados
- Botch (falha critica)
- Especialidades (reroll 10s)
- Blood Pool por geracao

### Sistema de Combate
- Tracker de Iniciativa
- Gerenciamento de rodadas
- Adicionar/remover combatentes
- Avancar turnos

### Chat em Tempo Real
- Mensagens persistentes
- WebSocket integrado
- Historico paginado

### Cenas
- Criar locais/cenas na cronica
- Ativar/desativar cenas
- Contextualizar a narrativa

## API Endpoints Principais

| Recurso | Endpoints |
|---------|-----------|
| Auth | `/api/auth/*` - login, registro, OAuth, reset senha |
| Chronicles | `/api/chronicles/*` - CRUD, convites, membros |
| Characters | `/api/characters/*` - fichas, aprovacao, notificacoes |
| Sessions | `/api/sessions/*` - iniciar/encerrar, participantes |
| XP | `/api/xp/*` - requisicoes, aprovacao, historico |
| Dice | `/api/dice/*` - rolagens V5 e V20 |
| Initiative | `/api/initiative/*` - combate, turnos |
| Chat | `/api/chat/*` - mensagens, historico |
| Scenes | `/api/scenes/*` - criar, ativar |
| Game Data | `/api/game-data/*` - clas, disciplinas, etc |
| WebSocket | `/ws/chronicle/{id}` - tempo real |

## Configuracao Discord OAuth

1. Crie uma aplicacao no [Discord Developer Portal](https://discord.com/developers/applications)
2. Configure o OAuth2 Redirect URI: `http://localhost:8001/api/auth/discord/callback`
3. Copie Client ID e Client Secret para o `.env`

## Deploy

Ver arquivo `DEPLOY.md` para instrucoes de deploy em:
- Vercel (frontend)
- Railway (backend + PostgreSQL)

## Licenca

Este projeto e apenas para uso educacional e faz referencia a Vampire: The Masquerade,
propriedade intelectual da Paradox Interactive AB.
