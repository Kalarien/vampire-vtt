"""
Script de migracao para atualizar keys das fichas de personagem.

Renomeia as keys antigas para as novas traduzidas:
- atributos.sociais.compostura -> autocontrole
- habilidades.furto -> ladroagem
- habilidades.perspicacia -> sagacidade
- habilidades.academicos -> erudicao
- habilidades.consciencia -> percepcao
- habilidades.oficio -> oficios

Executar com: python -m scripts.migrate_sheet_keys
"""

import asyncio
import json
import sys
import os

# Adiciona o diretorio pai ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.character import Character


# Mapeamento de keys antigas para novas
KEY_MIGRATIONS = {
    # Atributos
    "atributos.sociais.compostura": "atributos.sociais.autocontrole",

    # Habilidades
    "habilidades.furto": "habilidades.ladroagem",
    "habilidades.perspicacia": "habilidades.sagacidade",
    "habilidades.academicos": "habilidades.erudicao",
    "habilidades.consciencia": "habilidades.percepcao",
    "habilidades.oficio": "habilidades.oficios",
}


def migrate_sheet(sheet: dict) -> tuple[dict, list[str]]:
    """
    Migra uma sheet, renomeando keys antigas para novas.
    Retorna a sheet atualizada e lista de mudancas feitas.
    """
    if not sheet:
        return sheet, []

    changes = []

    # Atributos sociais: compostura -> autocontrole
    if "atributos" in sheet and "sociais" in sheet["atributos"]:
        sociais = sheet["atributos"]["sociais"]
        if "compostura" in sociais and "autocontrole" not in sociais:
            sociais["autocontrole"] = sociais.pop("compostura")
            changes.append("compostura -> autocontrole")

    # Habilidades
    if "habilidades" in sheet:
        habs = sheet["habilidades"]

        # furto -> ladroagem
        if "furto" in habs and "ladroagem" not in habs:
            habs["ladroagem"] = habs.pop("furto")
            changes.append("furto -> ladroagem")

        # perspicacia -> sagacidade
        if "perspicacia" in habs and "sagacidade" not in habs:
            habs["sagacidade"] = habs.pop("perspicacia")
            changes.append("perspicacia -> sagacidade")

        # academicos -> erudicao
        if "academicos" in habs and "erudicao" not in habs:
            habs["erudicao"] = habs.pop("academicos")
            changes.append("academicos -> erudicao")

        # consciencia -> percepcao
        if "consciencia" in habs and "percepcao" not in habs:
            habs["percepcao"] = habs.pop("consciencia")
            changes.append("consciencia -> percepcao")

        # oficio -> oficios
        if "oficio" in habs and "oficios" not in habs:
            habs["oficios"] = habs.pop("oficio")
            changes.append("oficio -> oficios")

    return sheet, changes


async def run_migration():
    """Executa a migracao em todos os personagens."""

    print("=" * 60)
    print("MIGRACAO DE KEYS DAS FICHAS DE PERSONAGEM")
    print("=" * 60)

    # Criar engine e session
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Buscar todos os personagens
        result = await session.execute(select(Character))
        characters = result.scalars().all()

        print(f"\nEncontrados {len(characters)} personagens para verificar.\n")

        migrated_count = 0
        skipped_count = 0

        for char in characters:
            print(f"Verificando: {char.name} (ID: {char.id})")

            if not char.sheet:
                print(f"  -> Sem sheet, pulando.")
                skipped_count += 1
                continue

            # Migrar a sheet
            new_sheet, changes = migrate_sheet(char.sheet)

            if changes:
                char.sheet = new_sheet
                print(f"  -> Migrado: {', '.join(changes)}")
                migrated_count += 1
            else:
                print(f"  -> Nenhuma mudanca necessaria.")
                skipped_count += 1

        # Commit das mudancas
        if migrated_count > 0:
            await session.commit()
            print(f"\n{'=' * 60}")
            print(f"MIGRACAO CONCLUIDA!")
            print(f"  - Personagens migrados: {migrated_count}")
            print(f"  - Personagens sem mudancas: {skipped_count}")
            print(f"{'=' * 60}")
        else:
            print(f"\nNenhuma migracao necessaria. Todas as fichas ja estao atualizadas.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_migration())
