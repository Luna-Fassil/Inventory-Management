# HyperLink Inventory System

[UI design mockup](https://www.figma.com/design/LT2yhVPQxUzbOlMvply3Ip/Inventory-Managment-System-(Copy)?node-id=0-1&p=f&t=WaZxlNOoIfxaF1rW-0)


# HyperLink Inventory Management System

## Overview
The HyperLink Inventory Management System is a web-based application designed to streamline inventory management for a clothing store. The system allows employees to add, edit, view, and remove clothing items from the inventory. It includes features such as search functionality, filtering by attributes (e.g., color, brand, season), and role-based access control.

## Setup Instructions
To run the HyperLink Inventory Management System locally, follow these steps:


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LunaFassil/HyperLink.git
   cd HyperLink
2. **Install Dependencies**:
   Ensure you have Python and Flask installed. You can install Flask using pip:
   ```bash
   pip install Flask
3. **Run the Application**:
   Navigate to the project directory and run the Flask application:
   ```bash
   python inventory.py
4. **Access the Application**:
Open your web browser and go to http://127.0.0.1:5000/ to access the inventory management system.

## Features Implemented in Iteration 1
- **Add Clothing Items**: Users can add new clothing items to the inventory by specifying details such as name, color, quantity, and price.
- **Edit Quantity and Details**: Users can edit the quantity and other details of existing items.
- **View Stock**: Users can view the stock quantity and details of each clothing item.
- **Remove Clothing Items**: Users can remove items from the inventory.
- **Website Layout**: The website layout is designed with navigational icons, a search bar, filter panel, and sorting options.

## Known Gaps and Limitations
- **No Backend Storage**: Items disappear upon page refresh. A file system will be implemented to save inventory data.
- **No User Authentication**: Anyone can access or modify inventory, leading to potential security issues.
- **Search and Filtering**: The search bar and filter panel are not yet functional.
- **Data Validation**: Incorrect values (e.g., negative numbers) are not recognized or flagged.
- **Lack of Undo/History**: No version control system to undo accidental deletions or edits.

## Repository and Project Board
- **GitHub Repository**: [HyperLink](https://github.com/LunaFassil/HyperLink)
- **GitHub Project Board**: [Project Board](https://github.com/users/LunaFassil/projects/2)

## Challenges and Next Steps
### Challenges Encountered
- **Learning Flask**: Team members had no prior experience with Flask, requiring extensive research and practice.
- **Testing & Debugging**: Multiple rounds of testing were needed to address CORS errors, incorrect request handling, and data inconsistencies.
- **Version Control & Git Conflicts**: Some team members were unfamiliar with Git, leading to merge conflicts.

### Goals for Next Iteration
- **Backend Storage**: Implement a file system to save inventory data persistently.
- **User Authentication**: Develop a login system to restrict access to authorized users.
- **Search and Filtering**: Enable search functionality by item name or ID and make the filter panel functional.
- **Data Validation**: Add validation for user inputs to prevent errors.
- **Version Control**: Implement a system to track changes and allow undo functionality.

## Contributing
We welcome contributions to the HyperLink Inventory Management System. Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
