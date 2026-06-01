# UI/UX Design Brief for Zomato AI Restaurant Recommender

## Project Overview

**Product Name:** Zomato AI Restaurant Recommender  
**Type:** Web Application (Streamlit-based)  
**Purpose:** An intelligent restaurant recommendation system that uses AI to provide personalized dining suggestions with human-like explanations

---

## Product Context

### What the Application Does
1. **Collects User Preferences** - Location, budget, cuisine type, minimum rating, and additional preferences (e.g., "romantic", "family-friendly")
2. **Filters Restaurants** - Searches through a curated Zomato restaurant dataset
3. **AI-Powered Ranking** - Uses Groq's Llama 3 70B LLM to intelligently rank and explain recommendations
4. **Displays Results** - Shows top restaurant recommendations with detailed AI-generated explanations

### Current State
The application is **functionally complete** with:
- ✅ Full backend pipeline (data loading, filtering, LLM integration)
- ✅ Basic Streamlit UI with sidebar inputs
- ✅ Working recommendation engine with AI explanations
- ⚠️ **Very basic visual design** - needs professional UI/UX upgrade

---

## Design Goals

### Primary Objectives
1. **Modern & Professional** - Compete with contemporary food discovery apps (Zomato, Swiggy, DoorDash)
2. **Trust & Credibility** - Users should feel confident in AI-powered recommendations
3. **Delightful Experience** - Make restaurant discovery fun and engaging
4. **Mobile-First Responsive** - Works beautifully on all device sizes
5. **Brand Alignment** - Subtle Zomato inspiration without being a clone

### Target Audience
- **Age:** 18-45 years old
- **Tech-Savvy:** Comfortable with AI-powered services
- **Food Enthusiasts:** People who enjoy dining out and discovering new restaurants
- **Urban Professionals:** Looking for quick, reliable restaurant recommendations

---

## Design Requirements

### 1. Color Palette

**Primary Brand Colors:**
- **Zomato Red:** `#E23744` (accent for CTAs, highlights)
- **Deep Red:** `#C62828` (hover states)

**Suggested Palette:**
- **Primary:** Vibrant food-inspired red/orange gradient
- **Secondary:** Deep navy or charcoal for text and contrast
- **Accent:** Gold/amber for ratings and premium features (`#FFB800`)
- **Success:** Fresh green for positive actions (`#28a745`)
- **Neutrals:** Light grays for backgrounds (`#F8F9FA`, `#E9ECEF`)

**Inspiration:** Food photography aesthetics - warm, appetizing, inviting

### 2. Typography

**Recommendations:**
- **Headings:** Bold, modern sans-serif (Inter, Poppins, or Outfit)
- **Body Text:** Readable sans-serif with good line-height (1.6-1.8)
- **Special Elements:** 
  - Restaurant names: Larger, bold weight
  - AI explanations: Slightly lighter weight for readability
  - Ratings: Tabular figures for consistency

**Hierarchy:**
- H1 (Page Title): 36-48px, Bold
- H2 (Section Headers): 24-32px, Semi-bold
- H3 (Restaurant Names): 20-24px, Bold
- Body: 15-16px, Regular
- Small (Metadata): 13-14px, Regular

### 3. Layout Structure

#### A. Header/Hero Section
```
┌─────────────────────────────────────────────────────┐
│  🍽️ Zomato AI Restaurant Recommender               │
│  Discover perfect restaurants powered by AI ✨      │
│                                                     │
│  [Background: Subtle food imagery or gradient]      │
└─────────────────────────────────────────────────────┘
```

**Elements:**
- Logo/icon (fork & knife, or AI brain with utensils)
- Tagline emphasizing AI-powered personalization
- Subtle animation on load (optional)

#### B. Two-Column Layout

**Left Sidebar (Preferences Panel):**
```
┌───────────────────────┐
│ 🔍 Tell Us Your       │
│    Preferences        │
├───────────────────────┤
│                       │
│ 📍 Location           │
│ [Select Dropdown]     │
│                       │
│ 💰 Budget             │
│ [Radio Cards]         │
│ ○ Low  ○ Med  ○ High │
│                       │
│ 🍴 Cuisine            │
│ [Select Dropdown]     │
│                       │
│ ⭐ Min Rating         │
│ [Slider: 0-5]         │
│                       │
│ ✨ Additional         │
│ [Text tags input]     │
│                       │
│ ┌──────────────────┐  │
│ │ 🔍 Get           │  │
│ │ Recommendations  │  │
│ └──────────────────┘  │
└───────────────────────┘
```

