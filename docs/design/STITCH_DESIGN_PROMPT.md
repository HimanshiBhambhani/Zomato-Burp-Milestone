# Google Stitch Design Prompt: AI-Powered Restaurant Recommendation System

## REFERENCE IMAGE ATTACHED
**IMPORTANT**: I've attached a reference image showing the exact design style, colors, and layout I want. Please closely match:
- The dark navy/purple background color scheme
- The pink/magenta accent colors for buttons and highlights
- The flat illustration style with playful characters
- The clean typography with white text on dark backgrounds
- The modern, friendly, and inviting aesthetic
- The layout structure with navigation, hero section, and content areas

### KEY ELEMENTS TO EXTRACT FROM REFERENCE IMAGE:

1. **Color Scheme**:
   - Background: Dark navy/purple (`#2D2F5F`)
   - Primary accent: Pink/magenta (`#D4619B`) for buttons
   - Secondary accent: Light green (`#A4D65E`) for badges
   - Text: Pure white (`#FFFFFF`)

2. **Typography Style**:
   - Bold, uppercase headings (like "BEST WINE IN TOWN!")
   - Clean sans-serif font throughout
   - High contrast white text on dark backgrounds

3. **Button Design**:
   - Pill-shaped with rounded corners (border-radius: 24-32px)
   - Pink gradient for primary actions ("RESERVE", "SIGN IN")
   - Light green for secondary badges ("New and Fresh")

4. **Illustration Style**:
   - Flat, geometric character designs
   - Simple shapes and solid colors
   - Playful decorative elements (hearts, stars, confetti)
   - Large hero illustration on left side
   - Color palette: Teal, blue, coral, yellow for characters

5. **Layout Pattern**:
   - Horizontal top navigation with logo centered, "SIGN IN" button right
   - Hero section: Illustration LEFT, content RIGHT
   - Content uses white text on dark background
   - Input fields are white/light with pill shape
   - Call-to-action button attached to input field

6. **Visual Mood**:
   - Modern, contemporary, friendly
   - Dark mode aesthetic with vibrant pops of color
   - Approachable and inviting, not corporate
   - Fun but sophisticated

## Project Overview

Design a modern, intuitive web interface for an AI-powered restaurant recommendation system. The application helps users discover personalized restaurant recommendations by combining structured filtering with Large Language Model (LLM) intelligence.

## Core Purpose

Users input dining preferences (location, budget, cuisine, ratings) and receive AI-curated restaurant recommendations with intelligent explanations for why each venue matches their needs.

---

## Key User Journey

1. **Landing State**: User arrives at a clean, welcoming interface with clear call-to-action
2. **Input Preferences**: User fills out a preference form (location, budget, cuisine, minimum rating, additional preferences)
3. **Processing**: System shows elegant loading state while AI analyzes options
4. **Results Display**: Top 5 restaurant recommendations appear as rich cards with AI-generated explanations
5. **Interaction**: User can refine preferences, ask follow-up questions, or save favorites

---

## Required UI Components

### 1. Header Section
- **Application Title**: "Zomato AI Restaurant Recommender" or similar food-focused branding
- **Tagline**: "Discover your next favorite dining experience with AI"
- **Optional**: Quick stats (e.g., "20,000+ restaurants | AI-powered recommendations")

### 2. Preference Input Panel (Sidebar or Left Panel)

**Input Fields:**
- **Location Selector**: Dropdown or autocomplete with Indian cities (Delhi, Bangalore, Mumbai, etc.)
- **Budget Selector**: Radio buttons or segmented control with 3 options:
  - Low (₹0-500 for two)
  - Medium (₹500-1500 for two)
  - High (₹1500+ for two)
- **Cuisine Input**: Text input or multi-select dropdown (Italian, Chinese, Indian, Continental, etc.)
- **Minimum Rating**: Star rating slider or segmented control (3.0, 3.5, 4.0, 4.5)
- **Additional Preferences**: Text area for freeform input (e.g., "family-friendly", "quick service", "outdoor seating", "romantic ambiance")

**Action Button:**
- Primary CTA: "Get AI Recommendations" or "Find Restaurants"
- Should be visually prominent with hover/active states

### 3. Results Display Area (Main Content)

**Recommendation Cards** (Display 5 cards vertically or in 2-column grid):

