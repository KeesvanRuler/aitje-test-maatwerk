"""Voorbeeld-CRM: een nep-CRM in het geheugen, om maatwerk te testen."""

from typing import Annotated

from aitje_plugin import PluginError, setting, tool

KLANTEN = {
    "K-1001": {"naam": "Bakkerij De Korenschoof", "plaats": "Tiel", "notities": ["Levert op dinsdag."]},
    "K-1002": {"naam": "Lunchroom Het Zonnetje", "plaats": "Culemborg", "notities": []},
}


def _verbonden() -> None:
    if not setting("crm_url") or not setting("crm_token"):
        raise PluginError("Het CRM is nog niet ingesteld. Vraag de beheerder (Beheer → Maatwerk).")


@tool
def klant_zoeken(naam: Annotated[str, "(Deel van) de naam van de klant"]) -> list[dict]:
    """Zoek klanten in het CRM op naam. Geeft klantnummer, naam en plaats."""
    _verbonden()
    gevonden = [
        {"klantnummer": k, "naam": v["naam"], "plaats": v["plaats"]}
        for k, v in KLANTEN.items()
        if naam.casefold() in v["naam"].casefold()
    ]
    return gevonden or [{"melding": f"Geen klant gevonden met '{naam}'."}]


@tool
def notities(klantnummer: str) -> list[str]:
    """De notities bij een klant in het CRM."""
    _verbonden()
    if klantnummer not in KLANTEN:
        raise PluginError(f"Klant {klantnummer} bestaat niet.")
    return KLANTEN[klantnummer]["notities"] or ["Nog geen notities."]


@tool(write=True)
def notitie_toevoegen(klantnummer: str, tekst: Annotated[str, "De notitie"]) -> str:
    """Zet een notitie bij een klant in het CRM. De gebruiker bevestigt dit eerst."""
    _verbonden()
    if klantnummer not in KLANTEN:
        raise PluginError(f"Klant {klantnummer} bestaat niet.")
    KLANTEN[klantnummer]["notities"].append(tekst)
    return f"Notitie toegevoegd bij {KLANTEN[klantnummer]['naam']}."