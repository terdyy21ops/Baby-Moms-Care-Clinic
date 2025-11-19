# Mother Dashboard Visual Design Guide

## 🎨 Color Palette

### Primary Colors
```
Rose Pink:     #EC4899  ████████
Deep Rose:     #DB2777  ████████
Light Pink:    #F9A8D4  ████████
Soft Pink:     #FBCFE8  ████████
Pale Pink:     #FDF2F8  ████████
```

### Accent Colors
```
Amber:         #F59E0B  ████████  (Pending Status)
Green:         #10B981  ████████  (Approved/Completed)
Blue:          #3B82F6  ████████  (Info)
Purple:        #A855F7  ████████  (Actions)
Red:           #EF4444  ████████  (Cancelled/Delete)
```

### Neutral Colors
```
Slate 800:     #1E293B  ████████  (Headers)
Slate 700:     #334155  ████████  (Labels)
Slate 600:     #475569  ████████  (Body Text)
Slate 500:     #64748B  ████████  (Secondary Text)
White:         #FFFFFF  ████████  (Cards)
```

## 📐 Layout Structure

### Dashboard Layout
```
┌─────────────────────────────────────────────────┐
│  Welcome Header (Gradient Pink Background)      │
│  "Welcome Back, Name! 💕"                       │
│  Large Heart Icon                               │
└─────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│ Upcoming │ Pending  │Completed │ Doctors  │
│   Icon   │   Icon   │   Icon   │   Icon   │
│    2     │    1     │    5     │    3     │
└──────────┴──────────┴──────────┴──────────┘

┌──────────────┬──────────────┬──────────────┐
│ Book Appt    │ View Doctors │ All Appts    │
│   Icon       │   Icon       │   Icon       │
│ Description  │ Description  │ Description  │
└──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────┐
│  Upcoming Appointments                          │
│  ┌───────────────────────────────────────────┐ │
│  │ Icon  Dr. Name                    [View]  │ │
│  │       Date & Time                         │ │
│  │       [Status Badge]                      │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Profile Layout
```
┌─────────────────────────────────────────────────┐
│  ┌────┐  Name (Gradient Text)                  │
│  │ 👤 │  Role Badge                             │
│  │ ✓  │  Email • Phone                          │
│  └────┘                                          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Profile Information                            │
│  ┌─────────────────┬─────────────────┐         │
│  │ First Name      │ Last Name       │         │
│  └─────────────────┴─────────────────┘         │
│  ┌─────────────────────────────────────┐       │
│  │ 📧 Email                            │       │
│  └─────────────────────────────────────┘       │
│  [Save Changes]  [Cancel]                      │
└─────────────────────────────────────────────────┘
```

### Notifications Layout
```
┌─────────────────────────────────────────────────┐
│  Notifications 🔔                               │
│  Large Bell Icon                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  5 notifications  [Mark All Read]              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  ┌────┐  Title • Unread Dot                    │
│  │ 📅 │  Message text here...                   │
│  └────┘  Time ago • Type Badge  [Mark Read]    │
└─────────────────────────────────────────────────┘
```

## 🎯 Component Specifications

### Stat Card
```
Size: Full width on mobile, 1/4 on desktop
Padding: 24px (p-6)
Border Radius: 16px (rounded-2xl)
Border: 2px solid gradient color
Shadow: Large (shadow-lg)
Hover: Lift 4px + shadow-xl

Icon Badge:
  Size: 56px × 56px (w-14 h-14)
  Border Radius: 16px (rounded-2xl)
  Gradient: from-[color]-400 to-[color]-500
  Shadow: Medium (shadow-md)

Number:
  Size: 36px (text-4xl)
  Weight: Bold
  Color: Gradient or solid accent

Label:
  Size: 14px (text-sm)
  Weight: Semibold
  Color: Slate-700
```

### Action Card
```
Size: Full width on mobile, 1/3 on desktop
Padding: 32px (p-8)
Border Radius: 16px (rounded-2xl)
Background: White with glassmorphism
Border: 1px solid pink-100
Shadow: Large (shadow-lg)
Hover: Lift 4px + shadow-xl

Icon Badge:
  Size: 64px × 64px (w-16 h-16)
  Border Radius: 16px (rounded-2xl)
  Gradient: from-[color]-500 to-[color]-600
  Shadow: Large (shadow-lg)
  Hover: Scale 110%

Arrow Icon:
  Size: 24px (w-6 h-6)
  Color: Accent color
  Hover: Translate right 8px

Title:
  Size: 20px (text-xl)
  Weight: Bold
  Color: Slate-800

Description:
  Size: 14px (text-sm)
  Color: Slate-600
```

### Appointment Card
```
Size: Full width
Padding: 20px (p-5)
Border Radius: 16px (rounded-2xl)
Background: Gradient from white to pink-50
Border: 1px solid pink-100
Hover: Border pink-300 + shadow-md

Icon Badge:
  Size: 56px × 56px (w-14 h-14)
  Border Radius: 16px (rounded-2xl)
  Gradient: from-pink-400 to-rose-500
  Shadow: Medium (shadow-md)

Doctor Name:
  Size: 18px (text-lg)
  Weight: Bold
  Color: Slate-800

Date/Time:
  Size: 14px (text-sm)
  Color: Slate-600
  Icons: 16px (w-4 h-4)

Status Badge:
  Padding: 8px 12px (px-3 py-1)
  Border Radius: Full (rounded-full)
  Size: 12px (text-xs)
  Weight: Semibold
  Border: 1px solid matching color

