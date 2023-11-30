from flask import Flask, render_template, request
import json

# Lade die Konfigurationsdatei
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
# Erstelle die Struktur für Blockchains
blockchains = {key: {'name': key} for key in config['blockchains']}

# Erstelle die Struktur für Versionen
versions = {key: {'name': key} for blockchain in config['blockchains'] for key in config['blockchains'][blockchain]}

# Erstelle die Struktur für tatsächliche Assets
assets = {key: {'name': key} for blockchain in config['blockchains'] for version in config['blockchains'][blockchain] for key in config['blockchains'][blockchain][version]}

def calculate_liquidation_price(blockchain, version, asset, amount, loan):
    try:
        ltv = config['blockchains'][blockchain][version][asset]
        loan_75 = loan / ltv
        liquidation_price = loan_75 / amount
        return liquidation_price
    except KeyError:
        return 0  # Platzhalterwert, bitte ersetzen


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blockchain = request.form['blockchain']
        version = request.form['version']
        asset = request.form['asset']
        amount = float(request.form['amount'])
        loan = float(request.form['loan'])
        # Hole den LTV-Wert aus der Konfiguration
        ltv = config['blockchains'][blockchain][version][asset]

        liquidation_price = calculate_liquidation_price(blockchain, version, asset, amount, loan)

        return render_template('index.html', blockchains=blockchains, versions=versions, assets=assets,
                               selected_blockchain=blockchain, selected_version=version, selected_asset=asset,
                               amount=amount, loan=loan, liquidation_price=liquidation_price, ltv=ltv)

    return render_template('index.html', blockchains=blockchains, versions=versions, assets=assets,
                           selected_blockchain=None, selected_version=None, selected_asset=None,
                           amount=0.1, loan=None, liquidation_price=None, ltv=None)


if __name__ == '__main__':
    app.run(debug=True)