**Main Content Area (Results):**
```
┌────────────────────────────────────────────┐
│  Your Personalized Recommendations         │
│  Based on: Delhi • Italian • Medium • 3.5+ │
├────────────────────────────────────────────┤
│                                            │
│  ╔═══════════════════════════════════════╗ │
│  ║ 🥇 #1                                 ║ │
│  ║                                       ║ │
│  ║ Restaurant Name                       ║ │
│  ║ ⭐⭐⭐⭐⭐ 4.8 • 🍴 Italian, Med    ║ │
│  ║ 💰 ₹1500 for two • 📍 Connaught Place ║ │
│  ║                                       ║ │
│  ║ 💬 AI Explanation:                    ║ │
│  ║ [Beautiful typography with good       ║ │
│  ║  line height explaining why this      ║ │
│  ║  restaurant is perfect...]            ║ │
│  ║                                       ║ │
│  ║ [Learn More] [Save] [Directions]      ║ │
│  ╚═══════════════════════════════════════╝ │
│                                            │
│  [Similar cards for #2, #3, #4, #5...]    │
└────────────────────────────────────────────┘
```

### 4. Component Design Specifications

#### A. Restaurant Recommendation Cards

**Visual Hierarchy:**
1. **Rank Badge** - Medal emoji (🥇🥈🥉) or numbered badge with gradient
2. **Restaurant Name** - Bold, large, primary color
3. **Rating Stars** - Gold stars with numeric rating
4. **Metadata Row** - Cuisine, cost, location with icons
5. **AI Explanation Box** - Light background, comfortable reading
6. **Action Buttons** - Secondary style, clear affordances

**Card Styling:**
- Background: White or very light gray
- Border: Subtle shadow, no harsh borders
- Border-radius: 12-16px for modern feel
- Padding: Generous (24-32px)
- Hover State: Subtle lift effect with deeper shadow
- Medal/Rank: Prominent badge or gradient background

**Icon Usage:**
- ⭐ Ratings
- 🍴 Cuisine
- 💰 Cost
- 📍 Location
- 👥 Votes/popularity
- 💬 AI explanation indicator

#### B. Input Widgets

**Location Dropdown:**
- Custom styled select with search
- Icons for major cities
- Clear visual feedback on selection

**Budget Radio Cards:**
- Visual cards instead of plain radio buttons
- Each card shows:
  - Icon (💵 💰 💎)
  - Label (Low/Medium/High)
  - Price range (₹0-500, ₹500-1500, ₹1500+)
- Selected state: Solid background with primary color
- Unselected: Border only, transparent

**Cuisine Dropdown:**
- Search-enabled select
- Popular cuisines at top
- Food emoji per cuisine (🍕 Italian, 🍜 Chinese, etc.)

**Rating Slider:**
- Custom styled with gradient track
- Star icons at endpoints
- Tooltip showing current value

**Additional Preferences:**
- Tag-style input (like hashtags)
- Auto-suggest common preferences
- Visual pills for entered tags

**Get Recommendations Button:**
- Large, prominent CTA
- Primary brand color
- Subtle animation on hover
- Loading spinner when processing

#### C. Empty States

**Welcome Screen (Before Search):**
```
┌──────────────────────────────────┐
│         🍽️                       │
│   Welcome to Zomato AI            │
│   Restaurant Recommender          │
│                                   │
│   📊 Dataset Overview:            │
│   • 20 Restaurants                │
│   • 3 Cities                      │
│   • 15+ Cuisines                  │
│   • Average Rating: 4.3 ⭐        │
│                                   │
│   ← Select your preferences       │
│      to get started               │
└──────────────────────────────────┘
```

**No Results State:**
```
┌──────────────────────────────────┐
│         🔍                        │
│   No restaurants found            │
│                                   │
│   Try adjusting your filters:     │
│   • Lower minimum rating          │
│   • Expand budget range           │
│   • Try different cuisine         │
│   • Select nearby locations       │
└──────────────────────────────────┘
```

#### D. Loading States

**During AI Processing:**
```
┌──────────────────────────────────┐
│         🤖                        │
│   AI is analyzing restaurants... │
│   [Animated spinner]              │
│                                   │
│   Filtering • Ranking • Explaining│
└──────────────────────────────────┘
```

### 5. Interactions & Micro-animations

**Recommended Animations:**
1. **Card Entry:** Stagger animation (each card fades + slides in sequentially)
2. **Button Hover:** Subtle scale (1.02x) + shadow increase
3. **Loading:** Smooth spinner or skeleton screens for cards
4. **Star Rating:** Gold shimmer effect
5. **Medal Badge:** Pulse animation on reveal
6. **Success State:** Checkmark animation after search

**Transitions:**
- Smooth easing (cubic-bezier)
- Duration: 200-300ms for most interactions
- No jarring movements

### 6. Responsive Breakpoints

**Desktop (>1200px):**
- Two-column layout (sidebar + main)
- 2 cards per row (optional)
- Full width hero

**Tablet (768-1200px):**
- Collapsible sidebar
- Single column cards
- Adjusted spacing

**Mobile (<768px):**
- Stack sidebar above content
- Sticky "Filter" button to toggle preferences
- Single column layout
- Reduced padding
- Larger touch targets (48px minimum)

### 7. Accessibility Requirements

