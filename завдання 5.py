
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realizaciya patronu Strategy dlya systemy eksportu analitychnykh zvitiv.

Predmetna oblasti: eksporsyst zvitiv dlya analitychnoho dashbordu.
Zhadan: eksportuvaty dani u riznykh formatakh (CSV, JSON, XML, Markdown).

ARKHITEKTURA:
- ExportStrategy (ABC) - interface dlia stratehiy eksportu
- CSVExporter, JSONExporter, XMLExporter, MarkdownExporter - konkretni stratehiy
- ReportExporter (kontekst) - klas, shcho pryminyuya stratehiyu

PEREVAHA STRATEGY:
1. Rozshyryvanist: legko dodavaty novi formaty bez zminy ReportExporter
2. Fleksybilnist: zminа stratehiy pid chas vykonannia
3. Testuvanist: kozhna stratehiya mozhe testuvaty se​paratno

OBHRUNTUVANNIA VYBORU:
- Bez Strategy: ReportExporter mav by bahatoto if/elif dlya kozhnoho formatu
- Z Strategy: kozhnyy format - vidokrelyy klas z vlasnoyu logikoyu
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any


# ========== INTERFACE STRATEHIY (ABC) ==========

class ExportStrategy(ABC):
    """
    Abstraktnyy interface dlya stratehiy eksportu.

    Vyznachaye kontrakт: kozhna konkretna stratehiya povynna realizuvaty export().
    """

    @abstractmethod
    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """
        Eksportuyuye dani u vidpovidnomu formati.

        Args:
            data: Spysok slovnykiv z danymy (riadky zvitu)
            title: Zaholovok zvitu

        Returns:
            str: Eksportovanyy vmiст u vidpovidnomu formati
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Povertaye rozshyrennia failу dlya tsyey stratehiy.

        Returns:
            str: Rozshyrennia (napr. 'csv', 'json')
        """
        pass


# ========== KONKRETNI STRATEHIY ==========

