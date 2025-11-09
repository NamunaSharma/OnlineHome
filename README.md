EasyHome
EasyHome is an intelligent online home service platform built using Python (Django), SQLite, HTML, CSS, and JavaScript.
It connects users with nearby service providers and enhances the booking experience through machine-learning-based recommendations.
**--Features**
**Smart Recommendations**
**Location-Based Filtering:** Uses the K-Nearest Neighbors (KNN) algorithm to display providers near the user’s location.
**Content-Based Recommendations:** Implements TF-IDF vectorization and cosine similarity on service descriptions to suggest similar services.

**Secure Booking & Ratings**

Users can book services securely, rate providers, and track their service history.

** Dashboards**

**Admin Dashboard:** Manage users, service providers, and bookings.

Service Provider Dashboard: Update services, view bookings, and manage customer interactions.

**Tech Stack**
Component	Technology
Backend	Python (Django)
Frontend	HTML, CSS, JavaScript
Database	SQLite
Machine Learning	scikit-learn (KNN, TF-IDF, cosine similarity)

**Installation & Setup**
1️⃣ Clone the repository
git clone https://github.com/yourusername/EasyHome.git
cd EasyHome

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # for macOS/Linux
venv\Scripts\activate      # for Windows

3️⃣ Install dependencies

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the development server
python manage.py runserver


Now open http://127.0.0.1:8000/ in your browser 

📈 How It Works

User registers, enters location, and browses available services.

KNN algorithm filters services based on location proximity.

TF-IDF + cosine similarity recommend similar services to the user.

Users can book services, make secure payments, and rate providers.

Admins and providers manage their respective dashboards efficiently.
