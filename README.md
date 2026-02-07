# 💎 Sanly Shop | Elite AI-Powered Tech Store

Sanly Shop is a premium, state-of-the-art e-commerce platform for high-end electronics. It features a sophisticated AI-powered image search engine and an elite-tier user interface designed for a seamless, luxurious shopping experience.

![Elite Design Preview](/home/kkk/projects/tmcars/static/img/bg.png)

## 🚀 Key Features

### 🧠 AI Image Search Engine
- **EfficientNet-B7 Integration**: Utilizes advanced deep learning to identify and match products based on visual similarity.
- **Performance Optimized**: Features are pre-calculated and indexed in the database, allowing for near-instant search results without heavy per-request computation.
- **Dual Input**: Supports high-quality image uploads and live camera capture with a modern, glassmorphic interface.

### 🏛️ Elite Design System
- **Elite Dark Aesthetics**: A professional-grade dark theme with deep contrast and vibrant blue accents.
- **Glassmorphism**: Unified design across all components using ultra-refined backdrop blurs and subtle geometric borders.
- **Inter Typography**: Sophisticated use of the Inter font family for maximum readability and a modern feel.
- **Custom Visuals**: Bespoke futuristic background imagery integrated with a refined dark overlay.

## 🛠️ Technology Stack
- **Backend**: Django 5.1
- **Real-time**: Django Channels & Redis
- **AI/ML**: PyTorch, TorchVision (EfficientNet-B7), OpenCV
- **Frontend**: Vanilla HTML5/CSS3, Bootstrap 5.3 (Elite Customization)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)

## 📦 Setup & Installation

1. **Environment Initialization**:
   Ensure you are using Python 3.12:
   ```bash
   source myenv/bin/activate
   ```

2. **Dependencies**:
   Install the required premium toolchain (ensure `pip` is available):
   ```bash
   pip install django django-channels channels-redis torch torchvision opencv-python pillow numpy
   ```

3. **Database Setup**:
   ```bash
   python manage.py makemigrations search
   python manage.py migrate
   ```

4. **AI Indexing**:
   Perform the initial indexing of all products to prime the search engine:
   ```bash
   python manage.py index_products
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 💻 Local Development

Follow these steps to set up the project on your local machine:

### 1. Clone & Environment
```bash
git clone https://github.com/Tacmyrat02/tmcars.git
cd tmcars
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy the environment template and configure your local settings:
```bash
cp .env.template .env
```
*(Optionally edit `.env` for custom database or redis settings)*

### 4. Database & Product Seeding
Initialize the database and populate it with elite-tier products:
```bash
python manage.py migrate
python manage.py seed_products
python manage.py index_products
```

### 5. Start the Project
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000 in your browser.

## 🚀 Production Deployment

To deploy **Sanly Shop** in a production environment (e.g., Ubuntu VPS), follow these steps:

### 1. Environment Configuration
Copy the template and fill in your production values:
```bash
cp .env.template .env
nano .env
```
Ensure `DEBUG=False` and `ALLOWED_HOSTS` are set correctly.

### 2. Dependency Installation
Install all dependencies from the freeze-lock:
```bash
pip install -r requirements.txt
```

### 3. Static Assets & Database
Prepare the database and collect all static files (CSS/JS) into the production folder:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Background Services & AI
Ensure **Redis** is running for real-time features:
```bash
sudo systemctl start redis
```
Re-run indexing if you add new products in production:
```bash
python manage.py index_products
```

### 5. Process Management (Recommended)
Use **Gunicorn** or **Daphne** (required for Channels) with **Supervisor** or **Systemd** to keep the server running.

## 📜 Development Notes
- **AI Stability**: The system is optimized for CPU/GPU inference. Ensure requirements for `torch` are met on the target server.
- **Media Storage**: In production, consider using S3 or a dedicated volume for `/media` if your server is ephemeral.

---
*© 2026 Sanly Shop - Redefining Digital Commerce*
# tachmyrat
