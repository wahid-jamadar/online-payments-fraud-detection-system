# 🛡️ Online Payments Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

A state-of-the-art **Machine Learning powered web application** designed to detect and prevent fraudulent transactions in real-time. Built with a robust Flask backend and an intuitive dashboard, this system provides financial institutions with the tools to safeguard their online payment ecosystems. The core detection engine utilizes a **Random Forest Classifier** trained on millions of transaction logs.

---

## ✨ Key Features

- **📊 Advanced Analytics Dashboard**: Real-time visualization of transaction statistics, fraud rates, and recent activities.
- **🔍 Precision Prediction**: Leverages a Random Forest-driven model to identify suspicious patterns with high confidence scores.
- **📁 Bulk Processing**: Upload CSV files containing thousands of transactions for instant batch analysis and results export.
- **📧 Automated Fraud Alerts**: Instant email notifications triggered upon the detection of high-risk transactions.
- **📜 Transaction History**: Comprehensive searchable logs with pagination for auditing and manual review.
- **🔌 RESTful API**: Seamlessly integrate fraud detection capabilities into existing payment gateways.
- **📥 Data Portability**: Export analyzed transaction data directly to CSV for further offline reporting.

---

## 🚀 Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)
- **Machine Learning**: XGBoost, Scikit-Learn, Pandas, NumPy
- **Database**: MySQL (relational storage for transaction logs and user accounts)
- **Frontend**: Vanilla HTML5, CSS3 (Modern UI/UX), JavaScript
- **Security**: Werkzeug password hashing, session-based authentication

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/wahid-jamadar/online-payments-fraud-detection-system.git
cd online-payments-fraud-detection-system
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
1. Ensure **MySQL Server** is running.
2. Create the database using the provided schema:
   ```bash
   mysql -u your_username -p < database/schema.sql
   ```
3. Initialize the admin user:
   ```bash
   python create_admin.py
   ```
   *Default Credentials: `admin` / `admin123`*

### 5. Environment Variables
Create a `.env` file in the root directory and configure your credentials:
```env
SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=fraud_db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

---

## 📂 Project Structure

```text
├── database/           # SQL schema files
├── ml/                 # Training and preprocessing scripts
├── model/              # Trained pickle files (XGBoost, LabelEncoder)
├── static/             # CSS, JS, and image assets
├── templates/          # HTML templates (Jinja2)
├── app.py              # Main Flask application entry point
├── config.py           # Configuration management
├── create_admin.py     # Script to initialize/update admin credentials
└── requirements.txt    # Project dependencies
```

---

## 🚦 Usage

### Running the Application
```bash
python app.py
```
Access the dashboard at `http://127.0.0.1:5000`

### Training the Model (Optional)
If you wish to retrain the model with new data:
```bash
python ml/train_model.py
```

---

## 🛡️ Security
This project implements:
- **Password Hashing**: Using `PBKDF2` with SHA256.
- **Session Management**: Secure server-side session handling.
- **Input Validation**: Sanitized transaction inputs to prevent injection attacks.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