class CSVExporter(ExportStrategy):
    """
    Stratehiya eksportu u CSV format.

    Realizuye CSV format z zaholovkami ta vidokrelennyam komi.
    """

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Eksportuyuye dani u CSV formati."""
        if not data:
            return ""

        lines = []

        # Zagolovok yak komentariy
        lines.append("# {}".format(title))
        lines.append("# Vytvoren: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append("")

        # Headers
        headers = list(data[0].keys())
        lines.append(",".join(str(h) for h in headers))

        # Dani
        for row in data:
            values = []
            for header in headers:
                val = row.get(header, "")
                # Ekranuvannia zaropen dlya CSV
                if isinstance(val, str) and ("," in val or '"' in val or "\n" in val):
                    val = '"{}"'.format(val.replace('"', '""'))
                values.append(str(val))
            lines.append(",".join(values))

        return "\n".join(lines)

    def get_file_extension(self) -> str:
        """Rozshyrennia failу: csv."""
        return "csv"


class JSONExporter(ExportStrategy):
    """
    Stratehiya eksportu u JSON format.

    Realizuye JSON format z vidiuuvannyam.
    """

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Eksportuyuye dani u JSON formati."""
        if not data:
            return "{}"

        # Manualʹna realizaciya JSON (bez json.dumps, yak vymahaye zavdannia)
        lines = []
        lines.append("{")
        lines.append('  "title": "{}",'.format(title.replace('"', '\\"')))
        lines.append('  "created": "{}",'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append('  "records": [')

        for i, row in enumerate(data):
            lines.append("    {")
            items = []
            for key, value in row.items():
                if isinstance(value, str):
                    items.append('      "{}": "{}"'.format(key, str(value).replace('"', '\\"')))
                elif isinstance(value, bool):
                    items.append('      "{}": {}'.format(key, "true" if value else "false"))
                elif value is None:
                    items.append('      "{}": null'.format(key))
                else:
                    items.append('      "{}": {}'.format(key, value))
            lines.append(",\n".join(items))
            lines.append("    }" + ("," if i < len(data) - 1 else ""))

        lines.append("  ]")
        lines.append("}")

        return "\n".join(lines)

    def get_file_extension(self) -> str:
        """Rozshyrennia failу: json."""
        return "json"


class XMLExporter(ExportStrategy):
    """
    Stratehiya eksportu u XML format.

    Realizuye XML format z teguvannyam.
    """

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Eksportuyuye dani u XML formati."""
        if not data:
            return "<report></report>"

        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append("<report>")
        lines.append("  <title>{}</title>".format(self._escape_xml(title)))
        lines.append("  <created>{}</created>".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append("  <records>")

        for row in data:
            lines.append("    <record>")
            for key, value in row.items():
                lines.append("      <{}>{}</{}>".format(
                    key,
                    self._escape_xml(str(value)),
                    key
                ))
            lines.append("    </record>")

        lines.append("  </records>")
        lines.append("</report>")

        return "\n".join(lines)

    @staticmethod
    def _escape_xml(text):
        """Ekranuvannia spetsialnykh symvoliv u XML."""
        text = str(text)
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        return text

    def get_file_extension(self) -> str:
        """Rozshyrennia failу: xml."""
        return "xml"


class MarkdownExporter(ExportStrategy):
    """
    Stratehiya eksportu u Markdown format.

    Realizuye Markdown tablycю.
    """

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Eksportuyuye dani u Markdown formati."""
        if not data:
            return "# {}".format(title)

        lines = []
        lines.append("# {}".format(title))
        lines.append("")
        lines.append("_Vytvoren: {}_".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append("")

        # Tablycia
        headers = list(data[0].keys())
        lines.append("| " + " | ".join(str(h) for h in headers) + " |")
        lines.append("|" + "|".join(["-" * 10 for _ in headers]) + "|")

        for row in data:
            values = []
            for header in headers:
                val = row.get(header, "")
                values.append(str(val)[:20])  # Obmezhuyemy dovzhynu
            lines.append("| " + " | ".join(values) + " |")

        return "\n".join(lines)

    def get_file_extension(self) -> str:
        """Rozshyrennia failу: md."""
        return "md"


class YAMLExporter(ExportStrategy):
    """
    NOVA STRATEHIYA: Eksport u YAML format.

    Demonstruye rozshyryvanist: dodana BEZ zminy inshykh klasiv.
    """

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Eksportuyuye dani u YAML formati."""
        if not data:
            return ""

        lines = []
        lines.append("title: {}".format(title))
        lines.append("created: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append("records:")

        for row in data:
            lines.append("  - ")
            for key, value in row.items():
                if isinstance(value, str) and " " in value:
                    lines.append('    {}: "{}"'.format(key, value))
                else:
                    lines.append("    {}: {}".format(key, value))

        return "\n".join(lines)

    def get_file_extension(self) -> str:
        """Rozshyrennia failу: yaml."""
        return "yaml"


# ========== KONTEKST: VYKORYSTOVUYE STRATEHIY ==========

class ReportExporter:
    """
    Kontekst: vyukoristovuye stratehiju eksportu.

    ReportExporter NE zna pro konkretn realizaciyu stratehiy.
    Vin prosto vyukoristovuye interface ExportStrategy.

    TSE YE KLYUCHEVA PEREVAGA STRATEGY:
    - Dodayemo novu stratehiju = dodayemo novoу klas
    - ReportExporter ne zmin​yuetsya
    - Kliyent mozhe vybyraty stratehiju dynamichno
    """

    def __init__(self, strategy: ExportStrategy = None):
        """
        Inicializaciya eksportera.

        Args:
            strategy: Pochatko​va stratehiya (opcionalno)
        """
        self._strategy = strategy
        self._data: List[Dict[str, Any]] = []
        self._title = ""

    def set_strategy(self, strategy: ExportStrategy):
        """
        Vstanovlyuye novu stratehiju eksprtu.

        Demostruye FLEKSYBILNIST: mozhlivo minyaty stratehiju pid chas vykonannia.

        Args:
            strategy: Nova stratehiya
        """
        if not isinstance(strategy, ExportStrategy):
            raise TypeError("Strategy povynna realizuvaty ExportStrategy")
        self._strategy = strategy

    def add_record(self, record: Dict[str, Any]):
        """
        Dodaye riadok do zvitu.

        Args:
            record: Slovnyk z danymy
        """
        self._data.append(record)

    def set_title(self, title: str):
        """Vstanovlyuye zaholovok zvitu."""
        self._title = title

    def export(self) -> str:
        """
        Eksportuyuye zvit vykorystovuyuchy vstavlenu.stratehiju.

        Delehuvannia: vyukoristovuye metod stratehiy bez znaniuu detaley realizacii.

        Returns:
            str: Eksportovanyy zvit
        """
        if not self._strategy:
            raise ValueError("Stratehiya ne vstanovlena. Vyukoristajte set_strategy().")

        if not self._data:
            return "# Zvit pustayu: {}".format(self._title)

        return self._strategy.export(self._data, self._title)

    def get_filename(self, base_name: str) -> str:
        """
        Povertaye imya failyu z vidpovidnym rozshyvenniam dlya vybranoiy stratehiy.

        Args:
            base_name: Bazove imya failyu

        Returns:
            str: Imya failyu z rozshyrennyam
        """
        if not self._strategy:
            return "{}.txt".format(base_name)
        return "{}.{}".format(base_name, self._strategy.get_file_extension())


# ========== DEMONSTRUVANNIA ==========

def demonstrate_strategy_pattern():
    """Demonstruvannia Strategy patronu."""
    print("="*80)
    print("PATERN STRATEGY: SISTEMA EKSPOR​TU ANALITYCHNYKH ZVITIV")
    print("="*80)

    # Prykladi danych
    sample_data = [
        {"ID": 1, "Product": "Laptop", "Sales": 1500, "Region": "North"},
        {"ID": 2, "Product": "Mouse", "Sales": 85, "Region": "South"},
        {"ID": 3, "Product": "Keyboard", "Sales": 120, "Region": "East"},
        {"ID": 4, "Product": "Monitor", "Sales": 300, "Region": "West"},
    ]

    # Stvorennia kontekstu
    exporter = ReportExporter()
    exporter.set_title("Analiz Prodazhu - Q4 2024")

    for record in sample_data:
        exporter.add_record(record)

    # 1. EKSPORT U CSV
    print("\n[1] EKSPORT U CSV")
    print("-"*80)
    exporter.set_strategy(CSVExporter())
    csv_output = exporter.export()
    print(csv_output)
    print("\nFailu: {}".format(exporter.get_filename("zvit_q4")))

    # 2. EKSPORT U JSON
    print("\n[2] EKSPORT U JSON")
    print("-"*80)
    exporter.set_strategy(JSONExporter())
    json_output = exporter.export()
    print(json_output)
    print("\nFailu: {}".format(exporter.get_filename("zvit_q4")))

    # 3. EKSPORT U XML
    print("\n[3] EKSPORT U XML")
    print("-"*80)
    exporter.set_strategy(XMLExporter())
    xml_output = exporter.export()
    print(xml_output)
    print("\nFailu: {}".format(exporter.get_filename("zvit_q4")))

    # 4. EKSPORT U MARKDOWN
    print("\n[4] EKSPORT U MARKDOWN")
    print("-"*80)
    exporter.set_strategy(MarkdownExporter())
    md_output = exporter.export()
    print(md_output)
    print("\nFailu: {}".format(exporter.get_filename("zvit_q4")))


def demonstrate_extensibility():
    """Demonstruvannia ROZSHYRYVANISTI: nova stratehiya bez zminy kodu."""
    print("\n\n" + "="*80)
    print("ROZSHYRYVANIST: NOVA STRATEHIYA (YAML) BEZ ZMINY ReportExporter")
    print("="*80)

    sample_data = [
        {"Department": "Sales", "Budget": 50000, "Spent": 45000},
        {"Department": "Marketing", "Budget": 30000, "Spent": 28000},
        {"Department": "Dev", "Budget": 100000, "Spent": 99500},
    ]

    exporter = ReportExporter()
    exporter.set_title("Byudzhetnyy Zvit")

    for record in sample_data:
        exporter.add_record(record)

    # NOVA STRATEHIYA - dodana bez zminy ReportExporter
    print("\n[NOVA] EKSPORT U YAML (nova stratehiya bez zminy klasiv)")
    print("-"*80)
    exporter.set_strategy(YAMLExporter())
    yaml_output = exporter.export()
    print(yaml_output)
    print("\nFailu: {}".format(exporter.get_filename("budget_report")))

    print("\n[OK] Nova stratehiya dod​ana BEZUSPECISHNO!")
    print("     - ReportExporter ne zminyvsya")
    print("     - YAMLExporter - novyy klas, realizuye ExportStrategy")
    print("     - Kliyentskyykoд ne zmin​yuetsya")


def demonstrate_dynamic_strategy_selection():
    """Demonstruvannia DYNAMICHNOHO VYBORU STRATEHIY."""
    print("\n\n" + "="*80)
    print("DYNAMICHNYY VYBIR STRATEHIY (RUNTIME)")
    print("="*80)

    sample_data = [
        {"User": "alice@example.com", "LoginCount": 42, "LastActive": "2024-01-15"},
        {"User": "bob@example.com", "LoginCount": 38, "LastActive": "2024-01-14"},
        {"User": "charlie@example.com", "LoginCount": 55, "LastActive": "2024-01-16"},
    ]

    exporter = ReportExporter()
    exporter.set_title("Zvit Aktyvnosti Korystuvachiv")

    for record in sample_data:
        exporter.add_record(record)

    # Menu vyboru formatu (v realnomy zastosuvanniu - vvid koystyvalnya abo konfig)
    strategies = {
        "csv": CSVExporter(),
        "json": JSONExporter(),
        "xml": XMLExporter(),
        "markdown": MarkdownExporter(),
        "yaml": YAMLExporter(),
    }

    print("\nDostupni formaty eksportu:")
    for fmt in strategies.keys():
        print("  - {}".format(fmt))

    print("\nDynamichne vyboruvaty form​aty:")
    for fmt, strategy in strategies.items():
        exporter.set_strategy(strategy)
        output = exporter.export()
        print("\n[{}] Pershyy riadok: {}".format(fmt.upper(), output.split("\n")[0]))


def demonstrate_comparison_without_pattern():
    """Demonstruvannia: YAKY BUV KOD BEZ STRATEGY."""
    print("\n\n" + "="*80)
    print("PORIVNIANNIA: KOD BEZ STRATEGY (ANTYPATON)")
    print("="*80)

    print("""
BEZ STRATEGY (ANTYPATON - Golden Hammer):

    class ReportExporter:
        def export_to_csv(self, data, title):
            # CSV logika...
            pass

        def export_to_json(self, data, title):
            # JSON logika...
            pass

        def export_to_xml(self, data, title):
            # XML logika...
            pass

        def export_to_markdown(self, data, title):
            # Markdown logika...
            pass

        def export(self, format, data, title):
            if format == "csv":
                return self.export_to_csv(data, title)
            elif format == "json":
                return self.export_to_json(data, title)
            elif format == "xml":
                return self.export_to_xml(data, title)
            elif format == "markdown":
                return self.export_to_markdown(data, title)
            else:
                raise ValueError("Unknown format")

PROBLEMY CIOHO PIDKHODU:
1. ReportExporter roset z kozhnym novym formatom
2. Logika eksportu pomeshan z logikoyu vyboru
3. Novyy format = zmina ReportExporter (VIOLATION of Open/Closed Principle)
4. Testuvannia skladne: ne mozhlivo testuvatty formaty odnokreslno

Z STRATEGY:
1. Kozhne format - vidokrelyy klas (Single Responsibility)
2. ReportExporter - tilky orhanizaciya (kontekst)
3. Novyy format = novoyu klas (Open/Closed Principle OK!)
4. Testuvannia legke: kozhny klasy monozhe testuvatty se​paratno
""")


def demonstrate_alternative_approaches():
    """Demonstruvannia ALTERNATIVNYKH PIDKHODIV."""
    print("\n\n" + "="*80)
    print("ALTERNATYVNI PIDKHODY DO STRATEGY")
    print("="*80)

    print("""
1. FUNKCIYI PERSHOGO KLASU (Pythonichniy pikhid):

   export_functions = {
       'csv': export_to_csv,
       'json': export_to_json,
       'xml': export_to_xml
   }

   def export(format, data, title):
       return export_functions[format](data, title)

   Perevaha: prostishe, bez klasiv
   Nedostatok: vazhche vidstezhuvatty stan, menshе struktura

2. STRATEHIYA YAK LAMBDA/FUNKCIYA (Python-style):

   exporter.strategy = lambda data, title: "...".join([...for ... in data])

   Perevaha: fluidy, korotko
   Nedostatok: menshе chitayemy, vazhche debuguvatlty

3. BUDUVALNYK (Builder) - alternatyva:

   export_builder = ExportBuilder() \\
       .add_title("Zvit") \\
       .add_data(data) \\
       .set_format("csv") \\
       .build()

   Perevaha: fluent API, pokrokove budyvannia
   Nedostatok: skladnishe dlia prostykh vypadkiv

4. ZAVANTAZHUVACH MODULYV (Dynamic modules):

   module = __import__('exporters.csv_exporter')
   exporter = module.CSVExporter()

   Perevaha: absolutna rozshyryvanist, zavisymisty zovsim slabi
   Nedostatok: nebezpechno, vazhche vidstezhuvatty, potribna konfihuraciya
""")


def demonstrate_when_strategy_becomes_antipattern():
    """Demonstruvannia: KOLY STRATEGY STAYE ANTYPAT​ERONOM."""
    print("\n\n" + "="*80)
    print("ANTYPATON: KOLY STRATEGY STAYE NADLISHKOVYM (Golden Hammer)")
    print("="*80)

    print("""
STRATEGY POSTAYE NADLISHKOVYM V TSYAH VYPADKAKH:

1. MALO VARIANT (1-2):

   Prykladi:
   - Yedyny formart eksportu (CSV)
   - 2 pohrovaryenty (PDF ta PNG)

   Rishennia:
   - Prostiy if/elif v metodach
   - Funkciyi pershogo klasu
   - Yeshche ne stukturuvaltyty kod

   Problem: Strategy vvodyty overhead klassiv bez koristy

2. STRATEHIY DUZHE PROSTI (trivialʹni):

   Prykladi:
   - Zmina rozmiru shryft​u (10pt, 12pt, 14pt)
   - Vibir kolyoru (red, blue, green)

   Rishennia:
   - Enum abo Dictionary z parametramy
   - Lambda-funkcii
   - Direct parameter passing

   Problem: Klasificirky bezprika​rno dlya trivialʹnyh operaciy

3. STRATEHIY MAYUT BAGATO SPILNOY LOGIKY:

   Prykladi:
   - Eksport u CSV i TSV (azonachi, tilky vidilʹnyk vidminnyyetʹsya)
   - Eksport u JSON i JSONL (azaonachi, tilky formatuvannia)

   Rishennia:
   - Pavyternist klasiv
   - Spilna bazova klasa z konfiguraciyeyu
   - Template Method pattern

   Problem: Kopiyuvannia kodu mizh stratehiyamy

4. YEK STRATEHIYA DOMINUYE:

   Prykladi:
   - 90% vypadkiv: normal eksport
   - 10% vypadkiv: spetsialʹnyy eksport

   Rishensia:
   - Normal eksport v bazovomu kodi
   - Special handlers tilky dlya vynyatkiv

   Problem: Zayva abstrakaya dlya malozoho vikorystyvannia

VYSNOVY:
- Strategy ORANTE dlia 3+ rozmayk stratehiy
- Strategy ORANTE koly stratehiy mayut skladnu logiku
- Strategy ORANTE koly stratehiy chasto rozshyryayutsya
- Bez Strategy: 1-2 trivialʹni variyanty, shcho ridko zminyayutsya
""")


def main():
    """Osnovna demonstruvalna funkciya."""
    print("\n")
    demonstrate_strategy_pattern()
    demonstrate_extensibility()
    demonstrate_dynamic_strategy_selection()
    demonstrate_comparison_without_pattern()
    demonstrate_alternative_approaches()
    demonstrate_when_strategy_becomes_antipattern()

    print("\n" + "="*80)
    print("DEMONSTRUVANNIA ZAVERSHENA")
    print("="*80)


if __name__ == "__main__":
    main()
