import os

try:
    from weasyprint import HTML
except OSError as e:
    raise RuntimeError(
        "WeasyPrint native dependencies are missing. "
        "On Windows you must install GTK/Cairo/Pango/GObject support. "
        "See https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
    ) from e

# Create HTML content for the PDF with nice formatting
html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {
        size: A4;
        margin: 20mm 15mm;
        background-color: #fcfbfa;
        @bottom-right {
            content: counter(page);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 9pt;
            color: #7f8c8d;
        }
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2c3e50;
        line-height: 1.5;
        margin: 0;
        padding: 0;
        font-size: 10.5pt;
    }
    *, *::before, *::after {
        box-sizing: border-box;
    }
    .header-banner {
        background-color: #2c3e50;
        color: #ffffff;
        padding: 25px 20px;
        margin-bottom: 25px;
        border-radius: 4px;
        text-align: center;
    }
    h1 {
        margin: 0;
        font-size: 20pt;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .subtitle {
        margin: 5px 0 0 0;
        font-size: 12pt;
        color: #bdc3c7;
        font-weight: 300;
    }
    h2 {
        color: #2980b9;
        font-size: 14pt;
        border-left: 4px solid #2980b9;
        padding-left: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
        page-break-after: avoid;
    }
    h3 {
        color: #34495e;
        font-size: 11.5pt;
        margin-top: 15px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    ul {
        margin: 0 0 15px 0;
        padding-left: 20px;
    }
    li {
        margin-bottom: 6px;
    }
    .bold-lead {
        font-weight: bold;
        color: #1a252f;
    }
    .work-title {
        font-style: italic;
        color: #c0392b;
        font-weight: bold;
    }
    .section-block {
        margin-bottom: 30px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        page-break-inside: avoid;
    }
    th, td {
        padding: 10px 12px;
        text-align: left;
        font-size: 10pt;
        border: 1px solid #dcdde1;
    }
    th {
        background-color: #2980b9;
        color: #ffffff;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f2f4f4;
    }
</style>
</head>
<body>

<div class="header-banner">
    <h1>Příprava na test z literatury</h1>
    <div class="subtitle">Klasicismus, Osvícenství a Preromantismus</div>
</div>

<div class="section-block">
    <h2>1. Klasicismus (2. polovina 17. století – 18. století)</h2>
    
    <h3>Základní charakteristika:</h3>
    <ul>
        <li>Vznikl ve Francii za vlády Ludvíka XIV. (Král Slunce).</li>
        <li>Směr přísného <span class="bold-lead">řádu, rozumu a pravidel</span>; umění muselo být dokonalé a jasné.</li>
        <li><span class="bold-lead">Rozum je nadřazen citu</span> (povinnost vůči státu/rodině je víc než osobní touhy).</li>
        <li>Inspirace <span class="bold-lead">antikou</span> (hledání ideálu krásy v řeckém a římském umění).</li>
    </ul>

    <h3>Rozdělení žánrů (přísný zákaz míchání):</h3>
    <ul>
        <li><span class="bold-lead">Vysoké:</span> tragédie, ódy – témata o králích a rekovských činech, vznešený jazyk.</li>
        <li><span class="bold-lead">Nízké:</span> komedie, bajky – témata o měšťanech, lidovější jazyk.</li>
    </ul>

    <h3>Zásada tří jednot (v divadle):</h3>
    <ul>
        <li><span class="bold-lead">Jednota času:</span> děj se musí odehrát do 24 hodin.</li>
        <li><span class="bold-lead">Jednota místa:</span> vše se odehrává v jednom prostředí (např. v jednom domě).</li>
        <li><span class="bold-lead">Jednota děje:</span> pouze jedna hlavní dějová linie, žádné odbočky.</li>
    </ul>

    <h3>Klíčoví autoři a díla:</h3>
    <ul>
        <li><span class="bold-lead">Molière</span> (Jean-Baptiste Poquelin) – mistr komedií, kritizoval lidské nešvary, pokrytectví a církev.
            <ul>
                <li><span class="work-title">Lakomec:</span> Hlavní postava Harpagon je chorobně lakomý měšťan. Miluje peníze (ukryté v kazetě na zahradě) víc než své děti (Cleanta a Elišku). Chce jim domluvit sňatky s bohatými starci. Kazeta se ztratí, což způsobí chaos. Nakonec děti prosadí svou lásku, ale Harpagon zůstává sám se svými penězi.</li>
                <li><span class="work-title">Tartuffe:</span> Hra o náboženském pokrytci, který se vetře do rodiny bohatého Orgona a pokusí se ho zničit a okrást.</li>
            </ul>
        </li>
        <li><span class="bold-lead">Jean de La Fontaine</span> – autor slavných <span class="work-title">Bajek</span> (zvířata mají lidské vlastnosti, na konci je jasné morální ponaučení).</li>
    </ul>
</div>

<div class="section-block">
    <h2>2. Osvícenství (18. století)</h2>
    
    <h3>Základní charakteristika:</h3>
    <ul>
        <li><span class="bold-lead">Filozofické a myšlenkové hnutí</span> (ne čistě umělecký směr).</li>
        <li>Boj proti církevnímu dogmatismu, tmářství a absolutismu panovníků.</li>
        <li>Kult <span class="bold-lead">rozumu, vědy, logiky</span> a pokroku (věda vysvětluje svět lépe než náboženství).</li>
        <li>Důraz na <span class="bold-lead">vzdělání</span> a humanismus.</li>
        <li>Koncept „osvícenského panovníka“ (vládne reformami ve prospěch lidu – např. Josef II.).</li>
    </ul>

    <h3>Klíčoví autoři a díla:</h3>
    <ul>
        <li><span class="bold-lead">Denis Diderot</span> – hlavní organizátor a redaktor <span class="work-title">Encyklopedie</span> (Racionální slovník věd, umění a řemesel). Cíl: shrnout a zpřístupnit lidem veškeré lidské vědění (odpor církve a panovníků).</li>
        <li><span class="bold-lead">Voltaire</span> (François-Marie Arouet) – filozof, dramatik, mistr ironie a satiry.
            <ul>
                <li><span class="work-title">Candide neboli Optimismus:</span> Filosofická povídka parodující názor, že žijeme v nejlepším možném světě. Candide putuje světem, zažívá katastrofy a zjišťuje, že svět má k dokonalosti daleko. Závěr: „Musíme obdělávat svou zahradu“ (soustředit se na smysluplnou práci).</li>
            </ul>
        </li>
        <li><span class="bold-lead">Daniel Defoe</span> – anglický spisovatel.
            <ul>
                <li><span class="work-title">Robinson Crusoe:</span> Robinson je typický osvícenský hrdina. Díky rozumu, praktičnosti, pracovitosti a vědě dokáže přežít na pustém ostrově a civilizovat ho.</li>
            </ul>
        </li>
        <li><span class="bold-lead">Jonathan Swift</span> – anglický satirik.
            <ul>
                <li><span class="work-title">Gulliverovy cesty:</span> Ostrá satira na anglickou společnost vyprávěná skrz Gulliverovy fiktivní cesty do zemí liliputů či obrů.</li>
            </ul>
        </li>
    </ul>
</div>

<div class="section-block">
    <h2>3. Preromantismus / Sentimentalismus (2. polovina 18. století)</h2>
    
    <h3>Základní charakteristika:</h3>
    <ul>
        <li>Reakce na chladný rozum osvícenství a svazující pravidla klasicismu.</li>
        <li>Do popředí staví <span class="bold-lead">cit, vášeň, intuici a individualitu</span>.</li>
        <li><span class="bold-lead">Útěk do čisté přírody</span> (civilizace je zkažená) a k minulosti (staré mýty, lidová slovesnost).</li>
        <li>Estetika tajuplna, nočního ticha, hřbitovů a zřícenin.</li>
        <li><span class="bold-lead">Preromantický hrdina:</span> Osamělý, nepochopený, melancholický snílek. Často končí tragicky (sebevraždou/šílenstvím) kvůli nenaplněné lásce či střetu se společností.</li>
    </ul>

    <h3>Hnutí Sturm und Drang (Bouře a vzdor) v Německu:</h3>
    <ul>
        <li>Mladí němečtí autoři bojující proti autoritám, konvencím a prosazující svobodu tvorby a génia osobnosti.</li>
    </ul>

    <h3>Klíčoví autoři a díla:</h3>
    <ul>
        <li><span class="bold-lead">Johann Wolfgang Goethe</span> – největší osobnost německé literatury.
            <ul>
                <li><span class="work-title">Utrpení mladého Werthera:</span> Román v dopisech. Citlivý umělec Werther se na venkově vášnivě zamiluje do Lotty. Ta ho má ráda, ale z povinnosti si vezme racionálního Alberta. Werther neustojí realitu, propadá depresím a zastřelí se Albertovou pistolí. (Kniha vyvolala „wertherovskou horečku“ – módu modrých fraků/žlutých vest a vlnu sebevražd).</li>
                <li><span class="work-title">Faust:</span> Veršované drama. Učenec Faust upíše duši ďáblovi (Mefistofelovi) za poznání, mládí a rozkoš.</li>
            </ul>
        </li>
        <li><span class="bold-lead">Friedrich Schiller</span> – básník a dramatik, Goethův přítel.
            <ul>
                <li><span class="work-title">Loupežníci:</span> Drama o bratrech Karlovi a Franzovi. Franz intrikami připraví Karla o otce i snoubenku. Karel se stává vůdcem loupežníků, aby trestal nespravedlnost. Zjišťuje však, že násilím morální řád napravit nelze.</li>
            </ul>
        </li>
    </ul>
</div>

<h2>Srovnávací tabulka (Pro bleskovou orientaci)</h2>
<table>
    <thead>
        <tr>
            <th>Směr</th>
            <th>Hlavní pilíř</th>
            <th>Typický hrdina</th>
            <th>Hlavní jména</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="bold-lead">Klasicismus</span></td>
            <td>Řád, pravidla, antika, povinnost</td>
            <td>Typizovaná postava (Lakomec)</td>
            <td>Molière</td>
        </tr>
        <tr>
            <td><span class="bold-lead">Osvícenství</span></td>
            <td>Rozum, věda, pokrok, logika</td>
            <td>Praktický člověk / vědec</td>
            <td>Voltaire, Diderot, Defoe</td>
        </tr>
        <tr>
            <td><span class="bold-lead">Preromantismus</span></td>
            <td>Cit, srdce, příroda, individualita</td>
            <td>Melancholický, nepochopený snílek</td>
            <td>Goethe, Schiller</td>
        </tr>
    </tbody>
</table>

</body>
</html>
"""

# Write HTML to a temporary file
with open("priprava.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Convert HTML to PDF using WeasyPrint
HTML("priprava.html").write_pdf("priprava_na_test_literatura.pdf")
print("PDF created successfully")
