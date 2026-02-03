# Student Expense Tracker 🚀

A modern, feature-rich expense tracking application built with Django and Django REST Framework, featuring a professional SaaS dashboard interface.

## ✨ Features

### 🎨 Modern UI/UX
- **SaaS Dashboard Design**: Professional sidebar navigation with glass-morphism header
- **Responsive Layout**: Mobile-friendly design that adapts to all screen sizes
- **Modern Components**: Stats cards, charts, and interactive elements
- **Fintech Aesthetic**: Deep navy, slate grey, and emerald green color scheme
- **Micro-interactions**: Smooth transitions and hover effects

### 💰 Expense Management
- **Add Expenses**: Quick expense entry with categories and descriptions
- **Track Spending**: Monitor expenses by category, date, and amount
- **Real-time Stats**: Live updates for total expenses, monthly totals, and entry counts
- **Currency Support**: Indian Rupees (₹) with proper formatting

### 🔍 Advanced Filtering
- **Category Filters**: Multi-select filtering by expense categories
- **Sorting Options**: By date, amount (high/low), and title (A-Z)
- **Date Ranges**: Last 7 days, last 30 days, or custom date ranges
- **Amount Ranges**: Filter by minimum and maximum amounts
- **Real-time Updates**: Instant filter application with visual feedback

### 👤 User Features
- **Authentication**: Secure login, registration, and logout
- **Profile Dropdown**: Quick access to profile, settings, and logout
- **User-specific Data**: Each user sees only their own expenses
- **Session Management**: Secure session-based authentication

### 📊 Dashboard Components
- **Stats Cards**: Total expenses, monthly totals, and entry counts
- **Spending Trends**: Chart placeholder for future visualizations
- **Recent Expenses**: List of latest expenses with delete functionality
- **Quick Add Form**: Compact expense entry form

## 🛠️ Technology Stack

- **Backend**: Django 6.0.1, Django REST Framework 3.16.1
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (development ready)
- **Authentication**: Django's built-in authentication system
- **API**: RESTful API with token and session authentication
- **Styling**: Custom CSS with Inter font and Lucide icons
- **CORS**: django-cors-headers for API security

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip and virtualenv

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Student_expense_tracker.git
   cd Student_expense_tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create default categories**
   ```bash
   python manage.py create_default_categories
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Register a new account or use the admin credentials

## 📁 Project Structure

```
Student_expense_tracker/
├── expense_tracker/          # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── expenses/               # Main Django app
│   ├── models.py          # Expense and Category models
│   ├── views.py           # API and view logic
│   ├── serializers.py     # REST API serializers
│   ├── urls.py            # App URL configuration
│   ├── admin.py           # Django admin configuration
│   ├── views_auth.py      # Authentication views
│   ├── templates/         # HTML templates
│   │   └── expenses/
│   │       ├── index.html # Main dashboard
│   │       ├── login.html # Login page
│   │       └── register.html # Registration page
│   └── management/        # Django management commands
│       └── commands/
│           └── create_default_categories.py
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout

### Categories (Public)
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Expenses (Authenticated)
- `GET /api/expenses/` - List user expenses (with filtering)
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/recent/` - Get recent expenses
- `GET /api/expenses/summary/` - Get expense statistics
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Database Settings
- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended (configure in settings.py)

## 🎨 Customization

### Adding New Categories
Edit the `create_default_categories.py` management command to add custom categories.

### Custom Styling
- Modify `expenses/templates/expenses/index.html` for UI changes
- Update CSS variables in the `<style>` section for theme customization

### API Extensions
- Add new endpoints in `expenses/urls.py`
- Implement view logic in `expenses/views.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Framework for the robust backend
- Django REST Framework for the API
- Lucide Icons for the beautiful icon set
- Google Fonts (Inter) for typography

## 📞 Support

For support, please open an issue in the GitHub repository or contact the project maintainer.

---

**Built with ❤️ using Django and modern web technologies**
