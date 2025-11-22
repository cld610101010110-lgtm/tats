# Atomic Design Quick Reference

## 📋 Template Structure at a Glance

```
ProjectSirGil - Copy/TattooAppointment/
│
├── templates/                                    # PROJECT-LEVEL (New Atomic Design)
│   ├── base.html                                # Base template - extend this!
│   ├── ATOMIC_DESIGN_GUIDE.md                   # Full documentation
│   │
│   ├── atoms/                                   # 🔹 Smallest components
│   │   ├── button.html
│   │   ├── input.html
│   │   ├── textarea.html
│   │   ├── label.html
│   │   └── badge.html
│   │
│   ├── molecules/                               # 🔸 Component groups
│   │   ├── form-field.html
│   │   ├── info-row.html
│   │   ├── stat-card.html
│   │   └── nav-link.html
│   │
│   ├── organisms/                               # 🔶 Complex components
│   │   ├── navbar.html
│   │   ├── appointment-card.html
│   │   ├── appointment-form.html
│   │   └── stats-grid.html
│   │
│   └── pages/                                   # 📄 Complete pages
│       └── appointment-list-example.html
│
└── appointments/templates/appointments/          # APP-LEVEL (Existing templates)
    ├── appointment_list.html                    # ← Refactor this!
    ├── index.html
    ├── login.html
    └── ...other existing templates
```

## 🚀 Quick Start: 3 Steps to Refactor

### Step 1: Change Base Template
```django
{# OLD #}
{% extends 'appointments/base.html' %}

{# NEW #}
{% extends 'base.html' %}
```

### Step 2: Use Atomic Components
```django
{# OLD - Inline HTML #}
<div class="appointment-card">
    <h3>{{ appointment.client_name }}</h3>
    <span class="badge">{{ appointment.status }}</span>
    <!-- ...100 lines of HTML... -->
</div>

{# NEW - One line! #}
{% include 'organisms/appointment-card.html' with appointment=appointment %}
```

### Step 3: Profit!
Your template went from 200 lines → 20 lines ✨

## 💡 Most Common Components

### Display an Appointment Card
```django
{% include 'organisms/appointment-card.html' with
    appointment=appointment
    show_actions=True
%}
```

### Display Statistics
```django
{% include 'organisms/stats-grid.html' with stats=stats %}
```

### Create a Form Field
```django
{% include 'molecules/form-field.html' with
    label='Email'
    name='email'
    type='email'
    required=True
%}
```

### Add a Button
```django
{% include 'atoms/button.html' with
    text='Submit'
    type='primary'
    button_type='submit'
%}
```

## 📖 Component Parameters Cheat Sheet

### atoms/button.html
| Parameter | Type | Options |
|-----------|------|---------|
| text | string | Button text |
| type | string | primary, secondary, danger, success, outline |
| url | string | Link URL (optional) |
| icon | string | Icon emoji/text |

### molecules/form-field.html
| Parameter | Type | Description |
|-----------|------|-------------|
| label | string | Field label |
| name | string | Input name |
| type | string | text, email, password, tel, date |
| field_type | string | 'textarea' for textarea |
| required | boolean | Required field |
| help_text | string | Help text below input |

### organisms/appointment-card.html
| Parameter | Type | Description |
|-----------|------|-------------|
| appointment | object | Appointment model instance |
| show_actions | boolean | Show edit/delete buttons |
| edit_url | string | Edit URL (if show_actions=True) |
| delete_url | string | Delete URL (if show_actions=True) |

### organisms/stats-grid.html
| Parameter | Type | Description |
|-----------|------|-------------|
| stats | dict | Stats object with total, pending, approved, rejected |

**Stats object structure:**
```python
stats = {
    'total': 10,
    'pending': 3,
    'approved': 5,
    'rejected': 2,
    'next_session': datetime_object  # optional
}
```

## 🎯 Before & After Examples

### Example 1: Appointment List Page

**BEFORE (appointments/appointment_list.html):**
```django
{% extends 'appointments/base.html' %}

{% block content %}
<div class="appointments-container">
    {% for appointment in appointments %}
    <div class="appointment-card {{ appointment.status }}">
        <div class="status-badge">{{ appointment.get_status_display }}</div>
        <h3>{{ appointment.client_name }}</h3>
        <div class="info-row">
            <span class="icon">📧</span>
            <span class="label">Email:</span>
            <span class="value">{{ appointment.email }}</span>
        </div>
        <div class="info-row">
            <span class="icon">📱</span>
            <span class="label">Phone:</span>
            <span class="value">{{ appointment.phone }}</span>
        </div>
        <div class="tattoo-design">{{ appointment.tattoo_design }}</div>
        {% if user.is_staff %}
            <a href="{% url 'appointments:edit' appointment.pk %}">Edit</a>
            <a href="{% url 'appointments:delete' appointment.pk %}">Delete</a>
        {% endif %}
    </div>
    {% endfor %}
</div>
{% endblock %}
```

**AFTER (Using Atomic Design):**
```django
{% extends 'base.html' %}

{% block content %}
<div class="container">
    {% include 'organisms/stats-grid.html' with stats=stats %}

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

### Example 2: Create Appointment Form

**BEFORE:**
```django
<form method="POST">
    {% csrf_token %}
    <div class="form-group">
        <label for="client_name">Name *</label>
        <input type="text" name="client_name" required>
    </div>
    <div class="form-group">
        <label for="email">Email *</label>
        <input type="email" name="email" required>
    </div>
    <!-- ...20 more lines... -->
    <button type="submit">Submit</button>
</form>
```

**AFTER:**
```django
{% include 'organisms/appointment-form.html' with form=form %}
```

## ✅ Checklist for Refactoring a Template

- [ ] Change `{% extends 'appointments/base.html' %}` to `{% extends 'base.html' %}`
- [ ] Replace status badges with `{% include 'atoms/badge.html' %}`
- [ ] Replace buttons with `{% include 'atoms/button.html' %}`
- [ ] Replace form fields with `{% include 'molecules/form-field.html' %}`
- [ ] Replace appointment cards with `{% include 'organisms/appointment-card.html' %}`
- [ ] Replace stats sections with `{% include 'organisms/stats-grid.html' %}`
- [ ] Test the page to ensure everything works
- [ ] Remove old CSS that's now in the atomic components

## 🔗 File Locations

**Atomic components:** `templates/atoms/`, `templates/molecules/`, `templates/organisms/`
**Your app templates:** `appointments/templates/appointments/`
**Base template:** `templates/base.html`
**Documentation:** `templates/ATOMIC_DESIGN_GUIDE.md`

## 📞 Need Help?

See `ATOMIC_DESIGN_GUIDE.md` for:
- Complete documentation
- Migration guides
- Parameter reference
- Best practices
- Django template syntax guide

---

**Remember:** Your existing templates still work! The atomic structure is additive, not destructive. Refactor at your own pace. 🎨
