# Google Stitch Design Prompt: Zomato AI Restaurant Recommender

## Quick Brief for AI Design Generation

**Project:** Modern web app for AI-powered restaurant recommendations (similar to Zomato but with LLM intelligence)

---

## What I Need

Design a **modern, food-focused web application interface** with these key screens:

### 1. Main Screen - Restaurant Recommendation Dashboard

**Layout:** Two-column design
- **Left Sidebar (350px):** User preference inputs
- **Right Main Area:** AI-powered restaurant recommendation cards

**Left Sidebar Components:**
```
🔍 Your Preferences
├─ 📍 Location (dropdown: Delhi, Mumbai, Bangalore)
├─ 💰 Budget (3 visual radio cards: Low/Medium/High)
├─ 🍴 Cuisine (dropdown with search)
├─ ⭐ Minimum Rating (slider: 0-5 stars)
├─ ✨ Additional Preferences (tag input)
└─ [Large "Get Recommendations" button - red/orange]
```

**Main Area - Restaurant Cards:**
Each card shows:
- 🥇 Rank badge (gold medals for top 3)
- Restaurant name (large, bold)
- ⭐⭐⭐⭐⭐ Star rating (4.8/5.0)
- 🍴 Cuisine type • 💰 Cost (₹1500 for two) • 📍 Location
- 💬 AI Explanation section (light background box with rounded corners)
- Action buttons: [Learn More] [Directions] [Save]

---

## Visual Style Requirements

**Color Palette:**
- Primary: Zomato Red (#E23744) for buttons, accents, headings
- Gold: #FFB800 for star ratings and premium elements
- Background: Clean white (#FFFFFF) with subtle gray sections (#F8F9FA)
- Text: Dark gray (#333) for main text, medium gray (#666) for secondary
- Success: Green (#28a745) for positive actions

**Typography:**
- Modern sans-serif (Inter, Poppins, or similar)
- Headings: Bold, large (32-48px for title)
- Restaurant names: 20-24px, semi-bold
- Body text: 15-16px with generous line-height (1.6)
- AI explanations: Comfortable reading experience

**Card Design:**
- White background with subtle shadow (no harsh borders)
- Border-radius: 12-16px for modern feel
- Generous padding (24-32px)
- Hover effect: Slight elevation with deeper shadow
- Clean, spacious layout - easy to scan

**Overall Aesthetic:**
- Clean, modern, professional
- Warm and appetizing (food-focused)
- Trustworthy (AI-powered but not robotic)
- Spacious with good white space
- Mobile-responsive considerations

---

## Specific Design Elements

### Hero/Header Section
```
┌──────────────────────────────────────────────────┐
│  🍽️ Zomato AI Restaurant Recommender            │
│  Discover perfect restaurants powered by AI ✨   │
│  [Subtle gradient or food-themed background]     │
└──────────────────────────────────────────────────┘
```

### Restaurant Card Example
```
╔════════════════════════════════════════════════╗
║  🥇 #1                                         ║
║                                                ║
║  Dum Pukht                                     ║
║  ⭐⭐⭐⭐⭐ 4.9 / 5.0                         ║
║  🍴 North Indian, Awadhi • 💰 ₹4000 for two   ║
║  📍 Delhi • 👥 5,000 votes                     ║
║                                                ║
║  ╭─────────────────────────────────────────╮  ║
║  │ 💬 Why we recommend this:               │  ║
║  │ Dum Pukht offers an exceptional Mughlai│  ║
║  │ dining experience that perfectly matches│  ║
║  │ your preferences for authentic North    │  ║
║  │ Indian cuisine in Delhi...              │  ║
║  ╰─────────────────────────────────────────╯  ║
║                                                ║
║  [Learn More] [Get Directions] [♥ Save]        ║
╚════════════════════════════════════════════════╝
```

### Empty State (Before Search)
```
┌─────────────────────────────────┐
│        🍽️                       │
│   Welcome!                       │
│   Select your preferences        │
│   to discover great restaurants  │
│                                  │
│   📊 Dataset: 20 restaurants     │
│   🌆 Cities: Delhi, Mumbai, Blr  │
│   🍴 Cuisines: 15+ types         │
└─────────────────────────────────┘
```

---

## Device Views Needed

1. **Desktop (1920x1080)** - Two-column layout as described
2. **Tablet (1024x768)** - Collapsible sidebar, single column cards
3. **Mobile (375x812)** - Stacked layout, sticky filter button

---

## Key UI/UX Priorities

✅ **Visual Hierarchy** - Eyes should go: Rank → Name → Rating → Explanation → Actions
✅ **Scannability** - Users can quickly compare 5 recommendations
✅ **Trust Signals** - AI explanations feel credible and thoughtful
✅ **Food Appeal** - Warm colors, appetizing aesthetic
✅ **Modern & Clean** - Contemporary design patterns
✅ **Professional Polish** - Premium feel, attention to detail

---

## What Makes This Unique

🤖 **AI-Generated Explanations:** Each recommendation has a personalized explanation section - this should be visually distinct and inviting to read (light background, comfortable spacing)

🏆 **Smart Ranking:** Top recommendations get visual prominence (medal badges, gradient effects)

✨ **Personality:** Balance between professional restaurant guide and friendly AI assistant

---

## Design Deliverables Needed

1. **High-fidelity mockup** - Desktop view with 5 restaurant cards visible
2. **Component close-ups** - Sidebar inputs, restaurant card, empty state
3. **Color palette** - Exact hex codes
4. **Typography specs** - Font family, sizes, weights
5. **Spacing/measurements** - Card dimensions, padding values
6. **Icon suggestions** - For location, cuisine, rating, cost, etc.

---

## Inspiration Apps (for reference)

- **Zomato** - Brand colors and food aesthetic
- **Airbnb** - Clean card design and spacing
- **ChatGPT** - Text explanation styling
- **OpenTable** - Professional restaurant listings
- **Modern food delivery apps** - Contemporary UI patterns

---

## Technical Note

This will be built in **Streamlit** (Python web framework), so designs should be:
- Clean and straightforward (not overly complex animations)
- Card-based layouts work well
- Custom CSS can be injected for styling
- Focus on colors, typography, spacing, and component design

---

## Example Scenarios to Design For

**Scenario 1:** User searching for "Italian restaurants in Delhi, medium budget, 4+ rating"
→ Show 3-5 Italian restaurant cards with AI explanations

**Scenario 2:** First-time visitor
→ Show welcoming empty state with dataset preview

**Scenario 3:** No matching restaurants found
→ Show helpful "no results" state with suggestions

---

## Final Notes

**Tone:** Professional yet warm, modern yet approachable, intelligent yet friendly

**Goal:** Make users excited to discover restaurants with AI assistance - the design should feel like a premium recommendation service

**Priority:** Beautiful, modern interface that builds trust in AI recommendations while celebrating food discovery

---

## Generate These Views

Please create:
1. **Main dashboard** with sidebar + 5 restaurant recommendation cards
2. **Close-up of single restaurant card** showing all details
3. **Mobile responsive version** of the main view
4. **Color palette & typography guide**

Style: Modern, clean, food-focused, trustworthy, professionally polished
