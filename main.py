from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PRODUCTS_FILE = 'products.json'

# Load products from JSON file
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save products to JSON file
def save_products():
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file)

# Initialize products list
products = load_products()

# HTML templates within the Python file
home_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Gallery</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Product Gallery</h1>
        {% if 'logged_in' in session %}
            <a class="btn btn-primary mb-3" href="/add">Add New Product</a>
            <a class="btn btn-secondary mb-3" href="/logout">Logout</a>
        {% else %}
            <a class="btn btn-secondary mb-3" href="/login">Admin Login</a>
        {% endif %}
        <div class="row">
            {% for product in products %}
            <div class="col-md-4">
                <div class="card mb-4">
                    <img src="{{ product.image }}" class="card-img-top" alt="Product Image">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text">{{ product.description }}</p>
                        <p class="card-text text-muted">Price: ${{ product.price }}</p>
                        {% if 'logged_in' in session %}
                            <form action="/delete/{{ loop.index0 }}" method="POST">
                                <button type="submit" class="btn btn-danger">Delete</button>
                            </form>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1>Admin Login</h1>
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" class="form-control" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" class="form-control" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</body>
</html>
"""

add_product_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Add Product</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1>Add New Product</h1>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="name">Product Name:</label>
                <input type="text" class="form-control" name="name" required>
            </div>
            <div class="form-group">
                <label for="price">Price:</label>
                <input type="number" class="form-control" name="price" required>
            </div>
            <div class="form-group">
                <label for="description">Description:</label>
                <textarea class="form-control" name="description" required></textarea>
            </div>
            <div class="form-group">
                <label for="image">Image:</label>
                <input type="file" class="form-control" name="image" required>
            </div>
            <button type="submit" class="btn btn-success">Add Product</button>
        </form>
        <a href="/" class="btn btn-secondary mt-3">Back to Home</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page, products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template_string(login_page)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['image']
        
        if image:
            from werkzeug.utils import secure_filename
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            products.append({
                'name': name,
                'price': price,
                'description': description,
                'image': '/' + image_path
            })
            save_products()
        
        return redirect(url_for('home'))
    
    return render_template_string(add_product_page)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if 0 <= product_id < len(products):
        del products[product_id]
        save_products()
    return redirect(url_for('home'))

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)