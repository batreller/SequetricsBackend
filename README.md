1. Create and Activate Virtual Environment

   **Windows (Command Prompt / CMD):**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

   **Linux (Bash):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install FFmpeg

   **For Windows:**

   1. **Download FFmpeg:** Go to a https://github.com/BtbN/FFmpeg-Builds/releases and download a stable build for Windows, currently it is ffmpeg-n8.0-latest-win64-gpl-8.0
   2. **Extract:** Extract the files to a permanent location (e.g., `C:\Program Files\ffmpeg`).
   3. **Add to PATH:** You must add the path to the `bin` folder (e.g., `C:\Program Files\ffmpeg\bin`) to your system's
   **PATH** environment variable via the System Properties interface.
   4. **Verify:** Open a **new CMD window** and run:
   ```bash
   ffmpeg -version
   ```

   **For Linux (Debian/Ubuntu):**

    * Install FFmpeg using the package manager:
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    * **Verify:**
        ```bash
        ffmpeg -version
        ```
3. Install Dependencies via requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
4. Verify Installation with Doctor Script

    * Run the doctor script from the root project directory:
    ```bash
    python doctor.py
    ```
5. Configure and Start Database

   **a. Start Database via Docker:**
    ```bash
    docker-compose up -d
    ```

   **b. Configure Environment Variables:**
    * Create .env file with content of .env.example and change the configuration

6. Run Alembic Migrations

    * Apply all migrations:
    ```bash
    alembic upgrade head
    ```
7. Start the FastAPI Server

    * Launch the application:
    ```bash
    uvicorn app.main:app --reload
    ```

   The server will be accessible at **http://127.0.0.1:8000**.