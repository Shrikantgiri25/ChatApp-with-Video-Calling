# ChatApp with Video Calling

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Backend](https://img.shields.io/badge/backend-Django-blue)
![WebSockets](https://img.shields.io/badge/real--time-WebSockets-green)
![Auth](https://img.shields.io/badge/auth-Google%20OAuth%20%2B%20JWT-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 📌 Project Status – In Progress

Backend development is actively underway.

### ✅ Implemented Backend Features

* **Real-time Communication**

  * One-to-One Chat (WebSocket)
  * Group Chat (WebSocket)
  * Real-time Notifications (WebSocket)
* **Authentication**

  * Custom WebSocket Authentication Middleware
  * Google OAuth Integration
  * JWT Authentication
* **Services**

  * Email Sending Service
  * Email Link Verification
  * Token Creation & Verification
  * User Creation & Profile Updates
* **Routing**

  * Centralized routing for WebSocket consumers

### 🚀 Planned Features

* Video Calling (WebRTC)
* Audio Calling
* Frontend UI Implementation

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/ChatApp-with-Video-Calling.git
cd ChatApp-with-Video-Calling
```

**2. Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create `local.ini` configuration**
Inside the `config` folder, create a file named **`local.ini`** and paste the following content:

```ini
[DEFAULT]
DEBUG_VALUE=True
SECRET_KEY=
ALLOWED_HOSTS=*

[DATABASE]
ENGINE=django.db.backends.postgresql
NAME=
USER=
PASSWORD=
HOST=localhost
PORT=5432

[EMAIL]
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

[THROTTLE]
USER_THROTTLE_LIMIT = 80/hour
ANON_THROTTLE_LIMIT = 20/hour

[JWT_TOKEN]
JWT_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=1
ROTATE_REFRESH_TOKEN=True
BLACKLIST_AFTER_ROTATION=True

[REDIS]
REDIS_HOST=localhost
REDIS_PORT=6379
```

**5. Run migrations**

```bash
python manage.py migrate
```

**6. Start Redis (for WebSocket channel layer)**

```bash
redis-server
```

**7. Run the server**

```bash
python manage.py runserver
```

---

## 🧪 Quick Testing – One-to-One & Group Chat

For testing without the full frontend, you can use the included `templates/test_chat.html` file.

### **WebSocket Endpoints**

```python
from django.urls import re_path
from chitchat.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    # One-to-one chat: uuid1_uuid2
    re_path(r"ws/chat/(?P<room_name>[0-9a-f-]+_[0-9a-f-]+)/$", ChatConsumer.as_asgi()),
    # Group chat: group_uuid
    re_path(r"ws/chat/group_(?P<group_id>[0-9a-f-]+)/$", ChatConsumer.as_asgi()),
    # Notification: user_uuid
    re_path(
        r"ws/notifications/user_(?P<user_id>[0-9a-f-]+)/$",
        NotificationConsumer.as_asgi(),
    ),
]
```

**Example usage:**

* One-to-one chat:

  ```
  ws://127.0.0.1:8000/ws/chat/<uuid1>_<uuid2>/
  ```
* Group chat:

  ```
  ws://127.0.0.1:8000/ws/chat/group_<group_uuid>/
  ```
* Notifications:

  ```
  ws://127.0.0.1:8000/ws/notifications/user_<user_uuid>/
  ```

---

**1. Create a superuser and test accounts**

```bash
python manage.py createsuperuser
```

**2. Start the Django server & login via the browser**
Go to `http://127.0.0.1:8000/admin/` and log in. Create at least **two users** and one **group** with members.

**3. Open the test template**
Visit:

```
http://127.0.0.1:8000/test-chat/?room_name=<room_or_group_id>
```

**4. Open two browser tabs**

* Tab 1: Logged in as **User A**
* Tab 2: Logged in as **User B**

Type messages and watch them appear in **real-time** for both one-to-one and group chat.

---

## 📜 License

This project is licensed under the MIT License.
