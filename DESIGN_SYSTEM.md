# Design System Documentation

## Overview

This document describes the comprehensive design system implemented for the Toy Robot Simulator. The design system provides a modern, accessible, and consistent user experience with support for dark/light themes, glassmorphism effects, and rich micro-interactions.

## Table of Contents

1. [Design Tokens](#design-tokens)
2. [Theme System](#theme-system)
3. [Glassmorphism](#glassmorphism)
4. [Micro-interactions](#micro-interactions)
5. [Custom Scrollbars](#custom-scrollbars)
6. [Components](#components)
7. [Accessibility](#accessibility)
8. [Usage Examples](#usage-examples)

---

## Design Tokens

Design tokens are the foundational building blocks of the design system. They ensure consistency across the application.

### Spacing Scale

Based on a 4px base unit (`--space-unit`):

```css
--space-0: 0
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-5: 20px
--space-6: 24px
--space-8: 32px
--space-10: 40px
--space-12: 48px
--space-16: 64px
--space-20: 80px
--space-24: 96px
```

### Typography Scale

#### Font Families
- **Base**: System font stack (San Francisco, Segoe UI, Roboto, etc.)
- **Mono**: Monospace fonts for code/output (SF Mono, Monaco, Fira Code, etc.)

#### Font Sizes
```css
--font-size-xs: 0.75rem (12px)
--font-size-sm: 0.875rem (14px)
--font-size-base: 1rem (16px)
--font-size-lg: 1.125rem (18px)
--font-size-xl: 1.25rem (20px)
--font-size-2xl: 1.5rem (24px)
--font-size-3xl: 1.875rem (30px)
--font-size-4xl: 2.25rem (36px)
--font-size-5xl: 3rem (48px)
```

#### Font Weights
```css
--font-weight-light: 300
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
--font-weight-extrabold: 800
```

### Color Palette

The design system includes comprehensive color palettes for:
- Primary (Blue)
- Success (Green)
- Danger (Red)
- Warning (Amber)
- Info (Cyan)
- Neutral/Gray
- Purple (for special buttons)
- Cyan (for report button)

Each color has 10 shades (50-900) for maximum flexibility.

#### Semantic Colors

**Light Theme:**
```css
--primary-color: Blue 600
--success-color: Green 500
--danger-color: Red 500
--warning-color: Amber 500
--bg-primary: Gray 50
--card-bg: rgba(255, 255, 255, 0.95)
--text-primary: Gray 900
```

**Dark Theme:**
```css
--primary-color: Blue 500
--success-color: Green 400
--danger-color: Red 400
--warning-color: Amber 400
--bg-primary: #0a0f1a
--card-bg: rgba(30, 41, 59, 0.7)
--text-primary: Gray 50
```

### Shadows

```css
--shadow-xs: Minimal shadow
--shadow-sm: Small shadow
--shadow-md: Medium shadow
--shadow-lg: Large shadow
--shadow-xl: Extra large shadow
--shadow-2xl: Massive shadow
--shadow-glass: Glassmorphism shadow
--shadow-primary: Colored primary shadow
```

### Border Radius

```css
--radius-sm: 4px
--radius-base: 6px
--radius-md: 8px
--radius-lg: 12px
--radius-xl: 16px
--radius-2xl: 24px
--radius-3xl: 32px
--radius-full: 9999px (perfect circle)
```

### Transitions

#### Timing Functions
```css
--ease-linear: linear
--ease-in: cubic-bezier(0.4, 0, 1, 1)
--ease-out: cubic-bezier(0, 0, 0.2, 1)
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55)
--ease-smooth: cubic-bezier(0.25, 0.46, 0.45, 0.94)
```

#### Durations
```css
--duration-instant: 75ms
--duration-fast: 150ms
--duration-base: 200ms
--duration-medium: 300ms
--duration-slow: 500ms
--duration-slower: 700ms
```

---

## Theme System

### Theme Toggle

The design system includes an automatic theme toggle button that:
- Appears in the top-right corner
- Remembers user preference in localStorage
- Respects system preference (`prefers-color-scheme`)
- Provides smooth transitions between themes
- Includes sun/moon icons with smooth animations

### Switching Themes

Themes are controlled via the `data-theme` attribute on the root element:

```html
<html data-theme="light">  <!-- Light theme -->
<html data-theme="dark">   <!-- Dark theme -->
```

The theme manager automatically handles:
- Theme persistence
- System preference detection
- Smooth transitions
- Accessibility updates

### Custom Theme Transitions

All theme-aware components use the `--transition-theme` variable:

```css
--transition-theme: background-color 300ms ease-smooth,
                   color 300ms ease-smooth,
                   border-color 300ms ease-smooth,
                   box-shadow 300ms ease-smooth;
```

---

## Glassmorphism

Glassmorphism creates a frosted-glass effect with transparency and blur.

### Base Glass Effect

```css
.glass {
    background: var(--card-bg);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: var(--shadow-glass);
}
```

### Glass Variants

**Light Glass:**
```css
.glass-light {
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(12px) saturate(150%);
}
```

**Medium Glass:**
```css
.glass-medium {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(16px) saturate(180%);
}
```

**Heavy Glass:**
```css
.glass-heavy {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(24px) saturate(200%);
}
```

### Applied Components

Glassmorphism is applied to:
- All section cards
- Grid container
- D-pad controller
- Toast notifications
- Loading overlay
- Theme toggle button

---

## Micro-interactions

### Button Ripple Effect

Enhanced ripple effect that activates on click:

```css
/* Automatically added to all .btn elements */
.btn:active::before {
    width: 400px;
    height: 400px;
    opacity: 1;
}
```

### Button Shine Effect

Animated shine effect on hover:

```css
.btn:hover::after {
    /* Animated shine sweeps across button */
    left: 100%;
}
```

### Hover Effects

**Lift on Hover:**
```css
.btn:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-lg);
}
```

**Glow Effect:**
```css
.btn-glow:hover::after {
    opacity: 0.4;
    box-shadow: 0 0 20px currentColor;
}
```

### Input Focus Effects

Enhanced focus states with animated rings:

```css
input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15),
                0 4px 12px rgba(37, 99, 235, 0.1);
    transform: translateY(-2px);
}
```

### Section Hover Effects

Sections lift and show animated border on hover:

```css
section:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
}

section:hover::before {
    /* Animated gradient line appears at top */
    opacity: 1;
}
```

---

## Custom Scrollbars

### Design

Scrollbars are styled to match the theme with:
- Gradient background on thumb
- Smooth transitions
- Hover effects
- Theme-aware colors

### Implementation

```css
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        var(--color-primary-400),
        var(--color-primary-600)
    );
    border-radius: var(--radius-md);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        180deg,
        var(--color-primary-500),
        var(--color-primary-700)
    );
}
```

Firefox support via `scrollbar-width` and `scrollbar-color`.

---

## Components

### Cards/Sections

All sections automatically include:
- Glassmorphism background
- Smooth theme transitions
- Hover lift effect
- Animated top border on hover
- Responsive padding

### Grid Container

Features:
- Glassmorphism effect
- Theme-aware cell backgrounds
- Hover scale animation on cells
- Smooth transitions

### D-Pad Controller

Features:
- Glassmorphism background
- Theme-aware styling
- Button press animations
- Pulsing center icon

### Toast Notifications

Features:
- Glassmorphism effect
- Slide-in animation
- Theme support
- Auto-dismiss
- Accessibility announcements

### Theme Toggle Button

Features:
- Fixed position (top-right)
- Animated slider with bounce effect
- Icon transitions (sun/moon)
- Smooth theme switching
- Remembers preference

---

## Accessibility

### Keyboard Support

- All interactive elements are keyboard accessible
- Focus states are clearly visible
- Theme toggle supports Enter and Space keys

### Screen Readers

- Proper ARIA labels on all controls
- Theme changes announced
- Live regions for dynamic content

### Motion Preferences

Respects `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

### High Contrast Mode

Supports `prefers-contrast: high`:

```css
@media (prefers-contrast: high) {
    .glass, .card-glass {
        border: 2px solid currentColor;
    }
}
```

---

## Usage Examples

### Using Design Tokens

```css
.my-component {
    padding: var(--space-4);
    margin-bottom: var(--space-6);
    font-size: var(--font-size-lg);
    color: var(--text-primary);
    border-radius: var(--radius-lg);
    transition: var(--transition-all);
}
```

### Creating a Glass Card

```html
<div class="card-glass">
    <h2>My Card</h2>
    <p>Content here</p>
</div>
```

### Adding Custom Animations

```css
.my-element {
    animation: pulse-glow 2s ease-in-out infinite;
}

/* Or apply existing utility classes */
<div class="bounce-click scale-hover">
    Click me!
</div>
```

### Theme-Aware Styling

```css
.my-component {
    background: var(--bg-secondary);
    color: var(--text-primary);
    transition: var(--transition-theme);
}

[data-theme="dark"] .my-component {
    /* Dark theme specific styles */
    box-shadow: var(--shadow-lg);
}
```

---

## File Structure

```
frontend/css/
├── design-tokens.css    # All design tokens
├── theme.css            # Theme system & utilities
├── styles.css           # Main styles
├── controls.css         # Button & input styles
├── grid.css             # Grid component
├── dpad.css             # D-pad component
└── animations.css       # Animation utilities

frontend/js/
└── theme.js             # Theme management system
```

---

## Browser Support

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (with -webkit- prefixes)
- Mobile browsers: Full support

---

## Performance

The design system is optimized for performance:

- CSS custom properties for efficient theme switching
- Hardware-accelerated animations (transform, opacity)
- Minimal repaints/reflows
- Debounced scroll handlers
- Efficient ripple effect implementation

---

## Future Enhancements

Potential additions:
- Additional color themes (purple, green, etc.)
- More glassmorphism variants
- Expanded animation library
- Component library documentation
- Storybook integration

---

## Credits

Design System Version: 1.0.0
Last Updated: 2025
Built for: Toy Robot Simulator
