# ⚡ FlowGen - AI-Powered Workout Generator

An aesthetic, intelligent workout generator that creates customized exercise flows tailored to your energy. Based on your target muscle, difficulty level, and available time, the generator builds complete circuits, complete with warm-ups and cool-downs.

## 🚀 Live Demo
**[🎯 Click Here to See the Live App!]("Replace_this_text_with_your_vercel_url")** 
*(Don't forget to edit this file later and add your actual Vercel link here!)*

## 🛠️ Tech Stack
- **Frontend**: React (Vite) + Custom Vanilla CSS
- **Backend**: Python (Flask) + Gunicorn
- **Deployment Strategy**: Vercel (Frontend) & Render (Backend)

## 🏃‍♂️ Features
- **Predefined Circuits**: Jump straight into popular preset programs like *Phonk Pump HIIT*, *Matrix Mobility*, or *Vapor Core 300* from the stunning landing page.
- **Dynamic Generator**: Create custom, randomized workouts infinitely based on precise body targets and constraints.
- **Visuals Included**: Every single exercise automatically loads high-quality visual demonstrations.
- **Premium Design System**: Complete with glassmorphism overlays, premium typography, and an electric neon-orange aesthetic.

## 💻 Running Locally

To run this application on your own machine, you will need to run the frontend and backend simultaneously.

### 1. Start the Backend (API)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*The Flask API will start on port `10000` (i.e. `http://127.0.0.1:10000`)*

### 2. Start the Frontend (UI)
Open a brand new terminal, and run:
```bash
cd frontend
npm install
npm run dev
```
*The React app will start on port `5173` (i.e. `http://localhost:5173`)*

## 🌐 Deployment Details
The project is structurally ready for production deployment:
- **Backend**: The `requirements.txt` specifically includes `gunicorn` to support WSGI deployment on Render.
- **Frontend**: The React application grabs the API url via Vite Environment variables `import.meta.env.VITE_API_URL` to easily switch between Localhost and the Render Live Link.
