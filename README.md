# MILK MANAGEMENT SYSTEM  

This is a **Django-based** Milk Management System for tracking milk records and generating invoices.  

## 🚀 Features  
- Add and manage customers  
- Record daily milk collection  
- Calculate milk price based on fat percentage and quantity  
- Generate invoices for customers  
- Uses **PostgreSQL** as the database  

## 🛠️ Installation  

1. **Clone the repository**  
   ```sh
   git clone https://github.com/THURAKA-ANANTH/MILK_MANAGMENT_SYSTEM.git
   cd MILK_MANAGMENT_SYSTEM
   ```

2. **Create a virtual environment & activate it**  
   ```sh
   python -m venv venv  
   source venv/bin/activate  # macOS/Linux  
   venv\Scripts\activate     # Windows  
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply database migrations**  
   ```sh
   python manage.py migrate
   ```

5. **Create a Super Admin**  
   ```sh
   python manage.py createsuperuser
   ```
   - Enter a **username**, **email**, and **password** when prompted.  
   - This account will be used to log into the Django admin panel.  

6. **Run the development server**  
   ```sh
   python manage.py runserver
   ```

7. **Access the application**  
   Open your browser and go to:  
   ```
   http://127.0.0.1:8000/
   ```
   
8. **Log into the Admin Panel**  
   Open the admin panel at:  
   ```
   http://127.0.0.1:8000/admin/
   ```
   - Use the super admin credentials you created earlier to log in.  


## 👤 Author  
**THURAKA-ANANTH**  
- GitHub: [THURAKA-ANANTH](https://github.com/THURAKA-ANANTH)  

## ⚖️ License  
This project is licensed under the **MIT License**.  
