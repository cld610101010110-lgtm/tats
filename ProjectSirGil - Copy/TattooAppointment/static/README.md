# Modern Web Application Structure

This directory contains the static assets and frontend component structure for the Tattoo Appointment web application.

## Directory Structure

```
static/
├── css/                    # Stylesheets
├── images/                 # Static images and assets
├── js/                     # JavaScript files
├── fonts/                  # Custom fonts
└── templates/              # Frontend components (Atomic Design)
    ├── atoms/              # Basic building blocks
    ├── molecules/          # Simple component groups
    ├── organisms/          # Complex UI components
    ├── templates/          # Page-level layouts
    └── pages/              # Complete page views
```

## Atomic Design Methodology

This project uses [Atomic Design](https://bradfrost.com/blog/post/atomic-web-design/) methodology for organizing UI components:

### 🔹 Atoms
Basic building blocks of the interface. These are the smallest, indivisible components.

**Examples:**
- Buttons
- Input fields
- Labels
- Icons
- Typography elements

**Location:** `templates/atoms/`

### 🔸 Molecules
Simple groups of atoms functioning together as a unit.

**Examples:**
- Search bar (input + button)
- Form field (label + input + error message)
- Card header (title + subtitle)
- Navigation item (icon + text)

**Location:** `templates/molecules/`

### 🔶 Organisms
Complex UI components composed of molecules and/or atoms.

**Examples:**
- Navigation bar
- Appointment card
- Artist profile section
- Footer
- Header with logo and navigation

**Location:** `templates/organisms/`

### 📄 Templates
Page-level layouts that arrange organisms into a structure.

**Examples:**
- Base template with header/footer
- Two-column layout
- Dashboard layout
- Landing page layout

**Location:** `templates/templates/`

### 📑 Pages
Specific instances of templates with real content.

**Examples:**
- Home page
- Appointment booking page
- Artist gallery page
- User dashboard

**Location:** `templates/pages/`

## Usage Guidelines

### CSS Organization
```
css/
├── base/           # Reset, variables, mixins
├── components/     # Component-specific styles
├── layouts/        # Layout styles
├── utilities/      # Utility classes
└── main.css        # Main stylesheet
```

### JavaScript Organization
```
js/
├── components/     # Component scripts
├── utilities/      # Helper functions
├── vendor/         # Third-party libraries
└── main.js         # Main JavaScript file
```

## Best Practices

1. **Reusability**: Build components to be reusable across different contexts
2. **Modularity**: Keep components focused and single-purpose
3. **Consistency**: Use consistent naming conventions and patterns
4. **Documentation**: Document component props, usage, and variations
5. **Accessibility**: Ensure all components are accessible (ARIA labels, keyboard navigation)

## Naming Conventions

- **Files**: Use kebab-case (e.g., `button-primary.html`, `search-bar.html`)
- **CSS Classes**: Use BEM methodology (e.g., `.card__title--featured`)
- **JavaScript**: Use camelCase for variables and functions

## Integration with Django

To use these templates in Django:

```python
# In settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# In templates
{% load static %}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<script src="{% static 'js/main.js' %}"></script>
```

## Contributing

When adding new components:
1. Place them in the appropriate Atomic Design category
2. Document the component's purpose and usage
3. Ensure the component is responsive and accessible
4. Add corresponding CSS and JavaScript if needed
