# Reactides Healthcare Ecosystem 🏥

A complete healthcare ecosystem platform built with Django, designed to simplify healthcare services through doctor appointment booking, online medicine purchasing, and integrated healthcare service management.

Reactides combines healthcare consultation, appointment scheduling, and medicine e-commerce into one scalable digital platform.

---

# 🚀 Features

- 👨‍⚕️ Doctor Appointment Booking
- 💊 Online Medicine Ordering
- 🛒 Shopping Cart & Checkout System
- 📅 Appointment Scheduling
- 📧 OTP Email Verification
- 🔐 JWT Authentication
- 👥 User & Representative Management
- 🎟 Coupon & Discount System
- 🚚 Shipping Management
- 📦 Order Tracking
- 📜 Prescription Support
- 🧾 Order & Appointment Status History
- ⚡ REST API with Django REST Framework
- 📨 Asynchronous Email Sending with Celery

---

# 🏗 Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend Language |
| Django | Web Framework |
| Django REST Framework | API Development |
| PostgreSQL | Database |
| Redis | Celery Broker & Caching |
| Celery | Background Tasks & Email Queue |
| JWT | Authentication |
| Gunicorn | Production Server |
| Nginx | Reverse Proxy |

---

# 📦 Core Modules

## 👤 Authentication System

Features:
- User Registration
- Email OTP Verification
- Login & JWT Authentication
- User Roles & Permissions
- Representative Accounts

Main Entities:
- `account_user`
- `account_emailotp`
- `auth_group`
- `auth_permission`

---

## 👨‍⚕️ Doctor Appointment Module

Users can:
- Book appointments with doctors
- Choose consultation types
- Select appointment schedules
- Track appointment statuses

Features:
- Medical history support
- Current medication tracking
- Allergy information
- Appointment history logs
- Payment status tracking

Main Entities:
- `appointment_appointment`
- `appointment_appointmentstatushistory`
- `doctor_doctor`
- `consultation_type_consultationtype`

---

## 💊 Medicine E-Commerce System

Features:
- Medicine listing
- Product details & dosage information
- Shopping cart system
- Coupon & shipping discounts
- Order placement
- Order item tracking

Main Entities:
- `products`
- `cart_cart`
- `cart_cartitem`
- `checkout_order`
- `checkout_orderitem`

---

## 🛒 Cart & Checkout System

Includes:
- Dynamic cart management
- Shipping calculations
- Tax calculations
- Coupon discounts
- Payment method support

Features:
- Order subtotal & totals
- Shipping discounts
- Representative referral tracking

---

## 📦 Order Management

Users can:
- Place medicine orders
- Track order statuses
- View purchase history
- Manage shipping addresses

Main Entities:
- `checkout_order`
- `checkout_orderstatushistory`
- `account_shippingaddress`

---

## 📧 Celery Email Queue System

Reactides uses Celery for asynchronous background tasks such as:

- OTP email sending
- Appointment confirmation emails
- Order confirmation emails
- Notification emails

Benefits:
- Faster API responses
- Reliable email delivery
- Background task processing
- Improved scalability

---

# 🗄 Database Architecture

The backend system includes:

- Users & Authentication
- Doctors
- Appointments
- Consultation Types
- Medicines & Products
- Shopping Cart
- Orders & Checkout
- Coupons & Discounts
- Representatives

---

# 📊 ER Diagram

Below is the complete backend database ER diagram:

![Reactides ER Diagram](./Reactides.png)

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/reactides-backend.git

cd reactides-backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env`

```env
DEBUG=True

SECRET_KEY=your_secret_key

ALLOWED_HOSTS=*

DATABASE_URL=postgresql://postgres:password@localhost:5432/reactides

REDIS_URL=redis://127.0.0.1:6379

JWT_SECRET_KEY=your_jwt_secret

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

---

# 🛠 Run Migrations

```bash
python manage.py migrate
```

---

# 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---

# ▶️ Run Development Server

```bash
python manage.py runserver
```

---

# ⚡ Run Celery Worker

```bash
celery -A config worker -l info
```

---

# 🔥 Start Redis

```bash
redis-server
```

---

# 📡 Example API Routes

```http
/api/auth/
/api/doctors/
/api/appointments/
/api/products/
/api/cart/
/api/orders/
/api/coupons/
```

---

# 🔐 Authentication

Reactides uses JWT Authentication.

Example:

```http
Authorization: Bearer <token>
```

---

# 📁 File Management

Used for:

- Product images
- Medical PDFs
- User avatars
- Prescription files

---

# 🚀 Recommended Production Stack

- Ubuntu VPS
- Nginx
- Gunicorn
- PostgreSQL
- Redis
- Celery
- Supervisor

---

# 🧪 Future Improvements

- Video Consultation
- AI Health Assistance
- Online Prescription Upload
- Mobile Applications
- Live Doctor Chat
- Multi-vendor Pharmacy System

---

# 🤝 Contributing

Pull requests are welcome.

Steps:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request

---

# 📄 License

MIT License

---

# 👨‍💻 Developed By

Reactides Healthcare Team

Built with ❤️ using Django, DRF, PostgreSQL, Celery, and scalable backend technologies.
