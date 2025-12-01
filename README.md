# Saudi Estate – Real Estate Platform

## Project Description
**Saudi Estate** is a web-based real estate platform built with Django. It allows users to browse, filter, and explore property listings, while also enabling verified users to upload and manage their own properties. The platform focuses on clean UI/UX, document verification (title deed, ownership proof), responsive design, and seamless user interaction to bridge the gap between property owners and seekers.




## 🚀 Features List....


* **User Authentication & Authorization:** Secure registration, login, and logout with support for different user roles (Admin, User, Property Owner).
* **Property Owner Mode:** Users can upload, edit, and delete their own property listings directly through a dashboard.
* **Document Verification:** Upload system for title deeds, ownership proofs, and building licenses with verification status tracking (Pending / Approved / Rejected).
* **Advanced Search & Filtering:** Users can filter properties by city, price range, rooms, and property type.
* **Visit Requests:** Users can request a property visit by selecting preferred dates.
* **Inquiry System:** Built-in contact form for users to send inquiries directly to property owners.
* **Responsive Design:** Fully responsive UI/UX compatible with Desktop, Tablet, and Mobile devices.
* **Media Management:** Support for a main image, gallery images, and secure storage for property documents.
* **Pagination & Feedback:** Clean navigation with flash messages for success, errors, and confirmations.
* **Secure Configuration:** Secure handling of sensitive data using environment variables (`python-dotenv`).

---

## 👤 User Stories

* **As a Visitor**, I want to view the latest property listings on the homepage so I can explore options easily.
* **As a User**, I want to filter properties by city, price range, and number of rooms so I can find a suitable property.
* **As a User**, I want to register and log in so that I can access personalized features.
* **As a User**, I want to click on a property listing to view full details and photos.
* **As a Property Owner**, I want to upload my property with details, images, and ownership documents.
* **As a Property Owner**, I want to edit or delete my property listing so I can keep my information updated.
* **As a User**, I want to send an inquiry to the owner so I can ask questions about the property.
* **As a User**, I want to request a property visit so I can schedule a suitable time to view it.
* **As an Admin**, I want to review the uploaded documents so I can approve or reject a property listing.

---

## 📊 UML Diagram

The system involves the following key entities and their relationships.
Full Diagram: [📄 UML Diagram File](CLASS_DIAGRAM.png)

**Key Models:**
* `User` (AbstractUser extension or OneToOne link)
* `Property` (Main listing details)
* `PropertyImage` (Gallery images linked to Property)
* `Inquiry` (Messages from User to Property Owner)
* `VisitRequest` (Scheduling requests from User to Property Owner)

---

## 🎨 Wireframes

![Screenshot_2025-12-01_at_9 09 07_PM](https://github.com/user-attachments/assets/bc70bb66-a3ac-4adf-ad7d-7b488da04503)




![Screenshot_2025-12-01_at_9 08 35_PM](https://github.com/user-attachments/assets/d1f73f9d-919e-41e0-8b88-40e758e812c3)




![Screenshot_2025-12-01_at_9 08 18_PM](https://github.com/user-attachments/assets/b27f98ca-8d18-4283-8944-7d5df73947a1)




![Screenshot_2025-12-01_at_9 07 45_PM](https://github.com/user-attachments/assets/7706e741-f4e1-46f1-8360-7a9cf4903884)



* Homepage
* Add Property Form
* Login / Register Pages
* User Profile

