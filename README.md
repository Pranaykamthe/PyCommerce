# PyCommerce

A console-based **E-Commerce Management System** built with **Python, OOP, and MySQL** using a layered architecture.

## Features

### Customer

* Registration & authentication
* Product browsing and categories
* Shopping cart
* Wishlist
* Checkout & orders
* Payment processing/simulation
* Product reviews
* PDF receipt/invoice generation

### Admin

* Product management
* Category management
* User management
* Order management
* Payment management

## Tech Stack

* **Python** – Application development
* **MySQL** – Database
* **mysql-connector-python** – Database connectivity
* **pytest** – Automated testing
* **Rich / Tabulate** – Console UI
* **ReportLab** – PDF receipts
* **python-dotenv** – Configuration
* **Git & GitHub** – Version control

## Architecture

PyCommerce follows a layered architecture:

```text
User Interface
      ↓
Services
(Business Logic)
      ↓
Repositories
(Data Access)
      ↓
Models
      ↓
MySQL Database
```

This separation keeps the application maintainable, testable, and easy to extend.

## Project Structure

```text
PyCommerce/
├── config/
├── database/
├── models/
├── repositories/
├── services/
├── ui/
├── utils/
├── receipts/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Database

The application uses MySQL with tables for:

```text
users
categories
products
cart
orders
order_items
payments
reviews
wishlist
```

Database configuration is provided through environment variables:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pycommerce
```

> Never commit `.env` or database credentials to GitHub.

Initialize the database:

```powershell
python -m database.schema
```

## Installation & Usage

Clone the repository:

```bash
git clone <your-github-repository-url>
cd PyCommerce
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the application:

```powershell
python main.py
```

## Testing

PyCommerce uses **pytest** for automated testing.

```powershell
python -m pytest -v
```

Current test status:

```text
419 passed
0 failed
```

## Project Highlights

* Object-Oriented Python development
* Layered architecture
* Repository & Service patterns
* MySQL relational database design
* Authentication and authorization
* Cart, wishlist and order management
* Checkout and payment workflow
* PDF receipt generation
* Automated testing
* Git/GitHub based incremental development

## Future Improvements

* REST API
* Web-based frontend
* Real payment gateway integration
* Docker & CI/CD
* Cloud deployment
* Advanced product search and recommendations

## License

See the `LICENSE` file for license information.