✅ **Must Haves:**
- WCAG 2.1 AA compliant color contrast (4.5:1 for text)
- Keyboard navigation support
- Screen reader friendly labels
- Focus states on all interactive elements
- Alternative text for icons
- Semantic HTML structure

### 8. Visual Style References

**Inspiration Apps:**
- **Zomato** - Brand colors, food imagery style
- **Airbnb** - Clean card design, trustworthy aesthetic
- **OpenTable** - Professional restaurant listings
- **Yelp** - Rating display, review formatting
- **ChatGPT** - AI explanation text styling

**Design Trends to Incorporate:**
- Modern card-based layouts
- Soft shadows (no harsh borders)
- Generous white space
- Gradient accents (subtle, not overwhelming)
- Glass-morphism for overlays (optional)
- Illustration or icon system for empty states

---

## Technical Constraints

### Platform
- **Framework:** Streamlit (Python-based web framework)
- **Styling:** Custom CSS within Streamlit's constraints
- **Components:** HTML/CSS injection for custom styling
- **Limitations:** 
  - Cannot use complex JavaScript frameworks
  - Limited to Streamlit's component library
  - Custom components via HTML/CSS markdown

### Performance
- Lightweight design (images optimized)
- Fast loading times (<2s initial load)
- Smooth animations (60fps)

---

## Deliverables Requested

From Google Stitch or Design Tool:

### 1. High-Fidelity Mockups
- **Desktop View** (1920x1080)
  - Welcome/empty state
  - Search form filled
  - Results with 5 recommendation cards
- **Tablet View** (1024x768)
- **Mobile View** (375x812)

### 2. Component Library
- Button styles (primary, secondary, disabled)
- Input field styles
- Card variants
- Icon set
- Typography scale
- Color palette with hex codes

### 3. Style Guide
- Spacing system (4px, 8px, 16px, 24px, 32px scale)
- Shadow system (card, hover, modal)
- Border radius standards
- Animation specifications

### 4. Asset Export
- SVG icons
- Logo variations
- Background patterns/images
- Example food imagery

### 5. CSS Code (if possible)
- Reusable class names
- Streamlit-compatible CSS snippets
- Custom component HTML templates

---

## Design Brief Summary

**What to Design:**
A modern, food-focused web application interface for AI-powered restaurant recommendations

**Key Screens:**
1. Landing/Welcome screen with input sidebar
2. Loading state during AI processing
3. Results page with ranked restaurant cards
4. Empty state (no results found)
5. Mobile responsive variants

**Visual Direction:**
- Warm, appetizing color palette inspired by food
- Clean, modern card-based layout
- Professional typography with clear hierarchy
- Subtle animations for delight
- Trust-building through clear AI explanations
- Mobile-first responsive design

**Unique Selling Point:**
The AI explanation section in each card must feel conversational, trustworthy, and intelligently personalized - this is what sets us apart from basic restaurant listings.

---

## Reference Context

### Current Color Scheme
```css
Primary: #E23744 (Zomato Red)
Hover: #c62828
Stars: #FFB800 (Gold)
Success: #28a745 (Green)
Background: #f8f9fa
Card Background: #ffffff
Text Primary: #333333
Text Secondary: #666666
Border: #e9ecef
```

### Current UI Elements
- Sidebar with form inputs
- Simple recommendation cards
- Basic star rating display
- Plain text explanations
- Standard Streamlit widgets

### What Needs Improvement
❌ Generic look and feel
❌ Poor visual hierarchy
❌ Boring card design
❌ No brand personality
❌ Limited mobile optimization
❌ No animations or delight factors
❌ Weak call-to-action design

---

## Success Metrics

The design will be considered successful if:

✅ **Visual Appeal** - Users immediately feel this is a premium, modern app
✅ **Clarity** - All actions and information are immediately understandable
✅ **Trust** - AI explanations feel credible and well-presented
✅ **Engagement** - Users want to explore multiple recommendations
✅ **Responsiveness** - Works beautifully on all devices
✅ **Performance** - Design doesn't sacrifice speed
✅ **Implementability** - Can be built within Streamlit's constraints

---

## Additional Notes

### Brand Personality
- **Intelligent** - AI-powered, smart recommendations
- **Friendly** - Approachable, conversational tone
- **Confident** - Trustworthy, reliable suggestions
- **Modern** - Contemporary design language
- **Food-Focused** - Celebrates culinary discovery

### Content Tone
- UI Copy: Friendly, casual, encouraging
- AI Explanations: Professional yet warm
- Error Messages: Helpful, never frustrating
- Empty States: Motivational, guiding

---

## Contact & Feedback

This design brief is for a full-stack AI restaurant recommendation system. The backend architecture is complete - we need a beautiful frontend that makes users excited to discover new restaurants with AI assistance.

**Priority:** High visual impact while maintaining Streamlit implementation feasibility.

**Timeline:** ASAP for Phase 6 refinement

**Questions?** Refer to `architecture.md` for technical details and `context.md` for product context.