Button:
  Padding: 12px 24px (px-6 py-3)
  Border Radius: 12px (rounded-xl)
  Gradient: from-pink-500 to-rose-600
  Shadow: Medium (shadow-md)
  Hover: Darker gradient + shadow-lg
```

### Input Field
```
Height: 48px (py-3)
Padding: 16px (px-4)
Border Radius: 12px (rounded-xl)
Border: 2px solid #FBCFE8
Background: rgba(255, 255, 255, 0.9)

Focus State:
  Border: 2px solid #EC4899
  Shadow: 0 0 0 3px rgba(236, 72, 153, 0.1)
  Outline: None

With Icon:
  Padding Left: 48px (pl-12)
  Icon Size: 20px (w-5 h-5)
  Icon Color: Pink-400
  Icon Position: Left 16px
```

### Button Styles
```
Primary (Gradient):
  Background: from-pink-500 to-rose-600
  Text: White
  Padding: 16px 24px (px-6 py-4)
  Border Radius: 12px (rounded-xl)
  Font: Bold, 18px (text-lg)
  Shadow: Large (shadow-lg)
  Hover: Darker gradient + shadow-xl

Secondary (Solid):
  Background: Slate-200
  Text: Slate-700
  Padding: 16px 24px (px-6 py-4)
  Border Radius: 12px (rounded-xl)
  Font: Bold, 18px (text-lg)
  Hover: Slate-300

Small Button:
  Padding: 8px 16px (px-4 py-2)
  Font: Semibold, 14px (text-sm)
  Border Radius: 8px (rounded-lg)
```

## 🎭 Animation Specifications

### Hover Effects
```css
/* Card Lift */
transform: translateY(-4px);
transition: all 0.3s ease;

/* Icon Scale */
transform: scale(1.1);
transition: transform 0.3s ease;

/* Arrow Slide */
transform: translateX(8px);
transition: transform 0.3s ease;

/* Shadow Grow */
box-shadow: 0 20px 40px rgba(236, 72, 153, 0.15);
transition: box-shadow 0.3s ease;
```

### Loading States
```css
/* Pulse Animation */
animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;

/* Fade In */
animation: fadeIn 0.5s ease-in;

/* Slide Up */
animation: slideUp 0.5s ease-out;
```

## 📱 Responsive Breakpoints

```css
/* Mobile First */
Default: Full width, single column

/* Tablet (768px+) */
md: 2 columns for stats, actions
    Horizontal layout for profile header

/* Desktop (1024px+) */
lg: 4 columns for stats
    3 columns for actions
    Side-by-side forms

/* Large Desktop (1280px+) */
xl: Max width 1280px
    Centered content
```

## 🎨 Gradient Recipes

### Background Gradients
```css
/* Page Background */
background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 50%, #fbcfe8 100%);

/* Card Header */
background: linear-gradient(to right, #fdf2f8, #fce7f3);

/* Stat Card */
background: linear-gradient(135deg, #fff 0%, #fdf2f8 100%);
```

### Button Gradients
```css
/* Primary */
background: linear-gradient(to right, #ec4899, #db2777);

/* Hover */
background: linear-gradient(to right, #db2777, #be185d);

/* Icon Badge */
background: linear-gradient(to bottom right, #f9a8d4, #ec4899);
```

### Text Gradients
```css
/* Title */
background: linear-gradient(to right, #db2777, #ec4899);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

## 🔤 Typography Scale

```
Hero:        text-4xl (36px) - font-bold
Title:       text-3xl (30px) - font-bold
Heading:     text-2xl (24px) - font-bold
Subheading:  text-xl (20px) - font-bold
Large:       text-lg (18px) - font-semibold
Body:        text-base (16px) - font-normal
Small:       text-sm (14px) - font-medium
Tiny:        text-xs (12px) - font-semibold
```

## 📏 Spacing Scale

```
Tight:   space-y-2  (8px)
Normal:  space-y-4  (16px)
Relaxed: space-y-6  (24px)
Loose:   space-y-8  (32px)

Card Padding:    p-6 to p-8  (24-32px)
Section Margin:  mb-6 to mb-8 (24-32px)
Grid Gap:        gap-4 to gap-6 (16-24px)
```

## 🎯 Icon Sizes

```
Tiny:    w-4 h-4   (16px)  - Inline icons
Small:   w-5 h-5   (20px)  - Input prefixes
Medium:  w-6 h-6   (24px)  - Buttons
Large:   w-8 h-8   (32px)  - Action cards
XLarge:  w-10 h-10 (40px)  - Headers
Huge:    w-12 h-12 (48px)  - Empty states
```

## 🎨 Shadow Scale

```
Small:   shadow-sm   - Subtle depth
Medium:  shadow-md   - Standard cards
Large:   shadow-lg   - Important cards
XLarge:  shadow-xl   - Floating elements
2XLarge: shadow-2xl  - Modals
```

## ✨ Special Effects

### Glassmorphism
```css
background: rgba(255, 255, 255, 0.95);
backdrop-filter: blur(10px);
border: 1px solid rgba(236, 72, 153, 0.1);
```

### Unread Glow
```css
background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
border-left: 4px solid #f59e0b;
```

### Status Badges
```css
/* Pending */
background: #FEF3C7;
color: #92400E;
border: 1px solid #FDE68A;

/* Approved */
background: #D1FAE5;
color: #065F46;
border: 1px solid #A7F3D0;

/* Completed */
background: #DBEAFE;
color: #1E40AF;
border: 1px solid #BFDBFE;

/* Cancelled */
background: #FEE2E2;
color: #991B1B;
border: 1px solid #FECACA;
```

## 🎉 Result

A cohesive, beautiful design system that creates a delightful user experience for mothers using the Baby Moms Care platform! 🌸💕
