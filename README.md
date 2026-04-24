# 🚀 SwiftURL - URL Shortener

SwiftURL is a fast and simple URL shortener built using FastAPI. It allows users to convert long URLs into short, manageable links and redirect them efficiently.

---

## 📌 Features

* 🔗 Shorten long URLs
* ⚡ Fast redirection
* 🗄️ SQLite database integration
* 🌐 Simple frontend (HTML)
* 📦 Lightweight and easy to use

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** SQLite
* **Frontend:** HTML
* **Server:** Uvicorn

---

## 📂 Project Structure

```
SwiftURL/
│── main.py
│── index.html
│── urls.db
│── README.md
```

---

## 🚀 How to Run Locally

1. Clone the repository:

```
git clone https://github.com/05Harshittiwari/SwiftURL.git
cd SwiftURL
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
pip install fastapi uvicorn
```

4. Run the server:

```
uvicorn main:app --reload
```

5. Open in browser:

```
http://127.0.0.1:8000
```

---

## 📸 Output

* Enter a long URL
* Get a shortened link
* Use it for redirection

---

## 🔮 Future Improvements

* User authentication
* Analytics (click tracking)
* Custom short URLs
* Deployment on cloud (Render / AWS)


⭐ If you like this project, give it a star!
