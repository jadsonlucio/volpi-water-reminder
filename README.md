# volpi-water-reminder

Application the reminder the user that he has to drink water.

# Running the backend

This documentation provides detailed instructions on how to set up and run "Water Reminder" Django project using a Virtual Environment (venv) on both Windows and Linux operating systems.

## Prerequisites

1. **Python**: Ensure that Python is installed on your system. You can download the latest version from the [official Python website](https://www.python.org/downloads/).

## Windows

### Step 1: Create and Activate Virtual Environment

1. Open a Command Prompt:

   - Press `Win + R`, type `cmd`, and press Enter.
   - Alternatively, search for "Command Prompt" in the Start menu.

2. Navigate to your "Water Reminder" project directory:

   ```sh
   cd path\to\your\water-reminder-project
   ```

3. Create a virtual environment:

   ```sh
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```sh
   venv\Scripts\activate
   ```

### Step 2: Install Dependencies and Run the Project

1. Install project dependencies using `pip`:

   ```sh
   pip install -r requirements.txt
   ```

2. Navigate to your Django project's directory (where `manage.py` is located).

3. Apply migrations:

   ```sh
   python manage.py migrate
   ```

4. Start the development server:

   ```sh
   python manage.py runserver
   ```

5. Access the "Water Reminder" app in your web browser at `http://127.0.0.1:8000`.

6. To deactivate the virtual environment, simply run:
   ```sh
   deactivate
   ```

## Linux

### Step 1: Create and Activate Virtual Environment

1. Open a terminal.

2. Navigate to your "Water Reminder" project directory:

   ```sh
   cd /path/to/your/water-reminder-project
   ```

3. Create a virtual environment:

   ```sh
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```sh
   source venv/bin/activate
   ```

### Step 2: Install Dependencies and Run the Project

1. Install project dependencies using `pip`:

   ```sh
   pip install -r requirements.txt
   ```

2. Navigate to your Django project's directory (where `manage.py` is located).

3. Apply migrations:

   ```sh
   python manage.py migrate
   ```

4. Start the development server:

   ```sh
   python manage.py runserver
   ```

5. Access the "Water Reminder" app in your web browser at `http://127.0.0.1:8000`.

6. To deactivate the virtual environment, simply run:
   ```sh
   deactivate
   ```

# Running the Frontend

This documentation provides comprehensive instructions on how to set up and run the frontend of your "Water Reminder" application built with Quasar and Vue 3.

## Prerequisites

1. **Node.js and npm**: Ensure that Node.js and npm (Node Package Manager) are installed on your system. You can download the latest version of Node.js from the [official Node.js website](https://nodejs.org/).

## Installation and Setup

### Step 1: Install Quasar CLI

1. Open a terminal.

2. Install the Quasar CLI globally using npm:
   ```sh
   npm install -g @quasar/cli
   ```

### Step 2: Clone the "Water Reminder" Frontend Repository

1. Open a terminal.

2. Navigate to the directory where you want to store the frontend code:
   ```sh
   cd /path/to/your/projects
   ```

### Step 3: Install Dependencies

1. Navigate to the cloned repository's directory:

   ```sh
   cd /path/to/your/water-reminder-project/frontend
   ```

2. Install project dependencies using npm:
   ```sh
   npm install
   ```

## Running the Frontend

### Step 1: Start the Development Server

1. In the terminal, run the following command to start the Quasar development server:

   ```sh
   quasar dev
   ```

2. Access the "Water Reminder" frontend in your web browser at `http://localhost:9001/#/login`.

### Step 2: Making Changes

1. Open your preferred code editor and navigate to the "Water Reminder" frontend directory.

2. Modify the Vue components and Quasar files according to your requirements.

3. The development server will automatically reload when you save changes.

### Step 3: Build for Production

1. To build the frontend for production, run:

   ```sh
   quasar build
   ```

2. The built files will be available in the `dist` directory.
