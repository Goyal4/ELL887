from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

app = Flask(__name__)

# Build the ODBC connection string and URL encode it
connection_params = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:dbproduct.database.windows.net,1433;"
    "DATABASE=ELL_Database;"
    "UID=ELL887;"
    "PWD=Manas_Cloud;"  # Replace with your actual password if needed
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)
params = quote_plus(connection_params)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product Model (with only required columns)
class Product(db.Model):
    __tablename__ = 'Products'  # Ensure correct table name

    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(500))
    Price = db.Column(db.Float, nullable=False)

# Route to list all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'ProductID': p.ProductID,
        'Name': p.Name,
        'Description': p.Description,
        'Price': p.Price
    } for p in products])

# Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        Name=data['Name'],
        Description=data.get('Description', ''),
        Price=data['Price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

# Route to search for products by name (supports multiple matches)
@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': "Query parameter 'q' is required"}), 400

    products = Product.query.filter(Product.Name.ilike(f"%{query}%")).all()

    if products:
        return jsonify([{
            'ProductID': p.ProductID,
            'Name': p.Name,
            'Description': p.Description,
            'Price': p.Price
        } for p in products])
    else:
        return jsonify({'message': 'No products found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
