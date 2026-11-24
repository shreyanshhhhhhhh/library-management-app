# LibraTrack — Library Inventory Management System

A modern, responsive web application for managing library inventory, built with vanilla HTML/CSS/JavaScript.

![Dashboard](screenshots/01-dashboard.png)

## Features

### Core Functionality
- **Book Catalog Management** — Add, edit, delete books with full metadata (title, author, ISBN, genre, publisher, year, shelf location)
- **Multiple Copies Support** — Track individual copies of the same book, with per-copy availability tracking
- **Member Management** — Register members with configurable book limits by type (Student, Faculty, Staff, External)
- **Issue / Return Workflow** — Streamlined forms for issuing and returning books with real-time validation
- **Fine Management** — Automatic overdue fine calculation (₹2/day), payment tracking with multiple methods (Cash, UPI, Card, Waiver)
- **Transaction History** — Complete audit trail of all issues and returns with filtering

### Additional Features
- **Dashboard** — At-a-glance overview with key metrics, recent transactions, and overdue alerts
- **Notifications** — Real-time alerts for overdue books and upcoming due dates
- **Reports & Analytics** — Charts for genre distribution, monthly transaction trends, top borrowed books, and most active members
- **Global Search** — Search across books, members, and transactions from any page
- **Quick Actions** — Shortcut menu for common operations
- **Sample Data** — One-click demo data loading for testing
- **Responsive Design** — Works on desktop, tablet, and mobile screens
- **Persistent Storage** — All data saved to browser localStorage

## Scenarios Covered

1. **Adding a new book** — With ISBN uniqueness validation
2. **Adding multiple copies** of the same book
3. **Editing book details** — With safeguard against reducing copies below issued count
4. **Deleting a book** — Blocked if any copies are currently issued
5. **Registering a new member** — With duplicate email detection
6. **Configurable borrowing limits** per member type
7. **Issuing a book** — With checks for:
   - Member's borrowing limit
   - Book copy availability
   - Duplicate issue prevention (same book to same member)
   - Pending fine warnings
8. **Returning a book** — With automatic overdue fine calculation
9. **Fine calculation** — ₹2 per day overdue, applied on return
10. **Fine payment** — Multiple methods (Cash, UPI, Card, Librarian waiver)
11. **Blocking member deletion** if they have active issues or pending fines
12. **Overdue tracking** — Dashboard alerts and notification badges
13. **Due-soon reminders** — Notifications for books due within 2 days
14. **Transaction filtering** — By type (issue/return), status (active/returned/overdue)
15. **Faculty vs. Student limits** — Different max book allowances
16. **Report generation** — Genre distribution, monthly trends, leaderboards

## Tech Stack

- **Frontend:** HTML5, CSS3 (Custom Properties, Grid, Flexbox), Vanilla JavaScript (ES6+)
- **Charts:** Chart.js 4
- **Icons:** Material Icons Outlined (Google Fonts)
- **Typography:** Inter (Google Fonts)
- **Storage:** Browser localStorage

## Getting Started

1. Clone the repository
2. Open `index.html` in any modern browser
3. Click **Quick Action → Load Sample Data** to populate demo data
4. Explore the dashboard and all features!

No build tools, no server, no dependencies to install.

## Screenshots

See the `screenshots/` directory for a complete walkthrough of all features.

## License

MIT
