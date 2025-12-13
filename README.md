# MEN Stack Starter Template with Session Authentication

Welcome to the MEN Stack Starter Template! This template provides a foundational setup for building web applications using MongoDB, Express.js, and Node.js, complete with session authentication. This is ideal for students looking to kickstart their development projects.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Clone the Repository](#clone-the-repository)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Removing Git and Creating Your Own Repo](#removing-git-and-creating-your-own-repo)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- [Node.js](https://nodejs.org/) (LTS or later)
- [MongoDB](https://www.mongodb.com/) (make sure it's running)
- [Git](https://git-scm.com/) (for cloning the repository)

## Clone the Repository

To clone this repository, open your terminal and run:

```bash
git clone https://github.com/SEB-PT-6-Solutions/men-stack-session-auth-template.git YOUR_APP_NAME_HERE
```

## Installation
Navigate into the cloned directory:
```bash
cd YOUR_APP_NAME
```

Then, install the necessary dependencies:

```bash
npm i
```

## Environment Setup
```plaintext
MONGODB_URI=atlas_db_uri
SESSION_SECRET=your_secret_key
```
Replace `atlas_db_uri` with your desired database name and `your_secret_key` with a secure key.

## Removing Git and Creating Your Own Repo
To remove the existing Git history and create your own repository:

1. Remove the existing .git folder:
  ```bash
  rm -rf .git
  ```
2. Initialize a new Git repository:
  ```bash
  git init
  ```
3. Add all files to the new repository:
  ```bash
  git add .
  ```
4. Commit the changes
   ```bash
   git commit -m "Initial commit"
   ``` 
5. Create a new repository on GitHub (or any other platform) and follow the instructions to push your local repository.
  Make a new repository on [GitHub](https://github.com/) named `<your-project-name>`
  Now link your local project to your remote GitHub repo:
  ```bash
  git remote add origin https://github.com/<github-username>/YOUR_APP_NAME.git
  git push origin main
  ```

> 🚨 Do not copy the above command. It will not work. Your GitHub username will replace `<github-username>` (including the `<` and `>`) in the URL above.

## Running the application
```bash
npm run dev
```

## Features
- User registration and login with session management
- Basic CRUD operations
- Modular file structure
- Example routes and controllers
- Basic user model setup
- Middleware for templates and authorization
- Basic authentication flow

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Happy Coding!
