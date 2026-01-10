# Vampire VTT - Estado Atual do Projeto

**Ultima Atualizacao:** 07/01/2026

---

## Localizacao do Projeto

```
F:\Vampire VTT\vampire-vtt\
├── backend/    (FastAPI + SQLite)
└── frontend/   (React + Vite + TypeScript)
```

---

## Como Iniciar (Desenvolvimento)

### Backend
```bash
cd "F:\Vampire VTT\vampire-vtt\backend"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd "F:\Vampire VTT\vampire-vtt\frontend"
npm run dev
```

### Acessar
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

---

## Funcionalidades Completas

### Autenticacao
- [x] Login com Email/Senha
- [x] Discord OAuth
- [x] Recuperacao de senha (forgot-password, reset-password)
- [x] Toggle mostrar/ocultar senha
- [x] JWT tokens persistentes

### Cronicas
- [x] Criar/gerenciar cronicas (V5 ou V20)
- [x] Codigos de convite
- [x] Entrar/sair de cronicas
- [x] Regenerar codigo de convite

### Personagens
- [x] Fichas completas V5 e V20
- [x] Sistema de aprovacao pelo Narrador
- [x] Mudancas pendentes (pending_sheet)
- [x] Notificacoes de alteracoes
- [x] Historico de modificacoes (SheetChangeLog)

### Sessoes de Jogo
- [x] Iniciar/encerrar sessoes formais
- [x] Rastrear participantes
- [x] XP automatico ao encerrar

### Sistema de XP
- [x] Requisicoes de gasto de XP
- [x] Aprovacao/rejeicao pelo Narrador
- [x] Historico de transacoes (XPLog)
- [x] XP salvo corretamente na ficha

### Rolagem de Dados
- [x] V5: Hunger Dice, Messy Criticals, Bestial Failures
- [x] V5: Rouse, Frenzy, Remorse checks
- [x] V20: Sistema classico, Botch, Especialidades
- [x] Historico de rolagens

### Combate/Iniciativa
- [x] Tracker de Iniciativa
- [x] Gerenciamento de rodadas
- [x] Adicionar/remover combatentes
- [x] Avancar turnos

### Chat
- [x] Mensagens persistentes
- [x] WebSocket tempo real
- [x] Historico paginado

### Cenas
- [x] Criar cenas/locais
- [x] Ativar/desativar
- [x] Contextualizar narrativa

---

## Detalhes Tecnicos Importantes

### SQLite + JSON
- Usar `flag_modified()` para detectar mudancas em campos JSON
- Usar `copy.deepcopy()` antes de modificar sheets
- Fazer `flush()` apos modificacoes

### WebSocket
- URL: `/ws/chronicle/{id}` (NAO `/api/ws/...`)
- Auth via token no header ou query param

### Auth Token
- Persistido no localStorage (`vampire-vtt-auth`)
- Gerenciado pelo Zustand store

---

## Estrutura de Arquivos

### Backend (12 modulos de API)
- `auth.py` - Autenticacao (login, registro, OAuth, reset senha)
- `users.py` - Perfil de usuario
- `chronicles.py` - Cronicas e membros
- `characters.py` - Fichas e aprovacao
- `sessions.py` - Sessoes de jogo
- `xp.py` - Sistema de XP
- `dice.py` - Rolagens V5 e V20
- `initiative.py` - Sistema de combate
- `chat.py` - Chat persistente
- `scenes.py` - Cenas da cronica
- `game_data.py` - Dados estaticos do jogo
- `websocket.py` - Tempo real

### Frontend (10 paginas)
- `LandingPage` - Pagina inicial
- `LoginPage` - Login com email/Discord
- `ResetPasswordPage` - Redefinir senha
- `AuthCallback` - Callback OAuth
- `DashboardPage` - Dashboard do usuario
- `ChroniclesPage` - Lista de cronicas
- `ChroniclePage` - Hub da cronica (6 abas)
- `CharactersPage` - Lista de personagens
- `CharacterSheetPage` - Ficha do personagem
- `DiceRollerPage` - Rolador de dados

---

## Models do Banco (13)

1. User
2. Chronicle
3. ChronicleMember
4. Character
5. Scene
6. GameSession
7. SessionParticipant
8. InitiativeOrder
9. InitiativeEntry
10. DiceRoll
11. ChatMessage
12. XPRequest
13. XPLog / SheetChangeLog

---

## Proximos Passos

1. Testar todas as funcionalidades em ambiente limpo
2. Deploy (ver DEPLOY.md)
3. Testes automatizados

---

## Arquivos de Referencia

- `README.md` - Documentacao geral
- `DEPLOY.md` - Instrucoes de deploy
- `backend/.env.example` - Variaveis de ambiente
