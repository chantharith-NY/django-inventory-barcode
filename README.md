##Django Inventory Management System

This project is a Django-based Inventory Management System that allows users to manage items using barcode scanning. Users can borrow and return items by scanning their barcodes. This system is designed to simplify inventory tracking and enhance efficiency.

###Features
- Barcode Scanning: Users can scan barcodes to borrow or return items.
- Item Management: Add, update, and delete items in the inventory.
- User Management: Manage user accounts and permissions.
- Transaction History: Track borrowing and returning transactions.

###Requirements
- Python 3.8+
- Django 4.2+
- A barcode scanner (optional for hardware integration)
- Database (MySQL)

###Installation
1. Clone the Repository

`git clone git@github.com:<username>/django-inventory-barcode.git`
`cd django-inventory-barcode`

2. Set Up a Virtual Environment

`python -m venv venv`
- On MacOS:
`source venv/bin/activate`  
- On Windows: 
`venv\Scripts\activate`

3. Install Dependencies

`pip install -r requirements.txt`

4. Run Migrations

`python manage.py migrate`

5. Create a Superuser

`python manage.py createsuperuser`
Follow the prompts to set up an admin account.

6. Run the Development Server

`python manage.py runserver`

7. Access the Application
Open your browser and go to http://127.0.0.1:8000.

###Usage

1. Log in using your admin or user credentials.
2. Add items to the inventory through the admin panel or the UI.
3. Use the barcode scanner to borrow or return items:
    - Scan an item's barcode to borrow it.
    - Scan the same item's barcode again to return it.
4. View transaction history and manage inventory from the dashboard.

###Technologies Used
- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Barcode: python-barcode or external hardware integration

###Folder Structure

`django-inventory-barcode/
`├── inventory_management/      # Django project folder
`├── inventory/                 # Inventory app for managing items
`├── templates/                 # HTML templates
`├── static/                    # Static files (CSS, JS, images)
`├── manage.py                  # Django management script
`├── requirements.txt           # Dependencies
`└── README.md                  # Project description

###Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with descriptive messages.
4. Push your branch to your fork and create a pull request.
