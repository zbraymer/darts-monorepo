Here’s a step-by-step guide for building the backend for your dart scoring system, starting with "around the world":

---

### **1. Define the Backend Architecture**
- **Language**: Python with a framework like **FastAPI** (lightweight, async-friendly).
- **Database**: SQLite for simplicity during development, with the option to switch to PostgreSQL for scalability.
- **Data Models**:
  - **Player**: For tracking individual players.
  - **Game**: Stores game metadata (type, players, status).
  - **Throw**: Logs each dart throw with coordinates, timestamp, and outcome.

---

### **2. Core Functionalities**
For "around the world," the main backend responsibilities are:
1. **Game Management**:
   - Start a new game.
   - Add/remove players.
   - Progress tracking (e.g., target numbers hit for each player).

2. **Score Mapping**:
   - Accept coordinates from the frontend.
   - Map coordinates to board segments (1–20, doubles, triples, bullseye).

3. **Statistics Tracking**:
   - Store each throw and its outcome.
   - Compute statistics like throws per target.

---

### **3. Database Schema Design**
Here’s an initial schema:

#### Tables
- **players**
  - `id`: Primary Key
  - `name`: String
  - `created_at`: Timestamp

- **games**
  - `id`: Primary Key
  - `type`: Enum ("around_the_world", "501", "301")
  - `status`: Enum ("in_progress", "completed")
  - `created_at`: Timestamp

- **throws**
  - `id`: Primary Key
  - `game_id`: Foreign Key to `games`
  - `player_id`: Foreign Key to `players`
  - `target`: Integer (expected target)
  - `result`: Boolean (hit or miss)
  - `coordinates`: JSON (x, y for mapping clicks)
  - `timestamp`: Timestamp

---

### **4. API Design**
Use REST or GraphQL endpoints to interact with the backend.

#### Sample Endpoints for "Around the World":
- **POST /game/start**
  - Start a new game.
  - Request: `{ "type": "around_the_world", "players": ["Player1", "Player2"] }`
  - Response: `{ "game_id": 1, "status": "in_progress" }`

- **POST /game/{game_id}/throw**
  - Log a throw.
  - Request: `{ "player_id": 1, "coordinates": { "x": 123, "y": 456 } }`
  - Response: `{ "target": 1, "result": true }`

- **GET /game/{game_id}/progress**
  - Get the current status of the game.
  - Response: `{ "player_progress": { "Player1": 5, "Player2": 3 } }`

- **GET /player/{player_id}/statistics**
  - Fetch lifetime statistics for a player.
  - Response: `{ "average_throws_per_target": 3.4, "double_percentage": 45.0 }`

---

### **5. Initial Implementation for "Around the World"**
Start with:
1. **Player Management**:
   - CRUD operations for players.
2. **Game Logic**:
   - Create a new game.
   - Track player progress.
3. **Score Mapping**:
   - Implement a function to map (x, y) coordinates to board segments using a simple 2D geometry approach.

---

### **6. Plan Frontend Integration**
Although focusing on the backend now, keep the following in mind:
- Frontend will send dartboard clicks as (x, y) coordinates.
- Use clear API contracts (input/output JSON formats).

---

### Next Steps:
1. Set up a **FastAPI** project with the database schema.
2. Implement the `/game/start` and `/game/{game_id}/throw` endpoints.
3. Write a function to map (x, y) to board segments.
4. Test the core flow for "around the world."

Would you like help starting with the FastAPI setup or the scoring logic?