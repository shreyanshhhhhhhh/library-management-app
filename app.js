/* ============================================
   LibraTrack — Library Management System
   Application Logic (Vanilla JS + LocalStorage)
   ============================================ */

// ===== DATA LAYER =====
const DB = {
    _get(key) {
        try { return JSON.parse(localStorage.getItem(`libratrack_${key}`)) || []; }
        catch { return []; }
    },
    _set(key, data) { localStorage.setItem(`libratrack_${key}`, JSON.stringify(data)); },

    get books()        { return this._get('books'); },
    set books(v)       { this._set('books', v); },
    get members()      { return this._get('members'); },
    set members(v)     { this._set('members', v); },
    get transactions() { return this._get('transactions'); },
    set transactions(v){ this._set('transactions', v); },
    get finePayments() { return this._get('finePayments'); },
    set finePayments(v){ this._set('finePayments', v); },
    get notifications(){ return this._get('notifications'); },
    set notifications(v){ this._set('notifications', v); },

    nextId(key) {
        const counter = parseInt(localStorage.getItem(`libratrack_counter_${key}`) || '0') + 1;
        localStorage.setItem(`libratrack_counter_${key}`, counter);
        return counter;
    },

    clearAll() {
        const keys = ['books','members','transactions','finePayments','notifications',
                      'counter_books','counter_members','counter_transactions','counter_finePayments'];
        keys.forEach(k => localStorage.removeItem(`libratrack_${k}`));
    }
};

const FINE_RATE = 2; // ₹ per day overdue
const DEFAULT_DUE_DAYS = 14;

