from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from slugify import slugify
from functools import wraps
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Render.com için veritabanı yolu
if os.environ.get('RENDER'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/render/project/src/blog.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Yüklenen resimleri sunmak için route
@app.route('/data/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except:
        return send_from_directory('static', 'default-post.jpg')

db = SQLAlchemy(app)

# Admin bilgileri
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='category_rel', lazy=True)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug') and kwargs.get('name'):
            kwargs['slug'] = slugify(kwargs.get('name'))
        super().__init__(*args, **kwargs)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    preview = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reading_time = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug') and kwargs.get('title'):
            kwargs['slug'] = slugify(kwargs.get('title'))
        super().__init__(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            return f"/{app.config['UPLOAD_FOLDER']}/{self.image}"
        return "/static/default-post.jpg"  # Varsayılan resim

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.cookies.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.cookies.get('user_id'):
            return redirect(url_for('auth_login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    with app.app_context():
        db.create_all()
        
        # Varsayılan kategorileri ekle
        if not Category.query.first():
            default_categories = [
                "Teknoloji",
                "Yazılım Geliştirme",
                "Web Tasarım",
                "Mobil Uygulama",
                "Veri Bilimi",
                "Yapay Zeka",
                "Siber Güvenlik",
                "DevOps"
            ]
            for cat_name in default_categories:
                category = Category(name=cat_name)
                db.session.add(category)
            db.session.commit()

def clean_unused_images():
    """Kullanılmayan resimleri temizle"""
    # Veritabanındaki tüm resim dosyalarını al
    used_images = set()
    posts = Post.query.all()
    for post in posts:
        if post.image:
            used_images.add(post.image)
    
    # images klasöründeki tüm dosyaları kontrol et
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename not in used_images:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                os.remove(file_path)
                print(f"Silinen dosya: {filename}")
            except Exception as e:
                print(f"Dosya silinirken hata: {filename} - {str(e)}")

def save_image(file, post_id):
    """Resmi kaydet ve dosya adını döndür"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        _, ext = os.path.splitext(filename)
        image_filename = f"post_{post_id}{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        
        # Eğer aynı isimde dosya varsa sil
        if os.path.exists(file_path):
            os.remove(file_path)
        
        file.save(file_path)
        return image_filename
    return None

@app.route('/')
def index():
    posts = Post.query.filter_by(status='approved').order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            response = redirect(url_for('admin_dashboard'))
            response.set_cookie('admin_logged_in', 'true')
            return response
        else:
            flash('Hatalı kullanıcı adı veya şifre!', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    response = redirect(url_for('admin_login'))
    response.delete_cookie('admin_logged_in')
    return response

@app.route('/admin')
@admin_required
def admin_dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

@app.route('/admin/post/new', methods=['GET', 'POST'])
@admin_required
def admin_new_post():
    if request.method == 'POST':
        category = Category.query.get(request.form['category_id'])
        if not category:
            flash('Geçersiz kategori!', 'danger')
            return redirect(url_for('admin_new_post'))

        # Admin kullanıcısını bul veya oluştur
        admin_user = User.query.filter_by(username=ADMIN_USERNAME).first()
        if not admin_user:
            admin_user = User(
                username=ADMIN_USERNAME,
                email='admin@example.com'
            )
            admin_user.set_password(ADMIN_PASSWORD)
            db.session.add(admin_user)
            db.session.commit()

        post = Post(
            title=request.form['title'],
            preview=request.form['preview'],
            content=request.form['content'],
            category_id=category.id,
            author_id=admin_user.id,
            reading_time=int(request.form['reading_time']),
            status='approved'
        )
        db.session.add(post)
        db.session.commit()  # Önce post'u kaydet ve ID al

        # Resim yükleme işlemi
        if 'image' in request.files:
            image_filename = save_image(request.files['image'], post.id)
            if image_filename:
                post.image = image_filename
                db.session.commit()

        flash('Yazı başarıyla eklendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/post_form.html', categories=categories)

@app.route('/admin/post/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        category = Category.query.get(request.form['category_id'])
        if not category:
            flash('Geçersiz kategori!', 'danger')
            return redirect(url_for('admin_edit_post', id=id))

        # Resim yükleme işlemi
        if 'image' in request.files:
            image_filename = save_image(request.files['image'], post.id)
            if image_filename:
                post.image = image_filename

        post.title = request.form['title']
        post.preview = request.form['preview']
        post.content = request.form['content']
        post.category_id = category.id
        post.reading_time = int(request.form['reading_time'])
        post.slug = slugify(request.form['title'])
        
        db.session.commit()
        flash('Yazı başarıyla güncellendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/post_form.html', post=post, categories=categories)

@app.route('/admin/post/delete/<int:id>')
@admin_required
def admin_delete_post(id):
    post = Post.query.get_or_404(id)
    
    # Resmi sil
    if post.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    flash('Yazı başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/post/approve/<int:id>')
@admin_required
def admin_approve_post(id):
    post = Post.query.get_or_404(id)
    post.status = 'approved'
    db.session.commit()
    flash('Yazı başarıyla onaylandı!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/post/reject/<int:id>')
@admin_required
def admin_reject_post(id):
    post = Post.query.get_or_404(id)
    post.status = 'rejected'
    db.session.commit()
    flash('Yazı reddedildi!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash('Şifreler eşleşmiyor!', 'danger')
            return redirect(url_for('auth_register'))

        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor!', 'danger')
            return redirect(url_for('auth_register'))

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta adresi zaten kullanılıyor!', 'danger')
            return redirect(url_for('auth_register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth_login'))

    return render_template('auth/register.html')

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            response = redirect(url_for('user_dashboard'))
            response.set_cookie('user_id', str(user.id))
            return response
        
        flash('Hatalı e-posta veya şifre!', 'danger')
        return redirect(url_for('auth_login'))
    
    return render_template('auth/login.html')

@app.route('/auth/logout')
def auth_logout():
    response = redirect(url_for('index'))
    response.delete_cookie('user_id')
    return response

@app.route('/user/dashboard')
@user_required
def user_dashboard():
    user_id = int(request.cookies.get('user_id'))
    posts = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template('user/dashboard.html', posts=posts)

@app.route('/user/post/new', methods=['GET', 'POST'])
@user_required
def user_new_post():
    if request.method == 'POST':
        user_id = int(request.cookies.get('user_id'))
        category = Category.query.get(request.form['category_id'])
        if not category:
            flash('Geçersiz kategori!', 'danger')
            return redirect(url_for('user_new_post'))

        post = Post(
            title=request.form['title'],
            preview=request.form['preview'],
            content=request.form['content'],
            category_id=category.id,
            author_id=user_id,
            reading_time=int(request.form['reading_time']),
            status='pending'
        )
        db.session.add(post)
        db.session.commit()  # Önce post'u kaydet ve ID al

        # Resim yükleme işlemi
        if 'image' in request.files:
            image_filename = save_image(request.files['image'], post.id)
            if image_filename:
                post.image = image_filename
                db.session.commit()

        flash('Yazı başarıyla eklendi! Admin onayından sonra yayınlanacaktır.', 'success')
        return redirect(url_for('user_dashboard'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('user/post_form.html', categories=categories)

@app.route('/user/post/edit/<int:id>', methods=['GET', 'POST'])
@user_required
def user_edit_post(id):
    user_id = int(request.cookies.get('user_id'))
    post = Post.query.filter_by(id=id, author_id=user_id).first_or_404()
    
    if request.method == 'POST':
        category = Category.query.get(request.form['category_id'])
        if not category:
            flash('Geçersiz kategori!', 'danger')
            return redirect(url_for('user_edit_post', id=id))

        # Resim yükleme işlemi
        if 'image' in request.files:
            image_filename = save_image(request.files['image'], post.id)
            if image_filename:
                post.image = image_filename

        post.title = request.form['title']
        post.preview = request.form['preview']
        post.content = request.form['content']
        post.category_id = category.id
        post.reading_time = int(request.form['reading_time'])
        post.slug = slugify(request.form['title'])
        post.status = 'pending'  # Düzenlenen yazı tekrar onaya gönderilir
        
        db.session.commit()
        flash('Yazı başarıyla güncellendi! Admin onayından sonra yayınlanacaktır.', 'success')
        return redirect(url_for('user_dashboard'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('user/post_form.html', post=post, categories=categories)

@app.route('/user/post/delete/<int:id>')
@user_required
def user_delete_post(id):
    user_id = int(request.cookies.get('user_id'))
    post = Post.query.filter_by(id=id, author_id=user_id).first_or_404()
    
    # Resmi sil
    if post.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    flash('Yazı başarıyla silindi!', 'success')
    return redirect(url_for('user_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
        clean_unused_images()  # Uygulama başlarken gereksiz resimleri temizle
    app.run(debug=True) 