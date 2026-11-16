# 🚦 Fuzzy Logic-Based Smart Traffic Controller

An intelligent traffic management system that uses **Fuzzy Logic** to dynamically adjust traffic signal timings according to traffic congestion and waiting times.

The project simulates and compares two traffic control approaches:

- **Fixed-Time Controller:** Uses a predefined green-light duration.
- **Fuzzy Logic Controller:** Adjusts green-light duration based on traffic conditions.

The main objective is to demonstrate how intelligent, adaptive traffic signal control can help reduce vehicle waiting times and improve traffic flow.

---

## 🌐 Live Demo

🚀 [Fuzzy Logic-Based Smart Traffic Controller – Live Application](https://fuzzy-smart-traffic-controller.streamlit.app/)

## 💻 GitHub Repository

[View Source Code on GitHub](https://github.com/nehabhadauria25/fuzzy-smart-traffic-controller)
---

## 📌 Project Objectives

- Simulate traffic conditions at a two-direction intersection.
- Implement a traditional fixed-time traffic controller.
- Develop an adaptive fuzzy logic-based traffic controller.
- Compare the performance of both controllers.
- Visualize traffic congestion, waiting times, and queue lengths.
- Evaluate controller performance using quantitative metrics.

---

## ✨ Features

### 1. Traffic Simulation

- Generates random vehicle arrivals for North-South and East-West directions.
- Simulates vehicle queues and traffic movement.
- Uses the same vehicle arrival data for both controllers to ensure a fair comparison.

### 2. Fixed-Time Traffic Controller

- Assigns a predefined green-light duration.
- Provides a baseline for comparing adaptive traffic control.

### 3. Fuzzy Logic Traffic Controller

- Uses fuzzy logic to make adaptive signal-timing decisions.
- Considers traffic conditions to determine green-light duration.
- Supports dynamic traffic management.

### 4. Performance Metrics

The system evaluates:

- Average Waiting Time
- Average Queue Length
- Total Vehicles Passed
- Maximum Waiting Time
- Throughput
- Vehicles Still Waiting
- Congestion Level

### 5. Data Visualization

The application generates graphs to compare:

- Overall controller performance
- Average waiting time
- Average queue length
- Queue length over simulation time
- Green-light decisions

### 6. Interactive Streamlit Dashboard

- Adjustable simulation duration.
- Configurable vehicle arrival rates.
- Adjustable fixed green-light duration.
- Random seed configuration.
- Side-by-side controller comparison.
- CSV download of simulation results.

---

## 🛠️ Technologies Used

| Technology   | Purpose                                             |
| ------------ | --------------------------------------------------- |
| Python       | Core programming language                           |
| Streamlit    | Interactive web application                         |
| NumPy        | Numerical operations and vehicle arrival generation |
| Pandas       | Data handling and analysis                          |
| Matplotlib   | Data visualization                                  |
| Scikit-Fuzzy | Fuzzy logic implementation                          |
| Pytest       | Automated testing                                   |

---

## 📂 Project Structure
```
fuzzy-smart-traffic-controller/
│
├── app.py
├── fuzzy_logic.py
├── simulation.py
├── traffic_metrics.py
├── visualization.py
│
├── tests/
│   ├── test_simulation.py
│   └── test_visualization.py
│
├── results/
│   ├── controller_comparison.png
│   ├── waiting_time.png
│   └── queue_comparison.png
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Step 1: Clone the Repository
```
git clone https://github.com/nehabhadauria25/fuzzy-smart-traffic-controller.git
```

### Step 2: Navigate to the Project Directory
```
cd fuzzy-smart-traffic-controller
```

### Step 3: Create a Virtual Environment (Recommended)
```
python -m venv .venv
```

Activate it on Windows PowerShell:
```
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies
```
python -m pip install -r requirements.txt
```

### Step 5: Run the Application
```
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Running Tests

The project uses Pytest for automated testing.

Run all tests:
```
python -m pytest -v
```

### Test Coverage

The project currently contains six automated tests:

| Test                       | Description                                   |
| -------------------------- | --------------------------------------------- |
| `test_calculate_metrics`   | Tests traffic performance metric calculations |
| `test_compare_controllers` | Tests comparison between controllers          |
| `test_congestion_level`    | Tests congestion classification               |
| `test_comparison_graph`    | Tests controller comparison graph generation  |
| `test_waiting_time_graph`  | Tests waiting-time graph generation           |
| `test_queue_graph`         | Tests queue comparison graph generation       |

**Latest test result: 6 passed, 0 failed.**

---

## 🚀 Future Improvements

- Support multiple traffic intersections.
- Introduce pedestrian movement and crossing signals.
- Incorporate real-world traffic datasets.
- Compare fuzzy logic with additional intelligent traffic-control algorithms.
- Develop a more realistic traffic simulation environment.
- Explore reinforcement learning for adaptive traffic management.

---

## 🎯 Conclusion

The Fuzzy Logic-Based Smart Traffic Controller demonstrates how fuzzy logic can be applied to traffic signal management.

By comparing fixed-time and adaptive traffic control under the same simulated traffic conditions, the project provides a practical demonstration of intelligent decision-making and performance evaluation.

**Note:** This project is an educational simulation and is not intended for controlling real-world traffic signals.
