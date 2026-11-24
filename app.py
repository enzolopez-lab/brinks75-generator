
from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BRINKS 75 - Générateur RP</title>
<style>
body {background:#101a35;color:white;font-family:Arial;
padding:25px;max-width:650px;margin:auto}
h1 {color:#75aaff;text-align:center}
input {width:95%;padding:12px;margin:8px 0;
border-radius:8px;border:0}
button {background:#2459b5;color:white;padding:14px;
border:0;border-radius:8px;width:100%;font-weight:bold;
margin-top:15px;cursor:pointer}
small {color:#aabbdc}
</style>
</head>
<body>
<h1>BRINKS 75</h1>
<h2>Générateur de carte RP</h2>
<p><small>Création de carte fictive pour jeu de rôle.</small></p>
<form action="/generer" method="post">
<input name="prenom" placeholder="Prénom" required>
<input name="nom" placeholder="Nom" required>
<input name="fonction" placeholder="Fonction" required>
<input name="service" placeholder="Service" required>
<input name="validite" placeholder="Validité" required>
<input name="signature" placeholder="Signature" required>
<input name="texte_bas" placeholder="Texte sous la signature" required>
<button type="submit">GÉNÉRER MA CARTE</button>
</form>
</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(PAGE)

@app.route("/generer", methods=["POST"])
def generer():
    data = request.form

    img = Image.new("RGB", (1500, 950), "#eaf1ff")
    draw = ImageDraw.Draw(img)

    navy = "#08265d"
    blue = "#174b9c"

    draw.rounded_rectangle(
        (10, 10, 1490, 940), radius=55,
        fill="#eaf1ff", outline=navy, width=15
    )

    draw.rounded_rectangle(
        (25, 25, 1475, 115), radius=30, fill=navy
    )

    try:
        font_big = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
        )
        font_medium = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25
        )
    except OSError:
        font_big = ImageFont.load_default()
        font_medium = font_big
        font_small = font_big

    draw.text((750, 70), "CARTE FICTIVE - ROLEPLAY",
              fill="white", font=font_medium, anchor="mm")

    draw.text((70, 155), "BRINKS 75", fill=navy, font=font_big)
    draw.text((75, 220), "CARTE DE PERSONNAGE",
              fill=blue, font=font_medium)

    fields = [
        ("NOM", data["nom"]),
        ("PRÉNOM", data["prenom"]),
        ("FONCTION", data["fonction"]),
        ("SERVICE", data["service"]),
        ("VALIDITÉ", data["validite"]),
        ("SIGNATURE", data["signature"]),
        ("TEXTE", data["texte_bas"])
    ]

    y = 310
    for label, value in fields:
        draw.text((80, y), label + " :", fill=navy, font=font_medium)
        draw.text((380, y), value[:55], fill="#111111",
                  font=font_medium)
        draw.line((80, y + 65, 1400, y + 65),
                  fill="#9aafd5", width=3)
        y += 85

    draw.text((750, 875), "DOCUMENT FICTIF - SANS VALEUR OFFICIELLE",
              fill="#b00020", font=font_medium, anchor="mm")

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    return send_file(
        output,
        mimetype="image/png",
        as_attachment=True,
        download_name="carte_brinks_rp.png"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
