# National Parks Tracker

This project allows users to track their visits to U.S. National Parks.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Set up your MongoDB database
6. Create a `.env` file in the `backend` directory with your MongoDB details
7. Run the data import script: `python data/parks.py`

## Project Structure

- `data/`: Contains the raw CSV data file
- `frontend/`: Contains the Next.js frontend code
- `backend/`: Contains the Flask backend code and data import script
- `venv/`: Python virtual environment
