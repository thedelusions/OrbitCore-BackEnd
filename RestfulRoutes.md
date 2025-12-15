### 🔐 Authentication
- `POST /auth/register` — Create a new user account
- `POST /auth/login` — Authenticate user and return access token

---

### 👤 Users
- `GET /users/:id` — Get public user profile
- `GET /users/me/requests` — View my join requests

---

### 💡 Projects
- `GET /projects` — List all projects
- `POST /projects` — Create a new project
- `GET /projects/:id` — Get project details
- `PUT /projects/:id` — Update project (owner only)
- `DELETE /projects/:id` — Delete project (owner only)

#### Project Filters
- `GET /projects?status=open`
- `GET /projects?tag=AI`
- `GET /projects?sort=top`

---

### 👍 Votes
- `POST /projects/:id/votes` — Upvote or downvote a project
- `DELETE /projects/:id/votes` — Remove vote

---

### 💬 Comments
- `GET /projects/:id/comments` — List comments for a project
- `POST /projects/:id/comments` — Add a comment to a project
- `DELETE /projects/:id/comments/:commentId` — Delete comment (comment owner only)

---

### 📨 Join Requests
- `POST /projects/:id/requests` — Request to join a project
- `GET /projects/:id/requests` — View join requests (project owner only)
- `PUT /requests/:id` — Accept or reject join request