# Pendencias - Fichas V5 (11/01/2026)

## O QUE FOI FEITO

### 1. Correcoes de Traducao
- [x] Compostura → Autocontrole
- [x] Furto → Ladroagem
- [x] Perspicacia → Sagacidade
- [x] Academicos → Erudicao
- [x] Consciencia → Percepcao
- [x] Oficio → Oficios

### 2. Ordem das Habilidades (corrigida conforme livro)

**Fisicas:**
1. Armas Brancas
2. Armas de Fogo
3. Atletismo
4. Briga
5. Conducao
6. Furtividade
7. Ladroagem
8. Oficios
9. Sobrevivencia

**Sociais:**
1. Empatia c/ Animais
2. Etiqueta
3. Intimidacao
4. Lideranca
5. Manha
6. Performance
7. Persuasao
8. Sagacidade
9. Labia

**Mentais:**
1. Ciencia
2. Erudicao
3. Financas
4. Investigacao
5. Medicina
6. Ocultismo
7. Percepcao
8. Politica
9. Tecnologia

### 3. Campo de Especializacao
- [x] Adicionado campo de texto ao lado de cada habilidade
- [x] Permite anotar especializacoes (+1 dado em situacoes especificas)

### 4. Disciplinas Expandidas
- [x] Tooltip ao passar mouse nas bolinhas mostrando poderes de cada nivel
- [x] Mostra: nome, descricao, custo, parada de dados, duracao
- [x] Textarea para anotar poderes escolhidos
- [x] Botao info para ver descricao completa da disciplina

### 5. Secao Lore
- [x] Adicionada no final da ficha (apos Notas)
- [x] Textarea grande para historia do personagem
- [x] Apenas o dono da ficha pode editar

### 6. Traducao das Disciplinas (backend)
- [x] Nomes dos poderes em PT
- [x] Descricoes em PT
- [x] Custos em PT (Gratis, 1 Rouse Check, etc.)
- [x] Pools de dados em PT (Manipulacao + Animalismo, etc.)
- [x] source_book = "Livro Basico"

### 7. Script de Migracao
- [x] Criado em `backend/scripts/migrate_sheet_keys.py`
- [x] Executado localmente (4 fichas migradas)

---

## O QUE FALTA FAZER

### 1. URGENTE - Rodar migracao em PRODUCAO (Railway)

As fichas em producao ainda tem as keys antigas. Precisa rodar o script no Railway:

**Opcao A - Via Railway CLI:**
```bash
railway run python -m scripts.migrate_sheet_keys
```

**Opcao B - Via Railway Dashboard:**
1. Acesse https://railway.app
2. Va no projeto VampireVTT → Backend
3. Abra o terminal/shell
4. Execute: `python -m scripts.migrate_sheet_keys`

**Opcao C - Adicionar ao Procfile (executa no deploy):**
Adicionar linha no Procfile:
```
release: python -m scripts.migrate_sheet_keys
```

### 2. VERIFICAR - Pools de dados aparecendo em ingles

O usuario reportou que mesmo apos traduzir, algumas pools ainda apareciam em ingles (ex: "Manipulation + Animalism").

**Possivel causa:** Cache do navegador ou backend nao reiniciado.

**Solucao:**
1. Limpar cache do navegador (Ctrl+Shift+R)
2. Verificar se o deploy do Railway terminou
3. Testar novamente

Se ainda aparecer em ingles, verificar o arquivo:
`backend/app/game_data/v5/disciplines.py`

Todas as pools devem estar como:
- Determinacao + Animalismo (nao Resolve + Animalism)
- Manipulacao + Animalismo (nao Manipulation + Animalism)
- Carisma + Presenca (nao Charisma + Presence)
- etc.

---

## ARQUIVOS MODIFICADOS

```
backend/
  app/game_data/v5/disciplines.py  # Traducoes completas
  scripts/__init__.py              # Novo
  scripts/migrate_sheet_keys.py    # Script de migracao

frontend/
  src/components/character/CharacterSheetV5.tsx  # Todas as mudancas
  src/pages/CharacterSheetPage.tsx               # Prop isOwner para Lore
```

---

## COMO TESTAR

1. Abrir uma ficha de personagem V5
2. Verificar se as habilidades estao na ordem correta
3. Verificar se tem campo de especializacao ao lado
4. Selecionar uma disciplina e passar mouse nas bolinhas
5. Verificar se o tooltip mostra poderes em PT
6. Rolar ate o final e verificar secao "Lore"

---

## COMMITS

- `11b2698` - Melhorias nas fichas V5: traducoes, especializacoes, disciplinas e lore