**Card Design (MATCH REFERENCE AESTHETIC):**
- **Background**: White (`#FFFFFF`) or very light gray (`#F8F9FC`) - provides contrast against dark page background
- **Border**: None or subtle shadow for elevation
- **Border-radius**: 16-20px (modern, rounded)
- **Padding**: 24-28px
- **Shadow**: Soft elevation shadow (`0 4px 12px rgba(0, 0, 0, 0.15)`)

Each card should include:
- **Rank Badge**: 
  - Style: Circular or pill-shaped badge in top-left
  - Colors: Gold for #1, Silver for #2, Bronze for #3, Pink accent for 4-5
  - Medal emojis: 🥇🥈🥉 or numbered badges (1, 2, 3...)
  
- **Restaurant Name**: 
  - Font-size: 22-24px, semi-bold or bold
  - Color: Dark navy (`#2D2D2D`) for contrast on white card
  
- **Cuisine Type**: 
  - Icon + text (e.g., 🍝 Italian, Mediterranean)
  - Font-size: 14-15px, regular
  - Color: Medium gray (`#6B6B7E`)
  
- **Rating Display**: 
  - Visual: Gold filled stars (⭐⭐⭐⭐⭐) + numeric (4.5)
  - Color: Gold (`#FFD166`) for stars
  - Font-size: 14-16px
  
- **Cost Indicator**: 
  - Format: "₹1200 for two" or "₹₹₹" symbols
  - Font-size: 15-16px, medium weight
  - Color: Dark gray (`#4A4A5E`)
  
- **AI Explanation Section**: 
  - Heading: "💡 Why this is a great match" (pink lightbulb icon)
  - Background: Light lavender/pink tint (`#F8F5FA`) or light green (`#F5FAF0`)
  - Border-radius: 12px
  - Padding: 16px
  - Text: 2-3 sentences, 14-15px, regular
  - Color: Dark text (`#3A3A4E`)
  
- **Action Buttons** (optional): 
  - Secondary style: Outlined or ghost buttons
  - Icons: ❤️ Save, 🔗 Share, 📍 View Map
  - Colors: Match accent colors (pink, green)

**Empty State:**
- Playful illustration (like reference image style characters looking confused/sad)
- White text on dark background
- Message: "No restaurants match your preferences"
- Suggestions in lighter text
- Pink "Try Again" button

**Loading State:**
- On dark background
- Elegant spinner in pink/green colors
- Skeleton cards with shimmer effect (light cards on dark background)
- Text: "🔍 AI is analyzing restaurants for you..."
- Progress indicator or animated dots

### 4. Follow-up/Refinement Panel (Optional Enhancement)

- Chat-style interface for follow-up questions
- Examples: "Show me vegetarian options", "Which is best for a date?", "Any with outdoor seating?"

---

## Design Style Guidelines

### Visual Style (MATCH REFERENCE IMAGE)
- **Modern & Playful**: Dark background with vibrant accents, friendly and inviting
- **Illustration-Driven**: Flat, modern character illustrations like in the reference image
- **Contemporary**: Dark mode aesthetic with high contrast and bold colors
- **Approachable**: Friendly, warm, and welcoming while maintaining sophistication

### Color Palette (FROM REFERENCE IMAGE)

**Primary Colors (USE THESE EXACTLY):**
- **Background Dark Navy/Purple**: `#2D2F5F` or `#2E3047` (main background like reference image)
- **Pure White**: `#FFFFFF` (text on dark backgrounds, card content)
- **Pink/Magenta Accent**: `#D4619B` or `#C85A8E` (primary buttons, highlights, CTAs - like "SIGN IN" and "RESERVE" buttons in reference)

**Secondary Colors:**
- **Light Green/Lime Accent**: `#A4D65E` or `#9FD356` (secondary badges, "New and Fresh" pill in reference)
- **Soft Purple/Lavender**: `#8B7FA8` or `#9B8FB8` (subtle backgrounds, gradient overlays)
- **Warm Coral/Rose**: `#E57C7C` or `#F28B82` (for hearts, love elements like in reference)
- **Soft Yellow/Gold**: `#FFD166` or `#FFC947` (for star ratings, sparkle elements)

**Illustration Elements:**
- **Character Style**: Flat, minimalist illustrations with simple geometric shapes (like the dining couple in reference)
- **Color Blocks**: Use solid colors for clothing (teal, blue, coral) like reference illustration
- **Decorative Elements**: Hearts, stars, sparkles in accent colors (pink, yellow) as shown in reference
- **Background Patterns**: Subtle texture or confetti dots like the green spray pattern in reference

