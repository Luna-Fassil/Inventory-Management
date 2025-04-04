# Developer Documentation

This document is intended to guide future developers in understanding the structure, responsibilities, and modification or extension of the system. It includes explanations of core features, system components, and code organization.

## Project Overview

HyperLink is a role-based inventory management system designed to streamline item tracking, user access, and administrative control in an organizational setting. It aims to make inventory tasks intuitive, efficient, and accessible to users with varying levels of permissions.

## Technologies Used  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python with Flask  
- **Testing:** PyTest & Flask’s test client  
- **Version Control:** Git & GitHub  
- **Video Tools:** ClipChamp (for final demo/tutorial)  

## Key Features  
- Role-based UI rendering (Admin, Manager, Employee access)  
- Add, edit, delete, and search inventory items  
- Filter items by category  
- Sort table columns dynamically  
- Export inventory as CSV  
- Input validation (e.g., no negative quantities)  
- Session and login system with secure access  
- Developer and user documentation included  
- Final demo video to showcase functionality  

## Target Users  
- Admins responsible for employee roles and system control  
- Managers and merchandisers needing efficient access to product data  
- Employees with limited, task-specific access  

## Problem Solved / Need Fulfilled  
HyperLink solves the problem of inefficient and unstructured inventory management systems by introducing a user-friendly, permission-based platform that’s easy to maintain and scale. It ensures that users can only access the features relevant to their roles, improving security, usability, and operational flow.