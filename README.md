<p align="center">
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Oracle_SQL-Ready-F80000?style=for-the-badge&logo=oracle&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq_AI-Integrated-4B32C3?style=for-the-badge&logo=ai&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
</p>

<h1 align="center">🛍️ SmartShop — AI-Powered E-Commerce Platform</h1>

<p align="center">
  <strong>A full-stack, enterprise-grade e-commerce platform with AI-powered recommendations, chatbot support, fraud detection, sentiment analysis, price prediction, and more.</strong>
</p>

<p align="center">
  Built with <strong>Django + Oracle SQL + Redis + Groq AI + HTML/CSS/JavaScript</strong>
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Prerequisites — What You Need Before Starting](#-prerequisites--what-you-need-before-starting)
- [Step-by-Step Installation Guide](#-step-by-step-installation-guide)
- [Running the Application](#-running-the-application)
- [Login Credentials](#-login-credentials)
- [All Pages & URLs](#-all-pages--urls)
- [Project Structure](#-project-structure)
- [AI Features Explained](#-ai-features-explained)
- [API Endpoints](#-api-endpoints)
- [Oracle SQL Setup (Optional)](#-oracle-sql-setup-optional)
- [Redis Setup (Optional)](#-redis-setup-optional)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | 🔐 **User Authentication** | Login, Sign Up, Logout with secure password hashing |
| 2 | 👤 **User Profiles** | Profile management, avatar, loyalty points, premium status |
| 3 | 📍 **Address Management** | Multiple shipping/billing addresses with default selection |
| 4 | 🛍️ **Product Catalog** | 16+ products across 8 categories with search, filter, sort, pagination |
| 5 | 🛒 **Shopping Cart** | Add, update, remove items with real-time AJAX updates |
| 6 | 📝 **Checkout Flow** | Multi-step checkout with saved address selection |
| 7 | 💳 **Payment Processing** | Simulated payment gateway (Card, UPI, Net Banking, COD) |
| 8 | 📦 **Order Management** | Order history, status tracking, order details |
| 9 | 📍 **Order Tracking** | Real-time tracking timeline with progress visualization |
| 10 | 🤖 **AI Recommendation Engine** | Groq-powered personalized product recommendations |
| 11 | 💬 **AI Chatbot Support** | 24/7 AI customer support chatbot on every page |
| 12 | 🛡️ **Fraud Detection** | AI-powered order fraud risk scoring and flagging |
| 13 | 📊 **Sentiment Analysis** | Automatic review sentiment scoring (positive/negative/neutral) |
| 14 | 🔮 **Price Prediction** | AI-based price trend analysis and buy/wait recommendations |
| 15 | 🕵️ **Fake Review Detection** | AI-powered detection of suspicious/fake reviews |
| 16 | 📈 **Admin Analytics Dashboard** | Revenue charts, top products, fraud alerts, AI insights |
| 17 | 🏭 **Warehouse Dashboard** | Inventory management, stock alerts, shipment tracking |
| 18 | 🎨 **Glassmorphism UI** | Premium frosted-glass design with orange & purple theme |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.10+ & Django 5.x | Server, business logic, ORM |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | UI with glassmorphism design |
| **Database** | SQLite (dev) / Oracle SQL (prod) | Data storage |
| **AI/ML** | Groq API (LLaMA 3.3 70B) | All AI features |
| **Cache** | Redis (optional) | Session & data caching |
| **API** | Django REST Framework | RESTful API endpoints |
| **Design** | Glassmorphism + Inter Font | Premium enterprise UI |

---

## 📸 Screenshots

> After running the app, visit `http://127.0.0.1:8000/` to see:
> - **Home Page** — Hero section, featured products, categories, deals
> - **Product Listing** — Grid layout with filters and sorting
> - **Product Detail** — Reviews, AI price prediction, related products
> - **Shopping Cart** — Item management with order summary
> - **Checkout** — Shipping address form with saved addresses
> - **Payment** — Card/UPI/COD payment options
> - **Admin Analytics** — Revenue charts, fraud alerts, AI insights
> - **Warehouse** — Inventory levels, stock alerts, shipments

---

## 📋 Prerequisites — What You Need Before Starting

> **⚠️ IMPORTANT: Read this section carefully if you have never used Python or Django before.**

### 1. Install Python (Required)

Python is the programming language this project is built with. You need version **3.10 or higher**.

#### Windows:

1. Go to the **official Python website**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python 3.x.x"** button
3. **Run the downloaded installer** (`.exe` file)
4. **⚠️ VERY IMPORTANT**: On the first screen of the installer, check the box that says:
   ```
   ☑ Add Python to PATH
   ```
   This is at the **bottom of the installer window**. If you miss this, nothing will work!
5. Click **"Install Now"**
6. Wait for installation to complete, then click **"Close"**

#### Verify Python is installed:

Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and type:

```bash
python --version
```

You should see something like:
```
Python 3.10.x
```

If you see `Python was not found` or an error, Python was not added to PATH. Reinstall and make sure to check "Add Python to PATH".

#### macOS:

```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10
```

#### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Install Git (Required)

Git is needed to download (clone) this project.

#### Windows:

1. Go to: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer
3. Click **"Next"** through all options (defaults are fine)
4. Click **"Install"**

#### Verify Git is installed:

```bash
git --version
```

You should see: `git version 2.x.x`

#### macOS:
```bash
brew install git
```

#### Linux:
```bash
sudo apt install git
```

### 3. A Text Editor (Optional but Recommended)

To view or edit the code, install one of these:
- **VS Code** (Recommended): [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Notepad++**: [https://notepad-plus-plus.org/](https://notepad-plus-plus.org/)

### 4. A Web Browser

Any modern browser works: **Chrome**, **Firefox**, **Edge**, or **Safari**.

---

## 🚀 Step-by-Step Installation Guide

> Follow these steps **exactly in order**. Copy-paste each command.

### Step 1: Open Command Prompt / Terminal

- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **macOS**: Press `Cmd + Space`, type `Terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 2: Choose Where to Download the Project

Navigate to where you want the project. For example, your Desktop:

```bash
# Windows
cd %USERPROFILE%\Desktop

# macOS / Linux
cd ~/Desktop
```

### Step 3: Download (Clone) the Project

```bash
git clone https://github.com/vasistacv/Ecommerce.git
```

This creates a folder called `Ecommerce` with all the project files.

### Step 4: Go Into the Project Folder

```bash
cd Ecommerce
```

### Step 5: Create a Virtual Environment

A virtual environment keeps this project's packages separate from your system Python.

```bash
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### Step 6: Activate the Virtual Environment

```bash
# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

After activation, you should see `(.venv)` at the beginning of your command line:
```
(.venv) C:\Users\YourName\Desktop\Ecommerce>
```

> **⚠️ You must activate the virtual environment every time you open a new terminal window to run the project.**

### Step 7: Install All Required Packages

```bash
pip install -r requirements.txt
```

This will download and install Django, Groq AI, and all other dependencies. Wait for it to finish (may take 1-2 minutes).

You should see `Successfully installed ...` at the end.

### Step 8: Set Up the Database

```bash
# Create database tables
python manage.py makemigrations accounts products cart orders payments ai_engine warehouse

python manage.py migrate
```

### Step 9: Load Sample Data (Products, Users, Categories)

```bash
python manage.py seed_data
```

You should see:
```
Seeding database...
  [OK] Superuser created (admin/admin123)
  [OK] Test users created
  [OK] Categories created
  [OK] 16 products created
  [OK] Reviews created
  [OK] Price history created
  [OK] Warehouses & inventory created
  [OK] Addresses created

Database seeded successfully!
   Admin Login: admin / admin123
   Test User:   user1 / password123
```

### Step 10: Start the Server! 🎉

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 11: Open in Your Browser

Open your web browser and go to:

👉 **http://127.0.0.1:8000/**

🎉 **The SmartShop e-commerce platform is now running on your computer!**

---

## ▶️ Running the Application

Every time you want to run the application after the first setup:

```bash
# 1. Open Command Prompt / Terminal

# 2. Go to the project folder
cd path\to\Ecommerce

# 3. Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Start the server
python manage.py runserver

# 5. Open http://127.0.0.1:8000/ in your browser
```

To **stop the server**, press `Ctrl + C` in the terminal.

---

## 🔑 Login Credentials

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | `admin` | `admin123` | Full access + Analytics + Warehouse + Django Admin |
| **Test User 1** | `user1` | `password123` | Normal shopping user |
| **Test User 2** | `user2` | `password123` | Normal shopping user |
| **Test User 3** | `user3` | `password123` | Normal shopping user |

> You can also create your own account via the **Sign Up** page!

---

## 🌐 All Pages & URLs

| Page | URL | Access |
|------|-----|--------|
| **Home Page** | `http://127.0.0.1:8000/` | Everyone |
| **All Products** | `http://127.0.0.1:8000/products/` | Everyone |
| **Product Detail** | `http://127.0.0.1:8000/products/<slug>/` | Everyone |
| **Login** | `http://127.0.0.1:8000/accounts/login/` | Everyone |
| **Register** | `http://127.0.0.1:8000/accounts/register/` | Everyone |
| **Profile** | `http://127.0.0.1:8000/accounts/profile/` | Logged in |
| **Shopping Cart** | `http://127.0.0.1:8000/cart/` | Logged in |
| **Checkout** | `http://127.0.0.1:8000/orders/checkout/` | Logged in |
| **My Orders** | `http://127.0.0.1:8000/orders/` | Logged in |
| **Order Tracking** | `http://127.0.0.1:8000/orders/<id>/track/` | Logged in |
| **Analytics Dashboard** | `http://127.0.0.1:8000/analytics/dashboard/` | Admin only |
| **Warehouse Dashboard** | `http://127.0.0.1:8000/warehouse/dashboard/` | Admin only |
| **Django Admin Panel** | `http://127.0.0.1:8000/admin/` | Admin only |
| **AI Chatbot** | 💬 Button (bottom-right corner) | Everyone |

---

## 📂 Project Structure

```
Ecommerce/
│
├── manage.py                  # Django management script
├── requirements.txt           # Python package dependencies
├── setup.bat                  # Windows auto-setup script
├── .env                       # Environment variables (API keys, DB config)
├── db.sqlite3                 # SQLite database (auto-generated)
│
├── config/                    # Django project configuration
│   ├── settings.py            #   Main settings (DB, cache, apps, AI config)
│   ├── urls.py                #   Root URL routing
│   ├── wsgi.py                #   WSGI entry point
│   └── asgi.py                #   ASGI entry point
│
├── accounts/                  # User authentication & profiles
│   ├── models.py              #   UserProfile, Address, UserActivity models
│   ├── views.py               #   Login, Register, Profile, Address views
│   ├── forms.py               #   Registration, Login, Profile forms
│   ├── urls.py                #   URL routing
│   └── admin.py               #   Admin panel registration
│
├── products/                  # Product catalog
│   ├── models.py              #   Product, Category, Review, PriceHistory
│   ├── views.py               #   Product list, detail, search, review
│   ├── urls.py                #   URL routing
│   ├── admin.py               #   Admin panel registration
│   └── management/commands/   #   seed_data command
│
├── cart/                      # Shopping cart
│   ├── models.py              #   Cart, CartItem models
│   ├── views.py               #   Add, update, remove, clear cart
│   ├── urls.py                #   URL routing
│   └── context_processors.py  #   Cart count in navbar
│
├── orders/                    # Order management
│   ├── models.py              #   Order, OrderItem, OrderTracking
│   ├── views.py               #   Checkout, order list, detail, tracking
│   ├── urls.py                #   URL routing
│   └── admin.py               #   Admin with inline items & tracking
│
├── payments/                  # Payment processing
│   ├── models.py              #   Payment model (Card, UPI, COD, etc.)
│   ├── views.py               #   Payment processing & success page
│   ├── urls.py                #   URL routing
│   └── admin.py               #   Admin panel registration
│
├── ai_engine/                 # 🤖 AI/ML features (Groq API)
│   ├── groq_client.py         #   Groq API client wrapper
│   ├── recommender.py         #   AI product recommendation engine
│   ├── chatbot.py             #   AI customer support chatbot
│   ├── fraud_detection.py     #   AI fraud risk scoring
│   ├── sentiment.py           #   AI review sentiment analysis
│   ├── price_prediction.py    #   AI price trend prediction
│   ├── fake_review.py         #   AI fake review detection
│   ├── views.py               #   API endpoints for all AI features
│   └── urls.py                #   URL routing
│
├── analytics/                 # Admin analytics dashboard
│   ├── views.py               #   Dashboard with metrics & charts
│   └── urls.py                #   URL routing
│
├── warehouse/                 # Warehouse management
│   ├── models.py              #   Warehouse, Inventory, Shipment
│   ├── views.py               #   Warehouse dashboard
│   ├── urls.py                #   URL routing
│   └── admin.py               #   Admin panel registration
│
├── templates/                 # HTML templates
│   ├── base.html              #   Master template (navbar, footer, chatbot)
│   ├── home.html              #   Homepage
│   ├── accounts/              #   Login, register, profile, address forms
│   ├── products/              #   Product list & detail pages
│   ├── cart/                  #   Shopping cart page
│   ├── orders/                #   Checkout, order list, detail, tracking
│   ├── payments/              #   Payment form & success page
│   ├── analytics/             #   Admin analytics dashboard
│   └── warehouse/             #   Warehouse management dashboard
│
├── static/                    # Static assets
│   ├── css/style.css          #   Main stylesheet (glassmorphism theme)
│   └── js/
│       ├── main.js            #   Core JavaScript (cart AJAX, search)
│       ├── chatbot.js         #   AI chatbot widget
│       └── analytics.js       #   Dashboard charts (Chart.js)
│
└── sql/                       # Database scripts
    └── schema.sql             #   Oracle SQL schema (all tables)
```

---

## 🤖 AI Features Explained

All AI features are powered by the **Groq API** using the **LLaMA 3.3 70B** model.

### 1. 🎯 Recommendation Engine (`ai_engine/recommender.py`)
- Analyzes user browsing history, purchases, and cart activity
- Recommends products based on preferences, categories, and price range
- Provides personalized reasons for each recommendation

### 2. 💬 Chatbot Support (`ai_engine/chatbot.py`)
- Available on every page via the 💬 floating button
- Knows about orders, shipping policies, returns, and products
- Context-aware: sees user's recent orders and loyalty points
- Maintains conversation history for natural dialog

### 3. 🛡️ Fraud Detection (`ai_engine/fraud_detection.py`)
- Analyzes orders for suspicious patterns
- Considers: order value vs history, new accounts, unusual quantities
- Returns risk score (0-1) with approve/review/reject recommendation
- Flags high-risk orders in admin dashboard

### 4. 📊 Sentiment Analysis (`ai_engine/sentiment.py`)
- Automatically analyzes review text for sentiment
- Scores from -1 (negative) to +1 (positive)
- Labels: positive / negative / neutral
- Extracts key points from each review

### 5. 🔮 Price Prediction (`ai_engine/price_prediction.py`)
- Analyzes 30-day price history and market factors
- Predicts price trend: up / down / stable
- Provides buy now / wait / neutral recommendation
- Available on each product detail page

### 6. 🕵️ Fake Review Detection (`ai_engine/fake_review.py`)
- Checks reviews for signs of inauthenticity
- Analyzes: vague language, mismatched rating/content, generic text
- Flags suspicious reviews with confidence score
- Visible in admin dashboard

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/chat/` | AI Chatbot — send message, get response |
| `GET` | `/api/ai/recommend/` | Get AI recommendations |
| `POST` | `/api/ai/fraud-check/` | Check order for fraud |
| `POST` | `/api/ai/sentiment/` | Analyze review sentiment |
| `GET` | `/api/ai/predict-price/?product=<slug>` | Predict product price |
| `POST` | `/api/ai/fake-review/` | Detect fake reviews |

### Example: Chat with AI Bot

```bash
curl -X POST http://127.0.0.1:8000/api/ai/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your shipping policies?"}'
```

---

## 🗄️ Oracle SQL Setup (Optional)

> **Note**: The project runs on **SQLite by default** — no Oracle needed for development. Oracle is for production deployment.

If you want to use Oracle SQL:

### 1. Install Oracle Database XE

Download from: [https://www.oracle.com/database/technologies/xe-downloads.html](https://www.oracle.com/database/technologies/xe-downloads.html)

### 2. Create Database User

```sql
-- Connect as SYSDBA
sqlplus sys/password@localhost:1521/XEPDB1 as sysdba

-- Create user
CREATE USER ecommerce_user IDENTIFIED BY ecommerce_pass;
GRANT CONNECT, RESOURCE, DBA TO ecommerce_user;
ALTER USER ecommerce_user QUOTA UNLIMITED ON USERS;
```

### 3. Run Schema Script

```sql
@sql/schema.sql
```

### 4. Update Django Settings

In `config/settings.py`, uncomment the Oracle database config and comment out SQLite:

```python
# Oracle SQL (uncomment this)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'XEPDB1',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_pass',
        'HOST': 'localhost',
        'PORT': '1521',
    }
}
```

### 5. Install Oracle Python Driver

```bash
pip install oracledb
```

---

## 📦 Redis Setup (Optional)

Redis provides faster caching and session management.

### Windows:

1. Download Redis for Windows: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
2. Install and start Redis service
3. Install Python Redis packages:
   ```bash
   pip install redis django-redis
   ```

### macOS:
```bash
brew install redis
brew services start redis
```

### Linux:
```bash
sudo apt install redis-server
sudo systemctl start redis
```

Redis is automatically detected — if running, the app uses it; if not, it falls back to in-memory cache.

---

## 🔧 Troubleshooting

### ❌ "python is not recognized as an internal or external command"
- Python is not in your PATH
- Reinstall Python and check **"Add Python to PATH"**
- Or use the full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe`

### ❌ "No module named 'django'"
- Virtual environment is not activated
- Run: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
- Then: `pip install -r requirements.txt`

### ❌ "OperationalError: no such table"
- Database tables not created
- Run: `python manage.py migrate`

### ❌ "Template not found" or blank page
- Make sure you're in the project root directory (where `manage.py` is)
- Check that the `templates/` folder exists

### ❌ Port 8000 already in use
- Another process is using port 8000
- Use a different port: `python manage.py runserver 8080`
- Then visit: `http://127.0.0.1:8080/`

### ❌ AI Chatbot not responding
- Check your Groq API key in `.env` file
- Ensure you have internet connection
- The chatbot will show a fallback message if the API is unreachable

### ❌ Static files (CSS/JS) not loading
- Run: `python manage.py collectstatic`
- Or ensure `DEBUG = True` in `config/settings.py`

### ❌ Unicode/Emoji errors on Windows
- This is a Windows console encoding issue
- The application itself works fine in the browser
- Emojis display correctly in web pages

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Vasista CV**

- GitHub: [@vasistacv](https://github.com/vasistacv)

---

<p align="center">
  <strong>Built with ❤️ using Django + Groq AI</strong>
  <br>
  <em>SmartShop — Where AI Meets Shopping</em>
</p>
