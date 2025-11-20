# Tutorial Feature Setup Guide

## Installation

To enable the tutorial feature, install the markdown package:

```bash
pip install markdown==3.7
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Features Added

1. **Tutorial Button in Navigation** - Rose-pink themed button in the navbar
2. **Hero Section Link** - "Need Help? View Tutorial Guide" link in hero section
3. **Floating Tutorial Button** - Fixed position button with pulse animation (bottom-right)
4. **Tutorial Page** - Full tutorial page at `/tutorial/` with rose-pink theme

## Usage

- Visit the home page at `/`
- Click any of the tutorial buttons to access the guide
- Tutorial page displays the USER_TUTORIAL.md content in a beautiful format

## Styling

All tutorial elements use the rose-pink theme:
- Primary Rose: #e11d8f
- Secondary Pink: #f472b6
- Accent Rose: #f43f5e

The floating button includes:
- Pulse animation
- Hover effects
- Responsive design
- Icon from Lucide Icons
