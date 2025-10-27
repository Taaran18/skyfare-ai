from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import pandas as pd
from ..utils.helpers import load_model, compute_duration

router = APIRouter()
model = load_model()

AIRLINES = [
    "IndiGo",
    "Air India",
    "Jet Airways",
    "SpiceJet",
    "Vistara",
    "GoAir",
    "Multiple carriers",
    "Air Asia",
    "Trujet",
]
SOURCES = ["Delhi", "Kolkata", "Mumbai", "Chennai", "Banglore"]
DESTINATIONS = ["Cochin", "Banglore", "Delhi", "Hyderabad", "Kolkata"]


@router.get("/", response_class=HTMLResponse)
def form():
    options_airline = "".join(f"<option value='{a}'>{a}</option>" for a in AIRLINES)
    options_source = "".join(f"<option value='{s}'>{s}</option>" for s in SOURCES)
    options_dest = "".join(f"<option value='{d}'>{d}</option>" for d in DESTINATIONS)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>SkyFareAI ✈️ — Flight Price Predictor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
        <style>
          body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #a78bfa, #f472b6, #60a5fa);
            background-size: 300% 300%;
            animation: gradientShift 8s ease infinite;
            transition: background 0.5s, color 0.5s;
          }}
          @keyframes gradientShift {{
            0% {{background-position: 0% 50%;}}
            50% {{background-position: 100% 50%;}}
            100% {{background-position: 0% 50%;}}
          }}
        </style>
      </head>

      <body class="dark:bg-gray-900 dark:text-gray-100 flex items-center justify-center min-h-screen transition-colors duration-500">
        <div class="backdrop-blur-xl bg-white/30 dark:bg-gray-800/40 border border-white/20 shadow-2xl rounded-3xl p-10 w-full max-w-2xl transition-all duration-500">
          
          <!-- Header Section -->
          <div class="text-center mb-8">
            <h1 class="text-4xl font-extrabold text-indigo-700 dark:text-indigo-300 inline-flex items-center justify-center gap-2">
              SkyFareAI <i data-feather="send" class="w-6 h-6 text-indigo-500 dark:text-indigo-400"></i>
            </h1>
            <p class="text-gray-700 dark:text-gray-400 mt-3">Predict your flight fare instantly ✈️</p>
          </div>

          <!-- Theme toggle button (top right corner inside card) -->
          <div class="absolute top-6 right-8">
            <button id="theme-toggle" onclick="toggleTheme()" class="p-2 rounded-md bg-indigo-100 dark:bg-gray-700 transition">
              <i id="theme-icon" data-feather="moon" class="w-5 h-5 text-indigo-600 dark:text-yellow-400"></i>
            </button>
          </div>

          <!-- Form -->
          <form method="post" action="/predict" class="grid grid-cols-2 gap-6">
            <div>
              <label>Airline</label>
              <select name="Airline" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400">{options_airline}</select>
            </div>

            <div>
              <label>Source</label>
              <select name="Source" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400">{options_source}</select>
            </div>

            <div>
              <label>Destination</label>
              <select name="Destination" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400">{options_dest}</select>
            </div>

            <div>
              <label>Date of Journey</label>
              <input type="date" name="Date_of_Journey" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400" />
            </div>

            <div>
              <label>Departure Time</label>
              <input type="time" name="Dep_Time" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400" />
            </div>

            <div>
              <label>Arrival Time</label>
              <input type="time" name="Arrival_Time" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400" />
            </div>

            <div>
              <label>Total Stops</label>
              <select name="Total_Stops" required class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400">
                <option value="non-stop">non-stop</option>
                <option value="1 stop">1 stop</option>
                <option value="2 stops">2 stops</option>
                <option value="3 stops">3 stops</option>
              </select>
            </div>

            <div class="col-span-2">
              <label>Additional Info</label>
              <input name="Additional_Info" value="No info" class="mt-2 w-full rounded-md p-2 bg-white/70 dark:bg-gray-700/70 border focus:ring-2 focus:ring-indigo-400" />
            </div>

            <div class="col-span-2 text-center mt-6">
              <button type="submit" class="bg-gradient-to-r from-indigo-500 to-pink-500 text-white font-semibold py-2 px-8 rounded-full shadow-lg hover:shadow-2xl transition-transform transform hover:-translate-y-0.5">
                💡 Predict Price
              </button>
            </div>
          </form>
        </div>

        <!-- Theme Toggle Script -->
        <script>
          function toggleTheme() {{
            const html = document.documentElement;
            const icon = document.getElementById("theme-icon");
            const isDark = html.classList.toggle("dark");
            localStorage.setItem("theme", isDark ? "dark" : "light");
            icon.dataset.feather = isDark ? "sun" : "moon";
            feather.replace();
          }}
          window.onload = function() {{
            if (localStorage.getItem("theme") === "dark") document.documentElement.classList.add("dark");
            feather.replace();
          }};
        </script>
      </body>
    </html>
    """


@router.post("/predict", response_class=HTMLResponse)
def predict(
    Airline: str = Form(...),
    Source: str = Form(...),
    Destination: str = Form(...),
    Date_of_Journey: str = Form(...),
    Dep_Time: str = Form(...),
    Arrival_Time: str = Form(...),
    Total_Stops: str = Form(...),
    Additional_Info: str = Form("No info"),
):
    Duration = compute_duration(Dep_Time, Arrival_Time)
    df = pd.DataFrame(
        [
            {
                "Airline": Airline,
                "Date_of_Journey": pd.to_datetime(Date_of_Journey).strftime("%d/%m/%Y"),
                "Source": Source,
                "Destination": Destination,
                "Route": f"{Source} → {Destination}",
                "Dep_Time": Dep_Time,
                "Arrival_Time": Arrival_Time,
                "Duration": Duration,
                "Total_Stops": Total_Stops,
                "Additional_Info": Additional_Info,
            }
        ]
    )
    price = round(float(model.predict(df)[0]), 2)

    return f"""
    <html>
      <head>
        <title>Prediction Result</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
      </head>
      <body class="gradient-bg dark:bg-gray-900 flex items-center justify-center min-h-screen text-gray-900 dark:text-white">
        <div class="backdrop-blur-xl bg-white/30 dark:bg-gray-800/50 border border-white/20 shadow-2xl rounded-3xl p-10 text-center max-w-md">
          <h2 class="text-2xl font-bold text-indigo-700 dark:text-indigo-300 mb-4">Predicted Flight Price ✈️</h2>
          <p class="text-4xl font-extrabold text-green-600 dark:text-green-400 mb-4">₹ {price}</p>
          <p class="text-gray-700 dark:text-gray-300 mb-6">Calculated Duration: <b>{Duration}</b></p>
          <a href="/" class="bg-gradient-to-r from-indigo-500 to-pink-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition">🔁 Predict Another</a>
        </div>
      </body>
    </html>
    """
