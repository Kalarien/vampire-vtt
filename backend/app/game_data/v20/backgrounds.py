from typing import Dict, List


BACKGROUNDS_V20: Dict[str, Dict] = {
    "allies": {
        "name": "Allies",
        "description": "Mortais que ajudam voluntariamente o vampiro.",
        "levels": {
            1: "Um aliado de poder ou influência modesta",
            2: "Dois aliados ou um mais poderoso",
            3: "Três aliados ou combinação",
            4: "Quatro aliados ou acesso a pequena organização",
            5: "Cinco aliados ou acesso a grande organização"
        }
    },
    "alternate_identity": {
        "name": "Alternate Identity",
        "description": "Identidade falsa com documentação.",
        "levels": {
            1: "Identidade menor com pouca documentação",
            2: "Identidade estabelecida localmente",
            3: "Identidade com histórico de crédito e referências",
            4: "Identidade profunda, resiste investigação moderada",
            5: "Identidade impecável, resiste investigação intensa"
        }
    },
    "contacts": {
        "name": "Contacts",
        "description": "Rede de informantes e fontes.",
        "levels": {
            1: "Um contato em uma área",
            2: "Contatos em duas áreas ou especializado",
            3: "Pequena rede de contatos",
            4: "Rede extensa de contatos",
            5: "Rede vasta, informação sobre quase tudo"
        }
    },
    "domain": {
        "name": "Domain",
        "description": "Território de caça controlado.",
        "levels": {
            1: "Pequeno edifício ou quarteirão",
            2: "Igreja, boate ou bloco de apartamentos",
            3: "Parque industrial ou pequeno bairro",
            4: "Bairro inteiro",
            5: "Grande área da cidade"
        }
    },
    "fame": {
        "name": "Fame",
        "description": "Reconhecimento público.",
        "levels": {
            1: "Conhecido localmente",
            2: "Conhecido na região",
            3: "Celebridade menor nacional",
            4: "Celebridade nacional",
            5: "Estrela internacional"
        }
    },
    "generation": {
        "name": "Generation",
        "description": "Proximidade com Caim.",
        "levels": {
            1: "12ª Geração",
            2: "11ª Geração",
            3: "10ª Geração",
            4: "9ª Geração",
            5: "8ª Geração"
        }
    },
    "herd": {
        "name": "Herd",
        "description": "Fontes regulares de sangue.",
        "levels": {
            1: "3 vasos",
            2: "7 vasos",
            3: "15 vasos",
            4: "30 vasos",
            5: "60+ vasos"
        }
    },
    "influence": {
        "name": "Influence",
        "description": "Poder político e social.",
        "levels": {
            1: "Moderadamente influente em uma esfera",
            2: "Bem posicionado em uma esfera",
            3: "Influência significativa em uma esfera",
            4: "Grande poder em uma esfera",
            5: "Dominante em uma esfera"
        }
    },
    "mentor": {
        "name": "Mentor",
        "description": "Vampiro mais velho que guia e ajuda.",
        "levels": {
            1: "Mentor com influência limitada",
            2: "Mentor ancilla respeitado",
            3: "Mentor ancilla poderoso",
            4: "Mentor Elder",
            5: "Mentor Elder muito poderoso"
        }
    },
    "resources": {
        "name": "Resources",
        "description": "Riqueza material.",
        "levels": {
            1: "Classe média baixa ($1.000 líquido)",
            2: "Classe média ($8.000 líquido)",
            3: "Classe alta ($50.000 líquido)",
            4: "Rico ($500.000 líquido)",
            5: "Milionário ($5.000.000+ líquido)"
        }
    },
    "retainers": {
        "name": "Retainers",
        "description": "Servos leais, geralmente carniçais.",
        "levels": {
            1: "Um retainer",
            2: "Dois retainers",
            3: "Três retainers",
            4: "Quatro retainers",
            5: "Cinco retainers"
        }
    },
    "status": {
        "name": "Status",
        "description": "Posição na sociedade Kindred.",
        "levels": {
            1: "Conhecido",
            2: "Respeitado",
            3: "Influente",
            4: "Poderoso",
            5: "Luminary"
        }
    },
}


def get_background_v20(background_id: str) -> Dict:
    """Get V20 background by ID"""
    return BACKGROUNDS_V20.get(background_id.lower().replace(" ", "_"), {})


def list_all_backgrounds_v20() -> List[str]:
    """List all V20 background names"""
    return list(BACKGROUNDS_V20.keys())
