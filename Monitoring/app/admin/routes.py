from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User  # Assurez-vous d'avoir un modèle User dans vos modèles
from app.models import Client



auth_bp = Blueprint('auth', __name__)

admin_bp = Blueprint('admin', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Remplacez cette logique avec la vérification réelle des informations d'identification
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login'))

@admin_bp.route('/client_list')
def client_list():
    clients = Client.query.all()  # Récupérez tous les clients (ajustez cela selon votre modèle)
    return render_template('admin/client_list.html', clients=clients)