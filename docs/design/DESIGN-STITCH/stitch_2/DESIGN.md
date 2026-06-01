---
name: Epicurean Intelligence
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#5b403f'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#7c5800'
  on-secondary: '#ffffff'
  secondary-container: '#feb700'
  on-secondary-container: '#6b4b00'
  tertiary: '#5c5c5c'
  on-tertiary: '#ffffff'
  tertiary-container: '#757474'
  on-tertiary-container: '#fffcfb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdea8'
  secondary-fixed-dim: '#ffba20'
  on-secondary-fixed: '#271900'
  on-secondary-fixed-variant: '#5e4200'
  tertiary-fixed: '#e4e2e1'
  tertiary-fixed-dim: '#c8c6c6'
  on-tertiary-fixed: '#1b1c1c'
  on-tertiary-fixed-variant: '#474747'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 64px
---

## Brand & Style

The design system is engineered to bridge the gap between high-utility data and the visceral joy of dining. It targets food enthusiasts who value precision, speed, and discovery. The brand personality is **Professional, Warm, and Intelligent**—acting as a sophisticated digital concierge rather than a mere search tool.

The visual style is **Corporate / Modern** with a focus on high-fidelity food imagery. It utilizes a "Content-First" philosophy where the UI recedes to let vibrant photography take center stage. The interface is characterized by generous whitespace, soft depth, and a high degree of "finish" through subtle micro-interactions and refined typography. The goal is to evoke a sense of reliability and appetite, ensuring the user feels both well-informed and inspired.

## Colors

The palette is anchored by the iconic red to maintain brand heritage, while introducing a sophisticated neutral scale to handle complex AI data visualization.

- **Primary (#E23744):** Used for critical actions, brand presence, and highlighting "must-try" recommendations.
- **Secondary (#FFB800):** Reserved exclusively for prestige markers: star ratings, Michelin status, and AI "Best Match" badges.
- **Neutral Surface (#FFFFFF):** The base for all primary content cards and modals to maximize clarity.
- **Neutral Background (#F8F9FA):** Used for page-level backgrounds to create a subtle contrast with white UI components, providing a layered "app-in-app" feel.
- **Tertiary/Text (#2D2D2D):** A soft black for primary typography to reduce eye strain while maintaining high legibility.

## Typography

This design system utilizes **Inter** across all levels to ensure maximum readability and a systematic, clean aesthetic. The type hierarchy is strictly defined to handle dense information—like menus and restaurant details—without overwhelming the user.

- **Headlines:** Use tight letter-spacing and bold weights to create a strong visual anchor.
- **Body:** Standardized at 16px for optimal reading on mobile and web.
- **Labels:** Used for metadata (distance, price bracket, AI tags). These often utilize uppercase styling and heavier weights to differentiate from body prose.
- **Responsive Note:** For mobile devices, headline-xl scales down to 32px to prevent awkward text wrapping on restaurant titles.

## Layout & Spacing

The design system employs a **Fluid Grid** approach based on an 8px square rhythm. This ensures alignment and harmony across all components.

- **Mobile:** A 4-column grid with 16px side margins. Content cards typically span the full width (4 columns) to prioritize food photography.
- **Tablet:** An 8-column grid with 24px margins. This allows for a two-card horizontal layout for restaurant listings.
- **Desktop:** A 12-column grid with a maximum content width of 1280px. This enables a multi-pane interface: filters on the left, results in the center, and the AI chatbot or "Selected Restaurant" view on the right.

Spacing between related elements (title and rating) should use `sm` (12px), while spacing between distinct sections (Menu and Reviews) should use `xl` (32px).

## Elevation & Depth

This design system uses **Tonal Layers** combined with **Ambient Shadows** to create a clear sense of hierarchy. Depth is functional, indicating interactable elements and temporary overlays.

- **Level 0 (Background):** #F8F9FA. The lowest plane.
- **Level 1 (Cards/Surface):** #FFFFFF with a 1px border (#E0E0E0) or a very soft shadow (0px 2px 4px rgba(0,0,0,0.05)). Used for restaurant cards and list items.
- **Level 2 (Floating/Active):** #FFFFFF with a medium shadow (0px 8px 16px rgba(0,0,0,0.08)). Used for hover states, filter dropdowns, and the AI recommendation engine input.
- **Level 3 (Modals):** #FFFFFF with a deep shadow (0px 16px 32px rgba(0,0,0,0.12)). Used for full-screen restaurant details and image galleries.

## Shapes

The shape language is defined by **Rounded** corners, creating a friendly and approachable feel that mimics the organic nature of food.

- **Small Components (Buttons, Inputs, Chips):** 8px (0.5rem) radius.
- **Medium Components (Restaurant Cards, Modals):** 16px (1rem) radius.
- **Large Components (Hero Banners, Image Containers):** 24px (1.5rem) radius.
- **Interactive States:** When a card is pressed, it should subtly shrink (98% scale) to provide tactile feedback.

## Components

- **Buttons:** Primary buttons are solid Primary Red with white text. Secondary buttons use a Primary Red outline with a transparent background. All buttons have a height of 48px for touch accessibility.
- **AI Recommender Chip:** High-contrast chips with a Secondary Gold background and dark text to highlight AI-generated tags like "Perfect for Dates" or "High Protein."
- **Input Fields:** Search bars and AI prompt boxes should be 56px tall, using a 16px corner radius and a subtle #F8F9FA fill to stand out from the white background.
- **Restaurant Cards:** Features a 16:9 aspect ratio image at the top with a 16px corner radius. Metadata (rating, price, distance) is placed below the image with generous `sm` padding.
- **Lists:** Used for menus or review sections. Items are separated by a 1px #F1F1F1 divider, with 16px vertical padding.
- **AI Progress/Loading:** A soft, pulsing Primary Red glow on the border of cards while the AI is "thinking" or fetching a recommendation.