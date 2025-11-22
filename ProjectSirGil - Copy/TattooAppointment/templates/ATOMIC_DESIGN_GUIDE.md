# Atomic Design Template Structure Guide

## 📁 Directory Structure

```
ProjectSirGil - Copy/TattooAppointment/
├── templates/                          # Project-level templates (NEW)
│   ├── base.html                      # Base template for all pages
│   ├── atoms/                         # Basic building blocks
│   │   ├── button.html               # Button component
│   │   ├── input.html                # Input field component
│   │   ├── textarea.html             # Textarea component
│   │   ├── label.html                # Label component
│   │   └── badge.html                # Badge/status component
│   ├── molecules/                     # Simple component groups
│   │   ├── form-field.html           # Complete form field (label + input + error)
│   │   ├── info-row.html             # Information display row
│   │   ├── stat-card.html            # Statistics card
│   │   └── nav-link.html             # Navigation link item
│   ├── organisms/                     # Complex UI components
│   │   ├── navbar.html               # Navigation bar
│   │   ├── appointment-card.html     # Appointment display card
│   │   ├── appointment-form.html     # Complete appointment form
│   │   └── stats-grid.html           # Statistics grid layout
│   └── pages/                         # Complete page templates
│       └── appointment-list-example.html  # Example implementation
│
└── appointments/templates/appointments/   # App-specific templates (EXISTING)
    ├── appointment_list.html          # Can be refactored to use atomic components
    ├── index.html
    ├── landing.html
    ├── login.html
    └── ...other templates
```

## 🎯 Atomic Design Methodology

### 🔹 Atoms (Basic Building Blocks)
**Location:** `templates/atoms/`

The smallest, indivisible components. Cannot be broken down further.

**Files:**
- `button.html` - Reusable button with multiple variants
- `input.html` - Form input field
- `textarea.html` - Multi-line text input
- `label.html` - Form label
- `badge.html` - Status badge

**Example Usage:**
```django
{% include 'atoms/button.html' with text='Submit' type='primary' %}
{% include 'atoms/input.html' with name='email' type='email' placeholder='Email' %}
{% include 'atoms/badge.html' with text='Approved' type='success' icon='✅' %}
```

### 🔸 Molecules (Simple Component Groups)
**Location:** `templates/molecules/`

Groups of atoms functioning together as a unit.

**Files:**
- `form-field.html` - Complete form field (label + input + error + help text)
- `info-row.html` - Information display with icon, label, and value
- `stat-card.html` - Statistics display card
- `nav-link.html` - Navigation link item

**Example Usage:**
```django
{% include 'molecules/form-field.html' with
    label='Email Address'
    name='email'
    type='email'
    placeholder='you@example.com'
    required=True
    help_text='We will never share your email'
%}

{% include 'molecules/info-row.html' with
    icon='📧'
    label='Email'
    value=appointment.email
%}
```

### 🔶 Organisms (Complex Components)
**Location:** `templates/organisms/`

Complex UI components composed of molecules and/or atoms.

**Files:**
- `navbar.html` - Complete navigation bar with authentication states
- `appointment-card.html` - Full appointment display card
- `appointment-form.html` - Complete appointment booking form
- `stats-grid.html` - Dashboard statistics grid

**Example Usage:**
```django
{% include 'organisms/navbar.html' %}

{% include 'organisms/appointment-card.html' with
    appointment=appointment
    show_actions=True
    edit_url=edit_url
    delete_url=delete_url
%}

{% include 'organisms/stats-grid.html' with stats=stats %}
```

### 📄 Pages (Complete Views)
**Location:** `templates/pages/`

Complete page templates that arrange organisms into layouts.

**Example Usage:**
```django
{% extends 'base.html' %}

{% block content %}
    {% include 'organisms/stats-grid.html' with stats=stats %}
    {% include 'organisms/appointment-card.html' with appointment=appointment %}
{% endblock %}
```

## 🔄 Migrating Existing Templates

