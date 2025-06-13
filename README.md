# 🧭 Prime Technologies - Internal Operations Dashboard

Welcome to the internal dashboard used by **Prime Technologies** to manage and monitor core operations, including product oversight, task management, user access, and analytics. Built with modern web technologies, this platform empowers teams with clear visibility and seamless control.

---

## 🌟 Overview

Designed for scale, speed, and simplicity — this dashboard enables Prime Technologies to:

- 📦 Manage Products and Inventory
- 📊 View Real-time Operational Analytics
- 🗂️ Organize Tasks via Kanban Workflow
- 👥 Handle Secure Team Authentication & Profiles
- 🔍 Search, Filter & Navigate with Lightning Fast Performance

Whether it's onboarding a product, checking performance stats, or assigning tasks — everything flows through this unified interface.

---

## ⚙️ Tech Stack

Built using the latest in frontend engineering to ensure reliability and responsiveness.

| Layer | Technology |
|-------|------------|
| Framework | **Next.js 15** |
| Language | **TypeScript** |
| Styling | **Tailwind CSS v4** |
| UI Library | **Shadcn-ui** |
| Form Handling | **React Hook Form + Zod** |
| State Management | **Zustand** |
| Auth | **Clerk** |
| Tables | **Tanstack Table + Dice UI** |
| Search Param State | **Nuqs** |
| UI Command Interface | **kbar (Cmd + K)** |
| Linting & Formatting | **ESLint, Prettier, Husky** |

---

## 🧩 App Pages

| Page | Description |
|------|-------------|
| **Sign Up / Sign In** | Secure multi-method authentication using Clerk |
| **Dashboard (Overview)** | KPI cards, graphs, and loading states via parallel routing |
| **Products** | Manage product listings with search, filters, pagination |
| **Add Product** | Form with full validation for adding new items |
| **Kanban Board** | Drag-and-drop task management with persistent state |
| **Profile** | Full user settings, password, and session control |
| **404 Not Found** | Graceful fallback for invalid routes |

---

## 🗂️ Feature-Oriented Directory Structure

## 📁 Directory Structure

```bash
src/
├── app/                     # Next.js App Router directory
│   ├── (auth)/             # Authentication routes (sign in, sign up)
│   ├── (dashboard)/        # Dashboard layout and pages
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   └── page.tsx
│   └── api/                # Backend API route handlers
│
├── components/             # Shared UI components
│   ├── ui/                 # Reusable UI elements (buttons, inputs, etc.)
│   └── layout/             # Layout components (header, sidebar, etc.)
│
├── features/               # Feature-specific modules
│   ├── product/            # Product management logic and UI
│   ├── tasks/              # Kanban board and task management
│   └── user/               # User profile and settings
│
├── lib/                    # Core utilities and configurations
│   ├── auth/               # Clerk auth configurations
│   ├── db/                 # Database integration and setup
│   └── utils/              # Shared utility functions
│
├── hooks/                  # Custom React hooks
│   └── use-debounce.ts
│
├── stores/                 # Zustand state management stores
│   └── dashboard-store.ts
│
└── types/                  # TypeScript global types
    └── index.ts
```
## 🚀 Getting Started

To get the project up and running locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/devkimudhalwadkar/primetech.git
cd primetech
```

### 2. Install Dependencies

```bash
pnpm install
```

> ℹ️ Note: The project uses `legacy-peer-deps=true`, already configured in `.npmrc` for compatibility.

### 3. Set Up Environment Variables

Create a local environment file by copying the example:

```bash
cp env.example.txt .env.local
```

Then, fill in `.env.local` with your required keys (e.g., Clerk API, database URL, etc.).

---

## 💻 Run the Application

Start the development server:

```bash
pnpm run dev
```

Now, open [http://localhost:3000](http://localhost:3000) in your browser to explore the Prime Technology Dashboard.

---

## ⚠️ Heads Up

After forking or cloning this project, be mindful of upstream changes. Pulling updates may introduce breaking changes. Always check commit history before syncing.

---

## 🛠 Maintained by

**Devki Mudhalwadkar**  
Built for internal use at **Prime Technology** to manage products, tasks, and operations from a centralized interface.

Repository: [https://github.com/devkimudhalwadkar/primetech](https://github.com/devkimudhalwadkar/primetech)

---

## 🥂 Cheers!

This dashboard is crafted with care to help businesses streamline their digital workflows. Contributions and improvements are always welcome!

