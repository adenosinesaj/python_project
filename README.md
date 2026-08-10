# manageHoise?
> *A Django-based web platform simplifying event planning and connecting vendors with customers.*

[![Live Demo](https://img.shields.io/badge/Live-Website-brightgreen)](https://python-project-sl6g.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/adenosinesaj/python_project)

---

## 🌐 Live Application
* **Website:** [python-project-sl6g.onrender.com](https://python-project-sl6g.onrender.com/)
* **Hosting Platform:** Render
* **Database Provider:** Supabase (PostgreSQL) / SQLite3 (Local)

**manageHoise?** is an online event planning and management web application built using Python and Django. In regions like Bangladesh, event planning heavily relies on manual efforts, which can be overwhelming and time-consuming. This project addresses those challenges by providing a centralized digital ecosystem for two distinct primary users: **Vendors** and **Customers**. Vendors can register, showcase, and manage event-related products and services (such as catering, decoration, or rental items), while customers can explore vendor offerings, manage shopping carts, complete orders, and view portfolios. By laying a solid digital foundation, **ManageHoise?** promotes paperless planning and empowers local small businesses.

---

# Home Page
<img width="1897" height="906" alt="Screenshot 2026-08-11 014451" src="https://github.com/user-attachments/assets/74cdf1e2-e101-42de-a359-af41534d122f" />

<img width="1899" height="913" alt="Screenshot 2026-08-11 014506" src="https://github.com/user-attachments/assets/033d0939-edc5-439a-9db0-ed53a636e04e" />

# Products
<img width="1902" height="908" alt="Screenshot 2026-08-11 014523" src="https://github.com/user-attachments/assets/5d764f61-7678-47ba-b031-861d65c686fa" />

# Portfolio
<img width="1904" height="906" alt="Screenshot 2026-08-11 014535" src="https://github.com/user-attachments/assets/4b81147c-5781-4c05-a330-e0e9ccb389bd" />

---

## 📌 Project Overview
* **Project Name:** ManageHoise?
* **Course:** Software Engineering Lab
* **Target Focus:** Event Planning & Management (Bangladesh & Urban Regions)
* **Architecture:** Django Model-View-Template (MVT)
* **Technology Stack:** Python, Django, HTML5, CSS3, Bootstrap, JavaScript, SQLite3 / PostgreSQL (Supabase)

---

## 📑 Table of Contents
1. [Introduction & Motivation](#-introduction--motivation)
2. [Problem Statement & Critical Challenges](#-problem-statement--critical-challenges)
3. [Social & Environmental Impact](#-social--environmental-impact)
4. [Key Features & User Roles](#-key-features--user-roles)
5. [System Architecture & Design](#-system-architecture--design)
6. [Tech Stack & Dependencies](#-tech-stack--dependencies)
7. [Database & ER Model](#-database--er-model)
8. [Installation & Setup](#-installation--setup)
9. [Future Roadmap](#-future-roadmap)
10. [Team Contributions](#-team-contributions)

---

## 🌿 Introduction & Motivation
Planning events manually creates coordination friction and user stress. **ManageHoise?** provides a centralized platform that bridges the gap between event organizers and service providers.

* **Centralized Discovery:** Provides a single portal to explore event services, compare vendors, and browse portfolios.
* **Digital Transformation:** Modernizes traditional event planning workflows through digital tools.
* **Local Vendor Empowerment:** Gives small and medium event vendors direct exposure to customers.

---

## 🚨 Problem Statement & Critical Challenges
Traditional event management suffers from fragmented communication, paper-based tracking, and limited visibility for local vendors

### Critical Challenges
* **Multi-User Architecture:** Designing a flexible system supporting separate permissions for Vendors and Customers.
* **Authentication & Authorization:** Securing user accounts and enforcing role-based access control.
* **State & Data Management:** Association of user-specific carts, portfolios, and historical orders.
* **Timeline Constraints:** Developing and testing core MVT workflows within the engineering sprint timeline.

---

## 🌱 Social & Environmental Impact
* **Paper Waste Reduction:** Promotes digital checklists, online order histories, and virtual product catalogs to reduce paper usage.
* **Economic Inclusivity:** Enables local small business vendors to register and expand their customer reach.
* **Enhanced Accessibility:** Centralizes event resources, allowing users to plan events remotely with lower search costs.

---

## 👥 Key Features & User Roles

### 🛍️ Vendors
* **Product & Service Management:** Add, update, and remove listings (catering, decor, rentals).
* **Vendor Profile:** Customize public profiles and display event portfolios (`Portfolio` model).

### 👤 Customers
* **Product Exploration:** Search and filter event listings by category or keywords.
* **Shopping Cart & Checkout:** Add items to cart, calculate totals, remove items, and place orders.
* **Order History:** View past orders and order statuses.
* **Profile Customization:** Edit personal details, profile picture, phone number, and bio.

### 🛡️ Admins
* **System Management:** Manage user accounts, vendor items, profiles, and order records via the Django Admin Panel.

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/adenosinesaj/python_project.git](https://github.com/adenosinesaj/python_project.git)
cd python_project

# 2. Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Set environment variables (Optional for local SQLite)
# export DATABASE_URL="postgresql://user:password@host:port/dbname"

# 5. Apply migrations & create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