// ===== UTILITY FUNCTIONS =====
function formatDate(d) {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function daysBetween(d1, d2) {
    const a = new Date(d1), b = new Date(d2);
    a.setHours(0,0,0,0); b.setHours(0,0,0,0);
    return Math.floor((b - a) / (1000 * 60 * 60 * 24));
}

function today() {
    return new Date().toISOString().split('T')[0];
}

function getBook(id) { return DB.books.find(b => b.id === id); }
function getMember(id) { return DB.members.find(m => m.id === id); }

function getAvailableCopies(bookId) {
    const book = getBook(bookId);
    if (!book) return 0;
    const issuedCount = DB.transactions.filter(t => t.bookId === bookId && !t.returnDate).length;
    return book.copies - issuedCount;
}

function getMemberIssuedCount(memberId) {
    return DB.transactions.filter(t => t.memberId === memberId && !t.returnDate).length;
}

function getMemberPendingFines(memberId) {
    let total = 0;
    DB.transactions.filter(t => t.memberId === memberId && t.fine > 0 && !t.finePaid).forEach(t => {
        total += t.fine;
    });
    // Also check active overdue
    DB.transactions.filter(t => t.memberId === memberId && !t.returnDate).forEach(t => {
        const overdueDays = daysBetween(t.dueDate, today());
        if (overdueDays > 0) total += overdueDays * FINE_RATE;
    });
    return total;
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span class="material-icons-outlined">${
        type === 'success' ? 'check_circle' : type === 'error' ? 'error' : type === 'warning' ? 'warning' : 'info'
    }</span>${message}`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'toastOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== MODAL MANAGEMENT =====
function openModal(id) {
    document.getElementById(id).classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}

document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.close));
});

document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal(overlay.id);
    });
});

// ===== CONFIRM DIALOG =====
let confirmCallback = null;
function showConfirm(title, message, callback) {
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;
    confirmCallback = callback;
    openModal('confirmModal');
}

document.getElementById('confirmYes').addEventListener('click', () => {
    closeModal('confirmModal');
    if (confirmCallback) confirmCallback();
    confirmCallback = null;
});

// ===== NAVIGATION =====
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');

function navigateTo(pageName) {
    navItems.forEach(n => n.classList.remove('active'));
    pages.forEach(p => p.classList.remove('active'));

    const nav = document.querySelector(`[data-page="${pageName}"]`);
    const page = document.getElementById(`page-${pageName}`);

    if (nav) nav.classList.add('active');
    if (page) page.classList.add('active');

    // Refresh the page data
    switch (pageName) {
        case 'dashboard': refreshDashboard(); break;
        case 'catalog': refreshCatalog(); break;
        case 'members': refreshMembers(); break;
        case 'issue': refreshIssuePage(); break;
        case 'transactions': refreshTransactions(); break;
        case 'fines': refreshFines(); break;
        case 'reports': refreshReports(); break;
    }
}

navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(item.dataset.page);
    });
});

// View All links
document.querySelectorAll('.view-all').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(link.dataset.page);
    });
});

// Mobile menu toggle
document.getElementById('menuToggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// ===== DASHBOARD =====
function refreshDashboard() {
    const books = DB.books;
    const txns = DB.transactions;
    const members = DB.members;

    let totalCopies = 0;
    let totalAvailable = 0;
    books.forEach(b => {
        totalCopies += b.copies;
        totalAvailable += getAvailableCopies(b.id);
    });

    const activeIssues = txns.filter(t => !t.returnDate).length;
    const overdue = txns.filter(t => !t.returnDate && daysBetween(t.dueDate, today()) > 0);
    let pendingFines = 0;
    overdue.forEach(t => { pendingFines += daysBetween(t.dueDate, today()) * FINE_RATE; });
    txns.filter(t => t.fine > 0 && !t.finePaid).forEach(t => { pendingFines += t.fine; });

    document.getElementById('stat-totalBooks').textContent = totalCopies;
    document.getElementById('stat-available').textContent = totalAvailable;
    document.getElementById('stat-issued').textContent = activeIssues;
    document.getElementById('stat-overdue').textContent = overdue.length;
    document.getElementById('stat-members').textContent = members.length;
    document.getElementById('stat-fines').textContent = `₹${pendingFines}`;

    // Recent transactions
    const recent = [...txns].sort((a, b) => b.id - a.id).slice(0, 5);
    const recentTbody = document.getElementById('recentTransactions');
    if (recent.length === 0) {
        recentTbody.innerHTML = '<tr><td colspan="4" class="empty-row">No transactions yet</td></tr>';
    } else {
        recentTbody.innerHTML = recent.map(t => {
            const book = getBook(t.bookId);
            const member = getMember(t.memberId);
            const type = t.returnDate ? 'Return' : 'Issue';
            const date = t.returnDate || t.issueDate;
            return `<tr>
                <td>${book ? book.title : 'Unknown'}</td>
                <td>${member ? member.name : 'Unknown'}</td>
                <td><span class="status-badge ${t.returnDate ? 'returned' : 'active'}">${type}</span></td>
                <td>${formatDate(date)}</td>
            </tr>`;
        }).join('');
    }

    // Overdue list
    const overdueTbody = document.getElementById('overdueList');
    if (overdue.length === 0) {
        overdueTbody.innerHTML = '<tr><td colspan="4" class="empty-row">No overdue books 🎉</td></tr>';
    } else {
        overdueTbody.innerHTML = overdue.slice(0, 5).map(t => {
            const book = getBook(t.bookId);
            const member = getMember(t.memberId);
            const days = daysBetween(t.dueDate, today());
            return `<tr>
                <td>${book ? book.title : 'Unknown'}</td>
                <td>${member ? member.name : 'Unknown'}</td>
                <td>${formatDate(t.dueDate)}</td>
                <td class="text-danger">₹${days * FINE_RATE}</td>
            </tr>`;
        }).join('');
    }

    // Check for notifications
    updateNotifications();
}

// ===== NOTIFICATIONS =====
function updateNotifications() {
    const txns = DB.transactions;
    const notifs = [];

    txns.filter(t => !t.returnDate).forEach(t => {
        const days = daysBetween(t.dueDate, today());
        const book = getBook(t.bookId);
        const member = getMember(t.memberId);
        if (!book || !member) return;

        if (days > 0) {
            notifs.push({
                type: 'overdue',
                text: `"${book.title}" issued to ${member.name} is ${days} day(s) overdue. Fine: ₹${days * FINE_RATE}`,
                priority: days
            });
        } else if (days >= -2 && days <= 0) {
            notifs.push({
                type: 'due-soon',
                text: `"${book.title}" issued to ${member.name} is due ${days === 0 ? 'today' : 'in ' + Math.abs(days) + ' day(s)'}`,
                priority: 0
            });
        }
    });

    notifs.sort((a, b) => b.priority - a.priority);

    const badge = document.getElementById('notifBadge');
    if (notifs.length > 0) {
        badge.style.display = 'inline';
        badge.textContent = notifs.length;
    } else {
        badge.style.display = 'none';
    }

    const notifList = document.getElementById('notifList');
    if (notifs.length === 0) {
        notifList.innerHTML = '<div class="notif-empty">No notifications</div>';
    } else {
        notifList.innerHTML = notifs.map(n => `
            <div class="notif-item">
                <span class="material-icons-outlined">${n.type === 'overdue' ? 'warning' : 'schedule'}</span>
                <span>${n.text}</span>
            </div>
        `).join('');
    }
}

document.getElementById('notifBtn').addEventListener('click', () => {
    const panel = document.getElementById('notifPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    updateNotifications();
});

document.getElementById('clearNotifs').addEventListener('click', () => {
    document.getElementById('notifPanel').style.display = 'none';
});

// Click outside to close notification panel
document.addEventListener('click', (e) => {
    const panel = document.getElementById('notifPanel');
    const btn = document.getElementById('notifBtn');
    if (!panel.contains(e.target) && !btn.contains(e.target)) {
        panel.style.display = 'none';
    }
});

// ===== BOOK CATALOG =====
function refreshCatalog() {
    const books = DB.books;
    const search = document.getElementById('catalogSearch').value.toLowerCase();
    const genre = document.getElementById('catalogGenre').value;
    const status = document.getElementById('catalogStatus').value;

    let filtered = books.filter(b => {
        if (search && !b.title.toLowerCase().includes(search) &&
            !b.author.toLowerCase().includes(search) &&
            !b.isbn.toLowerCase().includes(search)) return false;
        if (genre && b.genre !== genre) return false;
        if (status === 'available' && getAvailableCopies(b.id) <= 0) return false;
        if (status === 'issued' && getAvailableCopies(b.id) > 0) return false;
        return true;
    });

    const tbody = document.getElementById('catalogBody');
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-row">No books found</td></tr>';
    } else {
        tbody.innerHTML = filtered.map(b => {
            const avail = getAvailableCopies(b.id);
            return `<tr>
                <td><strong>${escHtml(b.title)}</strong></td>
                <td>${escHtml(b.author)}</td>
                <td><code>${escHtml(b.isbn)}</code></td>
                <td>${escHtml(b.genre)}</td>
                <td>${b.copies}</td>
                <td><span class="status-badge ${avail > 0 ? 'returned' : 'overdue'}">${avail}</span></td>
                <td>
                    <button class="btn-icon-only" title="View" onclick="viewBook(${b.id})">
                        <span class="material-icons-outlined">visibility</span>
                    </button>
                    <button class="btn-icon-only" title="Edit" onclick="editBook(${b.id})">
                        <span class="material-icons-outlined">edit</span>
                    </button>
                    <button class="btn-icon-only danger" title="Delete" onclick="deleteBook(${b.id})">
                        <span class="material-icons-outlined">delete</span>
                    </button>
                </td>
            </tr>`;
        }).join('');
    }
}

function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Catalog filters
['catalogSearch', 'catalogGenre', 'catalogStatus'].forEach(id => {
    document.getElementById(id).addEventListener('input', refreshCatalog);
    document.getElementById(id).addEventListener('change', refreshCatalog);
});

// Add Book
document.getElementById('addBookBtn').addEventListener('click', () => {
    document.getElementById('bookModalTitle').textContent = 'Add New Book';
    document.getElementById('bookSubmitBtn').textContent = 'Add Book';
    document.getElementById('bookForm').reset();
    document.getElementById('bookId').value = '';
    openModal('bookModal');
});

document.getElementById('bookForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const books = DB.books;
    const editId = document.getElementById('bookId').value;

    const data = {
        title: document.getElementById('bookTitle').value.trim(),
        author: document.getElementById('bookAuthor').value.trim(),
        isbn: document.getElementById('bookISBN').value.trim(),
        genre: document.getElementById('bookGenre').value,
        publisher: document.getElementById('bookPublisher').value.trim(),
        year: parseInt(document.getElementById('bookYear').value) || null,
        copies: parseInt(document.getElementById('bookCopies').value) || 1,
        location: document.getElementById('bookLocation').value.trim()
    };

    if (editId) {
        // Edit existing
        const idx = books.findIndex(b => b.id === parseInt(editId));
        if (idx !== -1) {
            // Don't allow reducing copies below issued count
            const issuedCount = DB.transactions.filter(t => t.bookId === parseInt(editId) && !t.returnDate).length;
            if (data.copies < issuedCount) {
                showToast(`Cannot reduce copies below ${issuedCount} (currently issued)`, 'error');
                return;
            }
            books[idx] = { ...books[idx], ...data };
            DB.books = books;
            showToast('Book updated successfully!', 'success');
        }
    } else {
        // Check duplicate ISBN
        if (books.some(b => b.isbn === data.isbn)) {
            showToast('A book with this ISBN already exists!', 'error');
            return;
        }
        data.id = DB.nextId('books');
        data.addedDate = today();
        books.push(data);
        DB.books = books;
        showToast('Book added successfully!', 'success');
    }

    closeModal('bookModal');
    refreshCatalog();
});

function editBook(id) {
    const book = getBook(id);
    if (!book) return;
    document.getElementById('bookModalTitle').textContent = 'Edit Book';
    document.getElementById('bookSubmitBtn').textContent = 'Save Changes';
    document.getElementById('bookId').value = book.id;
    document.getElementById('bookTitle').value = book.title;
    document.getElementById('bookAuthor').value = book.author;
    document.getElementById('bookISBN').value = book.isbn;
    document.getElementById('bookGenre').value = book.genre;
    document.getElementById('bookPublisher').value = book.publisher || '';
    document.getElementById('bookYear').value = book.year || '';
    document.getElementById('bookCopies').value = book.copies;
    document.getElementById('bookLocation').value = book.location || '';
    openModal('bookModal');
}

function viewBook(id) {
    const book = getBook(id);
    if (!book) return;
    const avail = getAvailableCopies(id);
    const issuedCopies = book.copies - avail;
    const txns = DB.transactions.filter(t => t.bookId === id);
    const activeTxns = txns.filter(t => !t.returnDate);

    let html = `
        <div class="detail-grid">
            <div class="detail-item"><div class="detail-label">Title</div><div class="detail-value">${escHtml(book.title)}</div></div>
            <div class="detail-item"><div class="detail-label">Author</div><div class="detail-value">${escHtml(book.author)}</div></div>
            <div class="detail-item"><div class="detail-label">ISBN</div><div class="detail-value"><code>${escHtml(book.isbn)}</code></div></div>
            <div class="detail-item"><div class="detail-label">Genre</div><div class="detail-value">${escHtml(book.genre)}</div></div>
            <div class="detail-item"><div class="detail-label">Publisher</div><div class="detail-value">${escHtml(book.publisher) || '—'}</div></div>
            <div class="detail-item"><div class="detail-label">Year</div><div class="detail-value">${book.year || '—'}</div></div>
            <div class="detail-item"><div class="detail-label">Total Copies</div><div class="detail-value">${book.copies}</div></div>
            <div class="detail-item"><div class="detail-label">Available</div><div class="detail-value"><span class="status-badge ${avail > 0 ? 'returned' : 'overdue'}">${avail}</span></div></div>
            <div class="detail-item"><div class="detail-label">Shelf Location</div><div class="detail-value">${escHtml(book.location) || '—'}</div></div>
            <div class="detail-item"><div class="detail-label">Date Added</div><div class="detail-value">${formatDate(book.addedDate)}</div></div>
        </div>`;

    if (activeTxns.length > 0) {
        html += `<div class="detail-section"><h4>Currently Issued To (${activeTxns.length} of ${book.copies} copies)</h4>
            <table class="data-table compact"><thead><tr><th>Member</th><th>Issue Date</th><th>Due Date</th><th>Status</th></tr></thead><tbody>`;
        activeTxns.forEach(t => {
            const member = getMember(t.memberId);
            const overdueDays = daysBetween(t.dueDate, today());
            html += `<tr>
                <td>${member ? escHtml(member.name) : 'Unknown'}</td>
                <td>${formatDate(t.issueDate)}</td>
                <td>${formatDate(t.dueDate)}</td>
                <td><span class="status-badge ${overdueDays > 0 ? 'overdue' : 'active'}">${overdueDays > 0 ? overdueDays + ' days overdue' : 'On time'}</span></td>
            </tr>`;
        });
        html += '</tbody></table></div>';
    }

    document.getElementById('bookDetailContent').innerHTML = html;
    openModal('bookDetailModal');
}

function deleteBook(id) {
    const book = getBook(id);
    if (!book) return;
    const activeTxns = DB.transactions.filter(t => t.bookId === id && !t.returnDate);
    if (activeTxns.length > 0) {
        showToast(`Cannot delete — ${activeTxns.length} copy(ies) currently issued!`, 'error');
        return;
    }
    showConfirm('Delete Book', `Are you sure you want to delete "${book.title}"? This cannot be undone.`, () => {
        let books = DB.books;
        books = books.filter(b => b.id !== id);
        DB.books = books;
        showToast('Book deleted', 'success');
        refreshCatalog();
    });
}

// ===== MEMBERS =====
function refreshMembers() {
    const members = DB.members;
    const search = document.getElementById('memberSearch').value.toLowerCase();
    const type = document.getElementById('memberType').value;

    let filtered = members.filter(m => {
        if (search && !m.name.toLowerCase().includes(search) &&
            !m.email.toLowerCase().includes(search) &&
            !(m.phone && m.phone.includes(search))) return false;
        if (type && m.type !== type) return false;
        return true;
    });

    const tbody = document.getElementById('memberBody');
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-row">No members found</td></tr>';
    } else {
        tbody.innerHTML = filtered.map(m => {
            const issued = getMemberIssuedCount(m.id);
            const fines = getMemberPendingFines(m.id);
            return `<tr>
                <td><code>M${String(m.id).padStart(4, '0')}</code></td>
                <td><strong>${escHtml(m.name)}</strong></td>
                <td>${escHtml(m.type)}</td>
                <td>${escHtml(m.email)}</td>
                <td>${issued} / ${m.maxBooks}</td>
                <td>${fines > 0 ? `<span class="text-danger">₹${fines}</span>` : '₹0'}</td>
                <td>
                    <button class="btn-icon-only" title="View" onclick="viewMember(${m.id})">
                        <span class="material-icons-outlined">visibility</span>
                    </button>
                    <button class="btn-icon-only" title="Edit" onclick="editMember(${m.id})">
                        <span class="material-icons-outlined">edit</span>
                    </button>
                    <button class="btn-icon-only danger" title="Delete" onclick="deleteMember(${m.id})">
                        <span class="material-icons-outlined">delete</span>
                    </button>
                </td>
            </tr>`;
        }).join('');
    }
}

['memberSearch', 'memberType'].forEach(id => {
    document.getElementById(id).addEventListener('input', refreshMembers);
    document.getElementById(id).addEventListener('change', refreshMembers);
});

document.getElementById('addMemberBtn').addEventListener('click', () => {
    document.getElementById('memberModalTitle').textContent = 'Add New Member';
    document.getElementById('memberSubmitBtn').textContent = 'Add Member';
    document.getElementById('memberForm').reset();
    document.getElementById('memberId').value = '';
    openModal('memberModal');
});

document.getElementById('memberForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const members = DB.members;
    const editId = document.getElementById('memberId').value;

    const data = {
        name: document.getElementById('memberName').value.trim(),
        type: document.getElementById('memberTypeInput').value,
        email: document.getElementById('memberEmail').value.trim(),
        phone: document.getElementById('memberPhone').value.trim(),
        maxBooks: parseInt(document.getElementById('memberMaxBooks').value) || 3
    };

    if (editId) {
        const idx = members.findIndex(m => m.id === parseInt(editId));
        if (idx !== -1) {
            members[idx] = { ...members[idx], ...data };
            DB.members = members;
            showToast('Member updated!', 'success');
        }
    } else {
        // Check duplicate email
        if (members.some(m => m.email === data.email)) {
            showToast('A member with this email already exists!', 'error');
            return;
        }
        data.id = DB.nextId('members');
        data.joinDate = today();
        members.push(data);
        DB.members = members;
        showToast('Member added!', 'success');
    }

    closeModal('memberModal');
    refreshMembers();
});

function editMember(id) {
    const member = getMember(id);
    if (!member) return;
    document.getElementById('memberModalTitle').textContent = 'Edit Member';
    document.getElementById('memberSubmitBtn').textContent = 'Save Changes';
    document.getElementById('memberId').value = member.id;
    document.getElementById('memberName').value = member.name;
    document.getElementById('memberTypeInput').value = member.type;
    document.getElementById('memberEmail').value = member.email;
    document.getElementById('memberPhone').value = member.phone || '';
    document.getElementById('memberMaxBooks').value = member.maxBooks;
    openModal('memberModal');
}

function viewMember(id) {
    const member = getMember(id);
    if (!member) return;
    const issued = getMemberIssuedCount(id);
    const fines = getMemberPendingFines(id);
    const txns = DB.transactions.filter(t => t.memberId === id);

    let html = `
        <div class="detail-grid">
            <div class="detail-item"><div class="detail-label">Member ID</div><div class="detail-value">M${String(member.id).padStart(4, '0')}</div></div>
            <div class="detail-item"><div class="detail-label">Name</div><div class="detail-value">${escHtml(member.name)}</div></div>
            <div class="detail-item"><div class="detail-label">Type</div><div class="detail-value">${escHtml(member.type)}</div></div>
            <div class="detail-item"><div class="detail-label">Email</div><div class="detail-value">${escHtml(member.email)}</div></div>
            <div class="detail-item"><div class="detail-label">Phone</div><div class="detail-value">${escHtml(member.phone) || '—'}</div></div>
            <div class="detail-item"><div class="detail-label">Max Books</div><div class="detail-value">${member.maxBooks}</div></div>
            <div class="detail-item"><div class="detail-label">Currently Issued</div><div class="detail-value">${issued}</div></div>
            <div class="detail-item"><div class="detail-label">Pending Fines</div><div class="detail-value">${fines > 0 ? `<span class="text-danger">₹${fines}</span>` : '₹0'}</div></div>
            <div class="detail-item"><div class="detail-label">Member Since</div><div class="detail-value">${formatDate(member.joinDate)}</div></div>
        </div>`;

    if (txns.length > 0) {
        html += `<div class="detail-section"><h4>Transaction History (${txns.length} total)</h4>
            <table class="data-table compact"><thead><tr><th>Book</th><th>Issue Date</th><th>Due Date</th><th>Return Date</th><th>Status</th></tr></thead><tbody>`;
        [...txns].sort((a, b) => b.id - a.id).slice(0, 10).forEach(t => {
            const book = getBook(t.bookId);
            const overdueDays = !t.returnDate ? daysBetween(t.dueDate, today()) : 0;
            const status = t.returnDate ? 'Returned' : (overdueDays > 0 ? 'Overdue' : 'Active');
            html += `<tr>
                <td>${book ? escHtml(book.title) : 'Unknown'}</td>
                <td>${formatDate(t.issueDate)}</td>
                <td>${formatDate(t.dueDate)}</td>
                <td>${formatDate(t.returnDate)}</td>
                <td><span class="status-badge ${status.toLowerCase()}">${status}</span></td>
            </tr>`;
        });
        html += '</tbody></table></div>';
    }

    document.getElementById('memberDetailContent').innerHTML = html;
    openModal('memberDetailModal');
}

function deleteMember(id) {
    const member = getMember(id);
    if (!member) return;
    const activeTxns = DB.transactions.filter(t => t.memberId === id && !t.returnDate);
    if (activeTxns.length > 0) {
        showToast(`Cannot delete — member has ${activeTxns.length} book(s) currently issued!`, 'error');
        return;
    }
    const pendingFines = getMemberPendingFines(id);
    if (pendingFines > 0) {
        showToast(`Cannot delete — member has ₹${pendingFines} in pending fines!`, 'error');
        return;
    }
    showConfirm('Delete Member', `Are you sure you want to delete "${member.name}"?`, () => {
        let members = DB.members;
        members = members.filter(m => m.id !== id);
        DB.members = members;
        showToast('Member deleted', 'success');
        refreshMembers();
    });
}

// ===== ISSUE / RETURN =====
function refreshIssuePage() {
    // Populate member dropdown
    const memberSelect = document.getElementById('issueMember');
    const members = DB.members;
    memberSelect.innerHTML = '<option value="">Select Member...</option>';
    members.forEach(m => {
        const issued = getMemberIssuedCount(m.id);
        const disabled = issued >= m.maxBooks;
        memberSelect.innerHTML += `<option value="${m.id}" ${disabled ? 'disabled' : ''}>
            ${m.name} (M${String(m.id).padStart(4, '0')})${disabled ? ' — Max limit reached' : ''}
        </option>`;
    });

    // Populate book dropdown (only available books)
    const bookSelect = document.getElementById('issueBook');
    const books = DB.books;
    bookSelect.innerHTML = '<option value="">Select Book...</option>';
    books.forEach(b => {
        const avail = getAvailableCopies(b.id);
        bookSelect.innerHTML += `<option value="${b.id}" ${avail <= 0 ? 'disabled' : ''}>
            ${b.title} — ${b.author} ${avail <= 0 ? '(No copies available)' : `(${avail} available)`}
        </option>`;
    });

    // Set default dates
    document.getElementById('issueDate').value = today();
    const due = new Date();
    due.setDate(due.getDate() + DEFAULT_DUE_DAYS);
    document.getElementById('dueDate').value = due.toISOString().split('T')[0];

    document.getElementById('returnDate').value = today();

    // Populate return dropdown
    const returnSelect = document.getElementById('returnTransaction');
    const activeTxns = DB.transactions.filter(t => !t.returnDate);
    returnSelect.innerHTML = '<option value="">Select an issued book...</option>';
    activeTxns.forEach(t => {
        const book = getBook(t.bookId);
        const member = getMember(t.memberId);
        returnSelect.innerHTML += `<option value="${t.id}">
            ${book ? book.title : '?'} → ${member ? member.name : '?'} (Due: ${formatDate(t.dueDate)})
        </option>`;
    });
}

// Show info on member selection
document.getElementById('issueMember').addEventListener('change', () => {
    const memberId = parseInt(document.getElementById('issueMember').value);
    if (!memberId) { document.getElementById('issueInfo').style.display = 'none'; return; }
    const member = getMember(memberId);
    const issued = getMemberIssuedCount(memberId);
    const fines = getMemberPendingFines(memberId);

    let infoText = `${member.name}: ${issued}/${member.maxBooks} books issued.`;
    if (fines > 0) infoText += ` Pending fines: ₹${fines}.`;

    document.getElementById('issueInfoText').textContent = infoText;
    document.getElementById('issueInfo').style.display = 'flex';
});

// Issue form
document.getElementById('issueForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const memberId = parseInt(document.getElementById('issueMember').value);
    const bookId = parseInt(document.getElementById('issueBook').value);
    const issueDate = document.getElementById('issueDate').value;
    const dueDate = document.getElementById('dueDate').value;

    if (!memberId || !bookId) { showToast('Please select both a member and a book', 'error'); return; }

    const member = getMember(memberId);
    const book = getBook(bookId);

    // Validation checks
    if (getMemberIssuedCount(memberId) >= member.maxBooks) {
        showToast(`${member.name} has reached the maximum book limit (${member.maxBooks})`, 'error');
        return;
    }

    if (getAvailableCopies(bookId) <= 0) {
        showToast(`No copies of "${book.title}" are available`, 'error');
        return;
    }

    // Check if same member already has this book
    const alreadyHas = DB.transactions.some(t => t.memberId === memberId && t.bookId === bookId && !t.returnDate);
    if (alreadyHas) {
        showToast(`${member.name} already has a copy of "${book.title}"`, 'error');
        return;
    }

    if (daysBetween(issueDate, dueDate) < 1) {
        showToast('Due date must be after issue date', 'error');
        return;
    }

    // Check for unpaid fines
    const pendingFines = getMemberPendingFines(memberId);
    if (pendingFines > 0) {
        showToast(`Warning: ${member.name} has ₹${pendingFines} in pending fines`, 'warning');
    }

    const txns = DB.transactions;
    const txn = {
        id: DB.nextId('transactions'),
        bookId,
        memberId,
        issueDate,
        dueDate,
        returnDate: null,
        fine: 0,
        finePaid: false
    };
    txns.push(txn);
    DB.transactions = txns;

    showToast(`"${book.title}" issued to ${member.name}`, 'success');
    document.getElementById('issueForm').reset();
    refreshIssuePage();
});

// Return: show summary on selection
document.getElementById('returnTransaction').addEventListener('change', () => {
    const txnId = parseInt(document.getElementById('returnTransaction').value);
    const summary = document.getElementById('returnSummary');
    if (!txnId) { summary.style.display = 'none'; return; }

    const txn = DB.transactions.find(t => t.id === txnId);
    if (!txn) return;
    const book = getBook(txn.bookId);
    const member = getMember(txn.memberId);
    const retDate = document.getElementById('returnDate').value || today();
    const overdueDays = Math.max(0, daysBetween(txn.dueDate, retDate));
    const fine = overdueDays * FINE_RATE;

    document.getElementById('retBook').textContent = book ? book.title : '?';
    document.getElementById('retMember').textContent = member ? member.name : '?';
    document.getElementById('retDue').textContent = formatDate(txn.dueDate);
    document.getElementById('retOverdue').textContent = overdueDays > 0 ? `${overdueDays} day(s)` : 'None';
    document.getElementById('retFine').textContent = fine > 0 ? `₹${fine}` : '₹0';

    summary.style.display = 'block';
});

document.getElementById('returnDate').addEventListener('change', () => {
    // Re-trigger summary calculation
    document.getElementById('returnTransaction').dispatchEvent(new Event('change'));
});

// Return form
document.getElementById('returnForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const txnId = parseInt(document.getElementById('returnTransaction').value);
    if (!txnId) { showToast('Please select an issued book', 'error'); return; }

    const txns = DB.transactions;
    const idx = txns.findIndex(t => t.id === txnId);
    if (idx === -1) return;

    const retDate = document.getElementById('returnDate').value || today();
    const overdueDays = Math.max(0, daysBetween(txns[idx].dueDate, retDate));
    const fine = overdueDays * FINE_RATE;

    txns[idx].returnDate = retDate;
    txns[idx].fine = fine;
    txns[idx].finePaid = false;
    DB.transactions = txns;

    const book = getBook(txns[idx].bookId);
    const member = getMember(txns[idx].memberId);

    if (fine > 0) {
        showToast(`Book returned. Fine of ₹${fine} applied for ${overdueDays} overdue day(s)`, 'warning');
    } else {
        showToast(`"${book ? book.title : 'Book'}" returned by ${member ? member.name : 'member'}`, 'success');
    }

    document.getElementById('returnForm').reset();
    document.getElementById('returnSummary').style.display = 'none';
    refreshIssuePage();
});

// ===== TRANSACTIONS =====
function refreshTransactions() {
    const txns = DB.transactions;
    const search = document.getElementById('txnSearch').value.toLowerCase();
    const type = document.getElementById('txnType').value;
    const status = document.getElementById('txnStatus').value;

    let filtered = [...txns].sort((a, b) => b.id - a.id);

    filtered = filtered.filter(t => {
        const book = getBook(t.bookId);
        const member = getMember(t.memberId);
        if (search) {
            const haystack = `${book ? book.title : ''} ${member ? member.name : ''} ${t.id}`.toLowerCase();
            if (!haystack.includes(search)) return false;
        }
        if (type === 'issue' && t.returnDate) return false;
        if (type === 'return' && !t.returnDate) return false;
        if (status === 'active' && t.returnDate) return false;
        if (status === 'returned' && !t.returnDate) return false;
        if (status === 'overdue') {
            if (t.returnDate) return false;
            if (daysBetween(t.dueDate, today()) <= 0) return false;
        }
        return true;
    });

    const tbody = document.getElementById('txnBody');
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-row">No transactions found</td></tr>';
    } else {
        tbody.innerHTML = filtered.map(t => {
            const book = getBook(t.bookId);
            const member = getMember(t.memberId);
            let statusText, statusClass;
            if (t.returnDate) {
                statusText = 'Returned';
                statusClass = 'returned';
            } else {
                const overdue = daysBetween(t.dueDate, today());
                if (overdue > 0) {
                    statusText = `Overdue (${overdue}d)`;
                    statusClass = 'overdue';
                } else {
                    statusText = 'Active';
                    statusClass = 'active';
                }
            }
            const fineAmt = t.returnDate ? t.fine : (daysBetween(t.dueDate, today()) > 0 ? daysBetween(t.dueDate, today()) * FINE_RATE : 0);

            return `<tr>
                <td><code>T${String(t.id).padStart(4, '0')}</code></td>
                <td>${book ? escHtml(book.title) : '?'}</td>
                <td>${member ? escHtml(member.name) : '?'}</td>
                <td>${formatDate(t.issueDate)}</td>
                <td>${formatDate(t.dueDate)}</td>
                <td>${formatDate(t.returnDate)}</td>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td>${fineAmt > 0 ? `<span class="text-danger">₹${fineAmt}</span>` : '₹0'}</td>
            </tr>`;
        }).join('');
    }
}

['txnSearch', 'txnType', 'txnStatus'].forEach(id => {
    document.getElementById(id).addEventListener('input', refreshTransactions);
    document.getElementById(id).addEventListener('change', refreshTransactions);
});

// ===== FINES =====
function refreshFines() {
    const txns = DB.transactions;

    // Pending fines: returned with unpaid fines + currently overdue
    let pendingRows = [];
    let totalPending = 0;

    // Returned books with unpaid fines
    txns.filter(t => t.returnDate && t.fine > 0 && !t.finePaid).forEach(t => {
        const book = getBook(t.bookId);
        const member = getMember(t.memberId);
        pendingRows.push({
            txnId: t.id,
            member: member ? member.name : '?',
            book: book ? book.title : '?',
            daysOverdue: '—',
            fine: t.fine,
            status: 'Returned (unpaid)',
            returned: true
        });
        totalPending += t.fine;
    });

    // Currently overdue
    txns.filter(t => !t.returnDate && daysBetween(t.dueDate, today()) > 0).forEach(t => {
        const book = getBook(t.bookId);
        const member = getMember(t.memberId);
        const days = daysBetween(t.dueDate, today());
        const fine = days * FINE_RATE;
        pendingRows.push({
            txnId: t.id,
            member: member ? member.name : '?',
            book: book ? book.title : '?',
            daysOverdue: days,
            fine: fine,
            status: 'Currently Overdue',
            returned: false
        });
        totalPending += fine;
    });

    document.getElementById('fines-totalPending').textContent = `₹${totalPending}`;

    // Total collected
    const payments = DB.finePayments;
    let totalCollected = 0;
    payments.forEach(p => totalCollected += p.amount);
    document.getElementById('fines-totalCollected').textContent = `₹${totalCollected}`;

    // Pending fines table
    const finesBody = document.getElementById('finesBody');
    if (pendingRows.length === 0) {
        finesBody.innerHTML = '<tr><td colspan="6" class="empty-row">No pending fines 🎉</td></tr>';
    } else {
        finesBody.innerHTML = pendingRows.map(r => `<tr>
            <td>${escHtml(r.member)}</td>
            <td>${escHtml(r.book)}</td>
            <td>${r.daysOverdue}</td>
            <td class="text-danger">₹${r.fine}</td>
            <td><span class="status-badge ${r.returned ? 'pending' : 'overdue'}">${r.status}</span></td>
            <td>${r.returned ? `<button class="btn btn-sm btn-primary" onclick="payFine(${r.txnId})">
                <span class="material-icons-outlined" style="font-size:1rem">paid</span> Pay
            </button>` : '<span style="color:var(--text-muted);font-size:0.8rem;">Return first</span>'}</td>
        </tr>`).join('');
    }

    // Fine history
    const histBody = document.getElementById('fineHistoryBody');
    if (payments.length === 0) {
        histBody.innerHTML = '<tr><td colspan="5" class="empty-row">No payments recorded</td></tr>';
    } else {
        histBody.innerHTML = [...payments].sort((a, b) => b.id - a.id).map(p => `<tr>
            <td><code>P${String(p.id).padStart(4, '0')}</code></td>
            <td>${escHtml(p.memberName)}</td>
            <td>₹${p.amount}</td>
            <td>${formatDate(p.date)}</td>
            <td>${escHtml(p.method)}</td>
        </tr>`).join('');
    }
}

function payFine(txnId) {
    const txn = DB.transactions.find(t => t.id === txnId);
    if (!txn) return;
    const book = getBook(txn.bookId);
    const member = getMember(txn.memberId);

    document.getElementById('payFineTxnId').value = txnId;
    document.getElementById('payFineMember').textContent = member ? member.name : '?';
    document.getElementById('payFineBook').textContent = book ? book.title : '?';
    document.getElementById('payFineAmount').textContent = `₹${txn.fine}`;

    openModal('payFineModal');
}

document.getElementById('payFineForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const txnId = parseInt(document.getElementById('payFineTxnId').value);
    const method = document.getElementById('payFineMethod').value;

    const txns = DB.transactions;
    const idx = txns.findIndex(t => t.id === txnId);
    if (idx === -1) return;

    const member = getMember(txns[idx].memberId);

    // Record payment
    const payments = DB.finePayments;
    payments.push({
        id: DB.nextId('finePayments'),
        txnId,
        memberName: member ? member.name : '?',
        amount: txns[idx].fine,
        date: today(),
        method
    });
    DB.finePayments = payments;

    // Mark fine as paid
    txns[idx].finePaid = true;
    DB.transactions = txns;

    closeModal('payFineModal');
    showToast(`Fine of ₹${txns[idx].fine} paid via ${method}`, 'success');
    refreshFines();
});

// ===== REPORTS =====
let genreChartInstance = null;
let monthlyChartInstance = null;

function refreshReports() {
    const books = DB.books;
    const txns = DB.transactions;
    const members = DB.members;

    // Genre distribution
    const genreCount = {};
    books.forEach(b => {
        genreCount[b.genre] = (genreCount[b.genre] || 0) + b.copies;
    });

    if (genreChartInstance) genreChartInstance.destroy();
    const genreCtx = document.getElementById('genreChart').getContext('2d');
    const genreLabels = Object.keys(genreCount);
    const genreData = Object.values(genreCount);
    const colors = ['#4f46e5', '#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316', '#6366f1'];

    genreChartInstance = new Chart(genreCtx, {
        type: 'doughnut',
        data: {
            labels: genreLabels.length > 0 ? genreLabels : ['No Data'],
            datasets: [{
                data: genreData.length > 0 ? genreData : [1],
                backgroundColor: genreLabels.length > 0 ? colors.slice(0, genreLabels.length) : ['#e2e8f0'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { font: { family: 'Inter', size: 12 } } }
            }
        }
    });

    // Monthly transactions (last 6 months)
    const monthLabels = [];
    const issueData = [];
    const returnData = [];
    for (let i = 5; i >= 0; i--) {
        const d = new Date();
        d.setMonth(d.getMonth() - i);
        const label = d.toLocaleDateString('en-IN', { month: 'short', year: '2-digit' });
        const ym = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        monthLabels.push(label);
        issueData.push(txns.filter(t => t.issueDate && t.issueDate.startsWith(ym)).length);
        returnData.push(txns.filter(t => t.returnDate && t.returnDate.startsWith(ym)).length);
    }

    if (monthlyChartInstance) monthlyChartInstance.destroy();
    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
    monthlyChartInstance = new Chart(monthlyCtx, {
        type: 'bar',
        data: {
            labels: monthLabels,
            datasets: [
                { label: 'Issues', data: issueData, backgroundColor: '#818cf8', borderRadius: 6 },
                { label: 'Returns', data: returnData, backgroundColor: '#10b981', borderRadius: 6 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { font: { family: 'Inter', size: 12 } } } },
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } },
                x: { grid: { display: false } }
            }
        }
    });

    // Top borrowed books
    const bookBorrowCount = {};
    txns.forEach(t => {
        bookBorrowCount[t.bookId] = (bookBorrowCount[t.bookId] || 0) + 1;
    });
    const topBooks = Object.entries(bookBorrowCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    const topBooksBody = document.getElementById('topBooksBody');
    if (topBooks.length === 0) {
        topBooksBody.innerHTML = '<tr><td colspan="3" class="empty-row">No data yet</td></tr>';
    } else {
        topBooksBody.innerHTML = topBooks.map(([bId, count], i) => {
            const book = getBook(parseInt(bId));
            return `<tr><td>${i + 1}</td><td>${book ? escHtml(book.title) : '?'}</td><td>${count}</td></tr>`;
        }).join('');
    }

    // Most active members
    const memberTxnCount = {};
    txns.forEach(t => {
        memberTxnCount[t.memberId] = (memberTxnCount[t.memberId] || 0) + 1;
    });
    const topMembers = Object.entries(memberTxnCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    const topMembersBody = document.getElementById('topMembersBody');
    if (topMembers.length === 0) {
        topMembersBody.innerHTML = '<tr><td colspan="3" class="empty-row">No data yet</td></tr>';
    } else {
        topMembersBody.innerHTML = topMembers.map(([mId, count], i) => {
            const member = getMember(parseInt(mId));
            return `<tr><td>${i + 1}</td><td>${member ? escHtml(member.name) : '?'}</td><td>${count}</td></tr>`;
        }).join('');
    }
}

// ===== QUICK ACTIONS =====
document.getElementById('quickActionBtn').addEventListener('click', () => openModal('quickActionModal'));

document.getElementById('qaAddBook').addEventListener('click', () => {
    closeModal('quickActionModal');
    navigateTo('catalog');
    setTimeout(() => document.getElementById('addBookBtn').click(), 100);
});

document.getElementById('qaAddMember').addEventListener('click', () => {
    closeModal('quickActionModal');
    navigateTo('members');
    setTimeout(() => document.getElementById('addMemberBtn').click(), 100);
});

document.getElementById('qaIssueBook').addEventListener('click', () => {
    closeModal('quickActionModal');
    navigateTo('issue');
});

document.getElementById('qaReturnBook').addEventListener('click', () => {
    closeModal('quickActionModal');
    navigateTo('issue');
});

document.getElementById('qaResetData').addEventListener('click', () => {
    closeModal('quickActionModal');
    showConfirm('Reset All Data', 'This will permanently delete all books, members, transactions and fines. Are you sure?', () => {
        DB.clearAll();
        showToast('All data has been reset', 'success');
        navigateTo('dashboard');
    });
});

// ===== SAMPLE DATA =====
document.getElementById('qaLoadSample').addEventListener('click', () => {
    closeModal('quickActionModal');
    if (DB.books.length > 0) {
        showConfirm('Load Sample Data', 'This will add sample data to your existing library. Continue?', loadSampleData);
    } else {
        loadSampleData();
    }
});

function loadSampleData() {
    // Sample books
    const sampleBooks = [
        { title: 'The Great Gatsby', author: 'F. Scott Fitzgerald', isbn: '978-0-7432-7356-5', genre: 'Fiction', publisher: 'Scribner', year: 1925, copies: 3, location: 'Rack A-1' },
        { title: 'Clean Code', author: 'Robert C. Martin', isbn: '978-0-13-235088-4', genre: 'Technology', publisher: 'Prentice Hall', year: 2008, copies: 2, location: 'Rack B-2' },
        { title: 'Sapiens', author: 'Yuval Noah Harari', isbn: '978-0-06-231609-7', genre: 'History', publisher: 'Harper', year: 2015, copies: 4, location: 'Rack C-1' },
        { title: 'A Brief History of Time', author: 'Stephen Hawking', isbn: '978-0-553-10953-5', genre: 'Science', publisher: 'Bantam Books', year: 1988, copies: 2, location: 'Rack D-3' },
        { title: 'To Kill a Mockingbird', author: 'Harper Lee', isbn: '978-0-06-112008-4', genre: 'Fiction', publisher: 'J.B. Lippincott', year: 1960, copies: 5, location: 'Rack A-2' },
        { title: 'Introduction to Algorithms', author: 'Thomas H. Cormen', isbn: '978-0-262-03384-8', genre: 'Technology', publisher: 'MIT Press', year: 2009, copies: 3, location: 'Rack B-1' },
        { title: 'The Republic', author: 'Plato', isbn: '978-0-14-044914-6', genre: 'Philosophy', publisher: 'Penguin Classics', year: -380, copies: 2, location: 'Rack E-1' },
        { title: 'Steve Jobs', author: 'Walter Isaacson', isbn: '978-1-4516-4853-9', genre: 'Biography', publisher: 'Simon & Schuster', year: 2011, copies: 2, location: 'Rack C-3' },
        { title: 'The Alchemist', author: 'Paulo Coelho', isbn: '978-0-06-112241-5', genre: 'Fiction', publisher: 'HarperOne', year: 1988, copies: 3, location: 'Rack A-3' },
        { title: 'Operating System Concepts', author: 'Abraham Silberschatz', isbn: '978-1-119-80052-0', genre: 'Technology', publisher: 'Wiley', year: 2021, copies: 4, location: 'Rack B-3' },
        { title: 'Pride and Prejudice', author: 'Jane Austen', isbn: '978-0-14-143951-8', genre: 'Literature', publisher: 'Penguin Classics', year: 1813, copies: 3, location: 'Rack A-4' },
        { title: 'Oxford English Dictionary', author: 'Oxford University Press', isbn: '978-0-19-861186-8', genre: 'Reference', publisher: 'OUP', year: 2010, copies: 1, location: 'Reference Desk' },
    ];

    const books = DB.books;
    const existingISBNs = new Set(books.map(b => b.isbn));
    sampleBooks.forEach(sb => {
        if (!existingISBNs.has(sb.isbn)) {
            sb.id = DB.nextId('books');
            sb.addedDate = today();
            books.push(sb);
        }
    });
    DB.books = books;

    // Sample members
    const sampleMembers = [
        { name: 'Aarav Sharma', type: 'Student', email: 'aarav.sharma@university.edu', phone: '9876543210', maxBooks: 3 },
        { name: 'Priya Patel', type: 'Student', email: 'priya.patel@university.edu', phone: '9876543211', maxBooks: 3 },
        { name: 'Dr. Meera Krishnan', type: 'Faculty', email: 'meera.k@university.edu', phone: '9876543212', maxBooks: 10 },
        { name: 'Rohan Gupta', type: 'Student', email: 'rohan.g@university.edu', phone: '9876543213', maxBooks: 3 },
        { name: 'Anita Desai', type: 'Staff', email: 'anita.d@university.edu', phone: '9876543214', maxBooks: 5 },
        { name: 'Vikram Singh', type: 'External', email: 'vikram.singh@gmail.com', phone: '9876543215', maxBooks: 2 },
    ];

    const members = DB.members;
    const existingEmails = new Set(members.map(m => m.email));
    sampleMembers.forEach(sm => {
        if (!existingEmails.has(sm.email)) {
            sm.id = DB.nextId('members');
            sm.joinDate = today();
            members.push(sm);
        }
    });
    DB.members = members;

    // Sample transactions — some active, some returned, some overdue
    const allBooks = DB.books;
    const allMembers = DB.members;

    if (allBooks.length >= 6 && allMembers.length >= 4) {
        const txns = DB.transactions;
        const sampleTxns = [
            // Returned on time (past)
            { bookIdx: 0, memberIdx: 0, issueDaysAgo: 30, dueDaysAgo: 16, returnDaysAgo: 18, fine: 0 },
            { bookIdx: 2, memberIdx: 1, issueDaysAgo: 25, dueDaysAgo: 11, returnDaysAgo: 10, fine: 0 },
            // Returned late (with fine)
            { bookIdx: 4, memberIdx: 3, issueDaysAgo: 28, dueDaysAgo: 14, returnDaysAgo: 7, fine: 14 },
            // Currently active (not overdue)
            { bookIdx: 1, memberIdx: 0, issueDaysAgo: 5, dueDaysFromNow: 9, active: true },
            { bookIdx: 5, memberIdx: 2, issueDaysAgo: 3, dueDaysFromNow: 11, active: true },
            { bookIdx: 3, memberIdx: 1, issueDaysAgo: 7, dueDaysFromNow: 7, active: true },
            // Currently overdue
            { bookIdx: 0, memberIdx: 3, issueDaysAgo: 20, dueDaysAgo: 6, active: true },
            { bookIdx: 8, memberIdx: 4, issueDaysAgo: 22, dueDaysAgo: 8, active: true },
        ];

        sampleTxns.forEach(st => {
            const book = allBooks[st.bookIdx];
            const member = allMembers[st.memberIdx];
            if (!book || !member) return;

            // Don't create duplicates
            if (st.active && txns.some(t => t.bookId === book.id && t.memberId === member.id && !t.returnDate)) return;

            const issueDate = new Date();
            issueDate.setDate(issueDate.getDate() - st.issueDaysAgo);

            const dueDate = new Date();
            if (st.dueDaysAgo !== undefined) {
                dueDate.setDate(dueDate.getDate() - st.dueDaysAgo);
            } else if (st.dueDaysFromNow !== undefined) {
                dueDate.setDate(dueDate.getDate() + st.dueDaysFromNow);
            }

            const txn = {
                id: DB.nextId('transactions'),
                bookId: book.id,
                memberId: member.id,
                issueDate: issueDate.toISOString().split('T')[0],
                dueDate: dueDate.toISOString().split('T')[0],
                returnDate: null,
                fine: 0,
                finePaid: false
            };

            if (!st.active) {
                const returnDate = new Date();
                returnDate.setDate(returnDate.getDate() - st.returnDaysAgo);
                txn.returnDate = returnDate.toISOString().split('T')[0];
                txn.fine = st.fine || 0;
                txn.finePaid = st.fine === 0;
            }

            txns.push(txn);
        });
        DB.transactions = txns;
    }

    showToast('Sample data loaded! 📚', 'success');
    navigateTo('dashboard');
}

// ===== GLOBAL SEARCH =====
document.getElementById('globalSearch').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value.trim().toLowerCase();
        if (!query) return;

        // Check books
        const book = DB.books.find(b =>
            b.title.toLowerCase().includes(query) ||
            b.author.toLowerCase().includes(query) ||
            b.isbn.toLowerCase().includes(query)
        );
        if (book) {
            navigateTo('catalog');
            document.getElementById('catalogSearch').value = query;
            refreshCatalog();
            return;
        }

        // Check members
        const member = DB.members.find(m =>
            m.name.toLowerCase().includes(query) ||
            m.email.toLowerCase().includes(query)
        );
        if (member) {
            navigateTo('members');
            document.getElementById('memberSearch').value = query;
            refreshMembers();
            return;
        }

        // Default: search catalog
        navigateTo('catalog');
        document.getElementById('catalogSearch').value = query;
        refreshCatalog();
    }
});

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    navigateTo('dashboard');
});
