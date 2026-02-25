# CleanRecruit - Recruitment Management System

## 1. Project Overview

**Project Name:** CleanRecruit  
**Project Type:** Web Application (Django + HTMX + SQLite)  
**Core Functionality:** A recruitment management system for a cleaning company that allows HR teams to track candidates through the hiring pipeline, manage positions, schedule interviews, and view analytics.  
**Target Users:** HR team members of a cleaning company

---

## 2. UI/UX Specification

### Layout Structure

**Pages:**
1. **Dashboard** - Overview with analytics cards and charts
2. **Candidates List** - Table with search, filter, and CRUD operations
3. **Candidate Detail/Edit** - Form for adding/editing candidates
4. **Positions List** - Job openings management
5. **Position Detail/Edit** - Form for adding/editing positions
6. **Interviews List** - Interview scheduling and tracking
7. **Analytics** - Detailed recruitment metrics and charts

**Layout:**
- Sidebar navigation (collapsible on mobile)
- Main content area with header
- Responsive grid system

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette:**
- Primary: `#0F766E` (Teal 700 - professional, trustworthy)
- Primary Light: `#14B8A6` (Teal 500)
- Primary Dark: `#0D9488` (Teal 600)
- Secondary: `#6366F1` (Indigo 500 - accent)
- Background: `#F8FAFC` (Slate 50)
- Surface: `#FFFFFF`
- Text Primary: `#1E293B` (Slate 800)
- Text Secondary: `#64748B` (Slate 500)
- Success: `#10B981` (Emerald 500)
- Warning: `#F59E0B` (Amber 500)
- Error: `#EF4444` (Red 500)
- Border: `#E2E8F0` (Slate 200)

**Typography:**
- Font Family: `'DM Sans', sans-serif` (headings), `'IBM Plex Sans', sans-serif` (body)
- Headings: 
  - H1: 32px, 700 weight
  - H2: 24px, 600 weight
  - H3: 20px, 600 weight
  - H4: 16px, 600 weight
- Body: 14px, 400 weight
- Small: 12px, 400 weight

**Spacing System:**
- Base unit: 4px
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64px

**Visual Effects:**
- Card shadows: `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)`
- Hover shadows: `0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)`
- Border radius: 8px (cards), 6px (buttons), 4px (inputs)
- Transitions: 150ms ease-in-out

### Components

**Navigation Sidebar:**
- Logo at top
- Navigation links with icons
- Active state: background highlight with left border accent
- Hover: subtle background change

**Cards:**
- White background
- Subtle shadow
- 8px border radius
- 24px padding

**Buttons:**
- Primary: Teal background, white text
- Secondary: White background, teal border
- Danger: Red background for delete actions
- Icon buttons for actions
- Loading state with spinner

**Forms:**
- Floating labels or top-aligned labels
- Input fields with border
- Focus state: teal border
- Error state: red border with message

**Tables:**
- Striped rows (optional)
- Hover highlight
- Sortable columns
- Pagination
- Row actions (edit, delete, view)

**Status Badges:**
- Pill-shaped
- Color-coded by status
- Small text

**Modals:**
- Centered overlay
- Smooth fade-in animation
- Close button and click-outside to close

**HTMX Elements:**
- Inline editing
- Auto-loading selects
- Dynamic table updates
- Loading indicators
- Toast notifications for feedback

---

## 3. Functionality Specification

### Core Features

**3.1 Candidate Management**
- Create, Read, Update, Delete candidates
- Fields:
  - First Name (required)
  - Last Name (required)
  - Email (required, unique)
  - Phone (optional)
  - Position Applied (foreign key)
  - Status (New, Screening, Interview, Offer, Hired, Rejected)
  - Experience (years)
  - Notes (text)
  - Applied Date (auto)
  - Updated Date (auto)
- Search by name, email
- Filter by status, position
- Sort by name, date, status

**3.2 Position Management**
- Create, Read, Update, Delete job positions
- Fields:
  - Title (required)
  - Description (text)
  - Department (required)
  - Location (required)
  - Status (Open, Filled, Closed)
  - Salary Range (min/max)
  - Created Date (auto)
  - Required Experience (years)
- Search and filter positions

**3.3 Interview Management**
- Create, Read, Update, Delete interviews
- Fields:
  - Candidate (foreign key)
  - Interviewer (name/email)
  - Scheduled Date/Time
  - Type (Phone, Video, In-Person)
  - Status (Scheduled, Completed, Cancelled, No-Show)
  - Notes (text)
  - Rating (1-5)
- Link to candidate

**3.4 Analytics Dashboard**
- Key Metrics Cards:
  - Total Candidates
  - Active Positions
  - Interviews This Week
  - Hire Rate (%)
- Charts:
  - Candidates by Status (donut chart)
  - Applications Over Time (line chart)
  - Hire Rate by Month (bar chart)
  - Positions by Department (bar chart)
- Recent Activity feed

### User Interactions and Flows

**Adding a Candidate:**
1. Click "Add Candidate" button
2. Modal opens with form
3. Fill in details
4. Submit → HTMX posts form
5. Success: Table updates, toast notification
6. Error: Form shows validation errors

**Editing a Candidate:**
1. Click edit icon on row
2. Modal opens with pre-filled form
3. Update details
4. Submit → HTMX updates
5. Success: Row updates, toast notification

**Deleting a Candidate:**
1. Click delete icon
2. Confirmation modal
3. Confirm → HTMX deletes
4. Success: Row removed with animation

**Filtering/Searching:**
1. Type in search box → debounced HTMX request
2. Select filter → immediate HTMX request
3. Table updates without page reload

### Data Handling
- SQLite database for simplicity
- Django ORM for queries
- HTMX for AJAX operations
- Django messages framework for notifications

### Edge Cases
- Empty states with helpful messages
- Form validation (required fields, email format)
- Duplicate email prevention
- Confirm before delete
- Handle network errors gracefully

---

## 4. Technical Stack

- **Backend:** Django 4.2+
- **Database:** SQLite3 (built-in)
- **Frontend:** HTMX + Alpine.js (for minimal JS)
- **Styling:** Custom CSS with CSS variables
- **Charts:** Chart.js
- **Icons:** Heroicons (SVG inline)
- **Fonts:** Google Fonts (DM Sans, IBM Plex Sans)

---

## 5. Project Structure

```
django-CRUD-app/
├── manage.py
├── cleanrecruit/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── recruits/
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        ├── base.html
        ├── components/
        │   ├── sidebar.html
        │   ├── header.html
        │   ├── modal.html
        │   ├── toast.html
        │   └── form_fields.html
        ├── dashboard.html
        ├── candidates/
        │   ├── list.html
        │   └── form.html
        ├── positions/
        │   ├── list.html
        │   └── form.html
        ├── interviews/
        │   ├── list.html
        │   └── form.html
        └── analytics.html
└── static/
    ├── css/
    │   └── styles.css
    └── js/
        └── main.js
```

---

## 6. Acceptance Criteria

1. ✅ Application runs without errors
2. ✅ All CRUD operations work for Candidates, Positions, Interviews
3. ✅ HTMX provides smooth, no-page-refresh interactions
4. ✅ UI is modern, clean, and responsive
5. ✅ Analytics dashboard shows accurate metrics
6. ✅ Forms validate input correctly
7. ✅ Search and filter work in real-time
8. ✅ Toast notifications appear for user actions
9. ✅ Empty states display appropriate messages
10. ✅ Mobile layout is usable