### Before (Old Structure):
```django
{# appointments/templates/appointments/appointment_list.html #}
{% extends 'appointments/base.html' %}

{% block content %}
<div class="appointments-container">
    {% for appointment in appointments %}
    <div class="appointment-card {{ appointment.status }}">
        <div class="status-badge status-{{ appointment.status }}">
            {{ appointment.get_status_display }}
        </div>
        <div class="client-name">{{ appointment.client_name }}</div>
        <div class="info-row">
            <span>📧</span>
            <span>Email:</span>
            <span>{{ appointment.email }}</span>
        </div>
        {# ...more code... #}
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### After (Atomic Design):
```django
{# appointments/templates/appointments/appointment_list.html #}
{% extends 'base.html' %}

{% block content %}
<div class="container">
    {# Statistics #}
    {% include 'organisms/stats-grid.html' with stats=stats %}

    {# Appointments Grid #}
    <div class="appointments-grid">
        {% for appointment in appointments %}
            {% include 'organisms/appointment-card.html' with
                appointment=appointment
                show_actions=user.is_staff
            %}
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## 📝 Migration Steps for Existing Templates

### Step 1: Update Base Template Inheritance
Change from app-specific base to project-level base:

```django
{# OLD #}
{% extends 'appointments/base.html' %}

{# NEW #}
{% extends 'base.html' %}
```

### Step 2: Replace Inline HTML with Component Includes
Identify repeated patterns and replace with atomic components:

```django
{# OLD - Inline HTML #}
<div class="appointment-card">
    <h3>{{ appointment.client_name }}</h3>
    <p>{{ appointment.email }}</p>
    {# ...lots of HTML... #}
</div>

{# NEW - Component Include #}
{% include 'organisms/appointment-card.html' with appointment=appointment %}
```

### Step 3: Refactor Forms
Replace form HTML with form components:

```django
{# OLD #}
<div class="form-field">
    <label for="email">Email *</label>
    <input type="email" name="email" id="email" required>
</div>

{# NEW #}
{% include 'molecules/form-field.html' with
    label='Email'
    name='email'
    type='email'
    required=True
%}
```

## 🎨 Django Template Syntax Essentials

### {% include %} - Include a Component
Use `{% include %}` to insert reusable components:

```django
{# Basic include #}
{% include 'atoms/button.html' %}

{# Include with parameters #}
{% include 'atoms/button.html' with text='Submit' type='primary' %}

{# Include with multiple parameters #}
{% include 'molecules/form-field.html' with
    label='Email Address'
    name='email'
    type='email'
    required=True
    help_text='We will never share your email'
%}
```

### {% extends %} - Template Inheritance
Use `{% extends %}` to inherit from a base template:

```django
{# Extend the project base template #}
{% extends 'base.html' %}

{# Override blocks #}
{% block title %}My Custom Title{% endblock %}

{% block content %}
    {# Your page content here #}
{% endblock %}
```

### Common Blocks in base.html

```django
{% block title %}         - Page title
{% block extra_css %}     - Additional CSS files
{% block body_class %}    - Body CSS classes
{% block content %}       - Main page content
{% block footer %}        - Footer content
{% block extra_js %}      - Additional JavaScript
```

## 📋 File Path Reference

### Exact File Paths

**Project-Level Templates:**
```
ProjectSirGil - Copy/TattooAppointment/templates/base.html
ProjectSirGil - Copy/TattooAppointment/templates/atoms/button.html
ProjectSirGil - Copy/TattooAppointment/templates/atoms/input.html
ProjectSirGil - Copy/TattooAppointment/templates/atoms/textarea.html
ProjectSirGil - Copy/TattooAppointment/templates/atoms/label.html
ProjectSirGil - Copy/TattooAppointment/templates/atoms/badge.html
ProjectSirGil - Copy/TattooAppointment/templates/molecules/form-field.html
ProjectSirGil - Copy/TattooAppointment/templates/molecules/info-row.html
ProjectSirGil - Copy/TattooAppointment/templates/molecules/stat-card.html
ProjectSirGil - Copy/TattooAppointment/templates/molecules/nav-link.html
ProjectSirGil - Copy/TattooAppointment/templates/organisms/navbar.html
ProjectSirGil - Copy/TattooAppointment/templates/organisms/appointment-card.html
ProjectSirGil - Copy/TattooAppointment/templates/organisms/appointment-form.html
ProjectSirGil - Copy/TattooAppointment/templates/organisms/stats-grid.html
ProjectSirGil - Copy/TattooAppointment/templates/pages/appointment-list-example.html
```

**App-Specific Templates (to be refactored):**
```
ProjectSirGil - Copy/TattooAppointment/appointments/templates/appointments/appointment_list.html
ProjectSirGil - Copy/TattooAppointment/appointments/templates/appointments/index.html
ProjectSirGil - Copy/TattooAppointment/appointments/templates/appointments/create_appointment.html
ProjectSirGil - Copy/TattooAppointment/appointments/templates/appointments/login.html
ProjectSirGil - Copy/TattooAppointment/appointments/templates/appointments/register.html
```

## ✅ Django Settings Configuration

Your `settings.py` is already configured correctly:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Project-level templates
        'APP_DIRS': True,                  # ✅ App-level templates still work
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**How it works:**
- Django first looks in `DIRS` (`templates/`) for templates
- Then it looks in each app's `templates/` directory (`appointments/templates/`)
- Both locations work simultaneously - no conflicts!

## 🚀 Quick Start: Refactoring Your First Template

### Example: Refactor `appointment_list.html`

**1. Create new file or update existing:**
```
appointments/templates/appointments/appointment_list.html
```

**2. Update the template:**
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}My Appointments{% endblock %}

{% block extra_css %}
<style>
    .appointments-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 25px;
        padding: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <h1>My Appointments</h1>

    {# Use the stats organism #}
    {% if stats %}
        {% include 'organisms/stats-grid.html' with stats=stats %}
    {% endif %}

    {# Use the appointment card organism #}
    <div class="appointments-grid">
        {% for appointment in appointments %}
            {% include 'organisms/appointment-card.html' with
                appointment=appointment
                show_actions=user.is_staff
                edit_url=appointment.get_edit_url
                delete_url=appointment.get_delete_url
            %}
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## 💡 Best Practices

1. **Keep Atoms Simple**: Atoms should be generic and reusable
2. **Make Molecules Flexible**: Use template variables for customization
3. **Document Parameters**: Always document what parameters a component expects
4. **Use Consistent Naming**: Follow the existing naming conventions
5. **Test Responsiveness**: Ensure components work on all screen sizes
6. **Avoid Over-Abstraction**: Don't create atomic components for one-time use
7. **Maintain Backwards Compatibility**: Old templates can coexist with new ones

## 🔗 Component Parameter Reference

### Atoms

#### button.html
- `text` (string): Button text
- `type` (string): primary, secondary, danger, success, outline
- `url` (string): Link URL (creates <a> tag)
- `button_type` (string): submit, button, reset
- `icon` (string): Icon to display
- `disabled` (boolean): Disable button
- `class` (string): Additional CSS classes

#### input.html
- `name` (string): Input name attribute
- `type` (string): text, email, password, number, tel, date
- `placeholder` (string): Placeholder text
- `value` (string): Input value
- `required` (boolean): Required field
- `disabled` (boolean): Disable input

### Molecules

#### form-field.html
- `label` (string): Field label
- `name` (string): Input name
- `type` (string): Input type
- `field_type` (string): 'textarea' for textarea input
- `placeholder` (string): Placeholder text
- `value` (string): Field value
- `required` (boolean): Required field
- `error` (string): Error message
- `help_text` (string): Help text below input

### Organisms

#### appointment-card.html
- `appointment` (object): Appointment model instance
- `show_actions` (boolean): Show edit/delete buttons
- `edit_url` (string): Edit URL
- `delete_url` (string): Delete URL

## 📚 Additional Resources

- [Atomic Design by Brad Frost](https://bradfrost.com/blog/post/atomic-web-design/)
- [Django Template Documentation](https://docs.djangoproject.com/en/5.2/topics/templates/)
- [Template Inheritance](https://docs.djangoproject.com/en/5.2/ref/templates/language/#template-inheritance)
- [Include Tag Documentation](https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#include)

---

**Happy Coding! 💀🎨**