**Text Colors:**
- **Primary Text**: `#FFFFFF` (bright white for headings and important text)
- **Secondary Text**: `#B8B8D8` or `#A8A8C8` (slightly muted for descriptions)
- **Accent Text**: `#A4D65E` (for highlighted terms, badges)

### Typography (MATCH REFERENCE IMAGE STYLE)
- **Headings**: Bold, modern sans-serif with high impact (like "BEST WINE IN TOWN!" in reference)
  - Main Title: 36-48px, bold, uppercase, white color, letter-spacing: 1-2px
  - Section Headings: 24-32px, semi-bold, white
  - Restaurant Names: 20-22px, semi-bold, white
- **Body Text**: Clean, readable sans-serif (e.g., Inter, DM Sans, Plus Jakarta Sans)
  - Main Copy: 15-17px, regular, slightly lighter white (#E5E5E5)
  - Descriptions: 14-16px, regular, muted (#B8B8D8)
  - Labels: 12-14px, medium weight
- **Navigation**: 14-16px, regular, white
- **Buttons**: 14-16px, medium/semi-bold, uppercase or sentence case

### Button & Interactive Elements (FROM REFERENCE IMAGE)
- **Primary Button Style** (like "RESERVE" button):
  - Background: Pink/magenta gradient (`#D4619B` to `#B94E81`)
  - Text: White, semi-bold, uppercase
  - Border-radius: 24-32px (pill-shaped)
  - Padding: 14px 32px
  - Hover: Slightly lighter gradient, subtle scale (1.02)
  - Shadow: Soft glow effect in pink

- **Secondary Button/Badge** (like "New and Fresh" pill):
  - Background: Light green (`#A4D65E`)
  - Text: Dark navy or white, medium weight
  - Border-radius: 16-20px (pill-shaped)
  - Padding: 8px 16px
  - Font-size: 12-13px

- **Input Fields**:
  - Background: White or very light gray (`#F8F8FA`)
  - Border: None or subtle 1px border
  - Border-radius: 24-28px (rounded pill shape)
  - Padding: 12px 20px
  - Placeholder: Light gray (#A0A0B0)

### Spacing & Layout (REFERENCE IMAGE STYLE)
- **Overall Background**: Dark navy/purple (`#2D2F5F`) - like reference image
- **Card Backgrounds**: Slightly lighter shade (`#3A3C68`) or white for contrast
- **Card Spacing**: 20-28px between cards
- **Internal Padding**: 24-32px within cards
- **Sidebar Width**: 340-400px (on desktop)
- **Max Content Width**: 1280-1440px (center-aligned)
- **Border Radius**: 16-24px for cards (modern, rounded corners)
- **Responsive Breakpoints**: Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)

### Illustration Style (CRITICAL - MATCH REFERENCE)
- **Character Design**: Flat, geometric, minimalist style (like the dining couple in reference)
  - Simple shapes for body parts (circles, rounded rectangles)
  - Solid color fills (no gradients within characters)
  - Friendly, approachable facial features (simple dots/circles for eyes)
  - Color palette: Teal, blue, coral, yellow for clothing
- **Decorative Elements**:
  - Floating hearts in coral/pink (`#E57C7C`)
  - Sparkle stars in yellow (`#FFD166`)
  - Confetti or spray patterns in light green (`#A4D65E`)
  - Food/drink icons in the same flat style
- **Placement**: Use illustrations in hero areas, empty states, and as decorative accents
- **Size**: Large hero illustrations (400-600px), smaller decorative elements (100-200px)

---

## Layout Structure (BASED ON REFERENCE IMAGE)

### Overall Design Pattern
- **Background**: Solid dark navy/purple (`#2D2F5F`) covering entire viewport
- **Navigation Bar**: Horizontal top nav with white text links + pink "SIGN IN" button (right-aligned)
- **Content Layout**: Side-by-side layout with illustration LEFT, content RIGHT (like reference)
- **Card Style**: Rounded corners, subtle elevation, light backgrounds on dark base

### Desktop Layout (≥1024px) - REFERENCE IMAGE INSPIRED
```
┌─────────────────────────────────────────────────────────────────┐
│  Nav: Home  Shop  Location  Gallery    🍽️ DineOut  [SIGN IN]  │  ← Dark navy bg, white text
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐   ┌──────────────────────────────┐  │
│  │                      │   │ [New and Fresh Badge]        │  │ ← Light green pill
│  │   🎨 ILLUSTRATION    │   │                              │  │
│  │   (Dining Couple)    │   │ BEST RESTAURANTS IN TOWN!    │  │ ← Bold white heading
│  │                      │   │ DISCOVER AI-POWERED RECS!    │  │
│  │   Flat, playful      │   │                              │  │
│  │   characters with    │   │ We analyze your dining       │  │
│  │   food/drinks        │   │ preferences and suggest...   │  │ ← White body text
│  │   Hearts ♥ Stars ✨  │   │                              │  │
│  │                      │   │ ┌────────────────┬─────────┐ │  │
│  └──────────────────────┘   │ │ Your email here│[RESERVE]│ │  │ ← Pill input + pink button
│                              │ └────────────────┴─────────┘ │  │
│                              └──────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  RECOMMENDATION CARDS SECTION                           │   │
│  │  (White or light cards on dark background)              │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

SIDEBAR VARIATION (Alternative Layout):
┌─────────────────────────────────────────────────────────────────┐
│  🍽️ Restaurant AI Finder         [User Avatar] [Settings]     │
├──────────────┬──────────────────────────────────────────────────┤
│  SIDEBAR     │  MAIN CONTENT (DARK BACKGROUND)                  │
│  (Slightly   │                                                  │
│   lighter    │  ┌────────────────────────────────────────────┐  │
│   purple)    │  │  🥇 Restaurant Card                       │  │ ← Light card on dark
│              │  │  ⭐⭐⭐⭐⭐ 4.8                            │  │
│ 📍 Location  │  │  Italian • ₹₹₹                            │  │
│ [Delhi   ▼]  │  │  💡 Why this matches: ...                 │  │
│              │  └────────────────────────────────────────────┘  │
│ 💰 Budget    │  ┌────────────────────────────────────────────┐  │
│ ○ Low        │  │  🥈 Restaurant Card                       │  │
│ ● Medium     │  │  ...                                      │  │
│ ○ High       │  └────────────────────────────────────────────┘  │
│              │                                                  │
│ 🍽️ Cuisine   │  [More cards...]                                │
│ [Italian  ]  │                                                  │
│              │                                                  │
│ ⭐ Rating    │                                                  │
│ [===●====]   │                                                  │
│              │                                                  │
│ [FIND MATCH] │  ← Pink pill button                             │
└──────────────┴──────────────────────────────────────────────────┘
```

### Mobile Layout (<768px)
- Stack vertically: Header → Preferences (collapsible) → Results
- Full-width cards
- Sticky "Get Recommendations" button at bottom
- Hamburger menu for preferences collapsing

---

## Component States & Interactions

### Interactive States
1. **Idle State**: Clean form, empty results area with prompt to begin
2. **Loading State**: 
   - Disable form inputs
   - Show skeleton cards or spinner
   - Display "AI is analyzing..." message
3. **Success State**: 
   - Display result cards with smooth fade-in animation
   - Show count: "Found 5 perfect matches for you"
4. **Empty State**: 
   - Friendly illustration
   - Helpful message with suggestions
5. **Error State**: 
   - Warning banner: "Oops! Something went wrong"
   - Retry button
   - Fallback suggestions

### Micro-interactions
- **Hover Effects**: Cards elevate slightly with shadow increase
- **Button States**: Color shift + scale on press
- **Form Validation**: Inline validation with helpful error messages
- **Smooth Transitions**: 200-300ms animations for state changes
- **Star Ratings**: Animated fill on load
- **Progress Indicators**: Show LLM processing time estimate

---

## Responsive Design Requirements

### Desktop (>1024px)
- Two-column layout (sidebar + main)
- Cards in 1-column stack or 2-column grid
- Hover effects enabled

### Tablet (768-1024px)
- Collapsible sidebar or full-width preference accordion
- Single-column card layout
- Touch-optimized controls

### Mobile (<768px)
- Fully vertical stack
- Bottom sheet or expandable sections for preferences
- Sticky CTA button
- Swipeable cards (optional)
- Simplified card layout (stack info vertically)

---

## Additional Features to Consider

### Visual Enhancements
- **Food Photography**: Background patterns or hero images of cuisine types
- **Icons**: Cuisine icons, budget indicators (₹, ₹₹, ₹₹₹), amenity icons
- **Badges**: "Top Rated", "Budget Friendly", "Hidden Gem"
- **Maps Integration**: Small location preview map on cards (optional)

### Accessibility
- ARIA labels for all interactive elements
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus indicators on all interactive elements

### Delight Factors
- **Success Animation**: Celebration confetti when perfect matches found
- **Empty State Illustration**: Playful food-themed characters
- **Loading Messages**: Rotating fun facts about cuisines while processing
- **Save Favorites**: Heart icon to bookmark restaurants for later

---

## Technical Constraints (for Stitch Design Export)

- Ensure design is compatible with **Streamlit framework**
- Components should map to standard Streamlit widgets:
  - `st.selectbox` (dropdowns)
  - `st.radio` (budget selector)
  - `st.text_input` (text fields)
  - `st.slider` (rating slider)
  - `st.button` (CTA)
  - `st.container` / `st.columns` (layout)
- CSS should be exportable for Streamlit's `st.markdown` injection
- Design should work within single-page application constraints

---

## Deliverables Needed from Stitch

1. **High-fidelity mockups** for all key states:
   - Landing/Idle state
   - Loading state
   - Success with results
   - Empty state
   - Mobile responsive views

2. **Component specifications**:
   - Color codes (hex values)
   - Font specifications (family, sizes, weights)
   - Spacing measurements (padding, margins)
   - Elevation/shadow values for cards

3. **Asset exports**:
   - Icons (SVG preferred)
   - Illustrations (for empty states)
   - Logo/brand elements

4. **CSS/Style guide**:
   - Reusable component styles
   - Responsive breakpoints
   - Animation specifications

---

## Key Success Metrics

The design should achieve:
- **Clarity**: Users instantly understand how to get recommendations
- **Speed**: Visual hierarchy guides users through 3-step flow in <30 seconds
- **Trust**: Professional appearance builds confidence in AI suggestions
- **Delight**: Micro-interactions and thoughtful details create memorable experience
- **Accessibility**: Usable by all users regardless of ability

---

## Brand Personality

- **Intelligent**: Showcases AI capability without being intimidating
- **Helpful**: Guide, not gatekeeper — friendly and approachable
- **Reliable**: Trustworthy recommendations for important dining decisions
- **Modern**: Contemporary design with clean aesthetics
- **Warm**: Food is social and joyful — reflect that in design

---

## Reference Inspiration

**Similar Products:**
- Zomato restaurant search (food discovery)
- OpenTable reservation interface (booking flow)
- Spotify recommendations (personalization)
- Airbnb search results (filtering + cards)

**Design Patterns:**
- Material Design 3 (cards, elevation, motion)
- Ant Design (form layouts, data display)
- Apple Human Interface Guidelines (clarity, simplicity)

---

## SUMMARY PROMPT FOR STITCH (Use with Attached Reference Image)

**Attach the DineOut reference image and use this concise prompt:**

"Design a restaurant recommendation web app that matches the attached reference image's aesthetic. 

**Extract and apply from reference:**
- Dark navy/purple background (#2D2F5F)
- Pink/magenta buttons (#D4619B) in pill shape
- Light green accent badges (#A4D65E)
- White text on dark backgrounds
- Flat, playful character illustrations (geometric, minimalist)
- Bold uppercase headings
- Navigation bar: white text + pink right-aligned button
- Hero layout: illustration LEFT, content RIGHT (like reference)
- Rounded pill-shaped input fields and buttons
- Modern, friendly, inviting mood

**Application-specific content:**
- App name: "Restaurant AI Finder" or similar
- Sidebar with preference filters (location, budget, cuisine, rating)
- Main area: White restaurant recommendation cards on dark background
- Cards include: rank badge, name, cuisine, stars, cost, AI explanation
- Pink primary buttons, light green secondary badges
- Playful food-themed illustrations in flat style

**Deliverables:**
1. Landing page with hero section
2. Results page with sidebar filters + restaurant cards
3. Mobile responsive layouts
4. Empty state with illustration
5. Loading state with spinner
6. Color codes, typography specs, spacing measurements
7. Exportable CSS for Streamlit

Match the warm, modern, approachable, dark-mode aesthetic of the reference image throughout."

---

## Final Notes

This is a **data-driven recommendation tool** that should feel both sophisticated and approachable. The AI explanations are the unique value proposition — design should highlight these insights prominently while maintaining clean information architecture for the structured data (name, rating, cost).

**The attached reference image is your primary guide.** Match its color palette, illustration style, typography, button design, and overall mood. Focus on creating a design that makes complex AI recommendations feel simple, trustworthy, and delightful to use.
