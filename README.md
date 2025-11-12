# 🛒 Customer Behavior Analysis Using Markov Chain, Monte Carlo Simulation & Round Robin Congestion Handling  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Notebook-Jupyter-orange.svg)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Made with ❤️ by Abhishek](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](https://github.com/)

---

## 📘 Project Overview  

This project models and predicts **customer movement behavior inside a retail store** using a combination of **Markov Chain**, **Monte Carlo Simulation**, and a **Round Robin-based congestion handling mechanism**.  

The goal is to analyze how customers transition between store sections, estimate section-wise traffic, and simulate store revenue generation based on visit probabilities and purchase trends.  
A **Round Robin method** is integrated as a checkpoint to efficiently handle congestion by balancing the number of customers across crowded sections.

---

## 🎯 Objectives  

- Analyze customer movement data from entry to exit.  
- Generate transition probability matrices using **Markov Chains**.  
- Simulate realistic store activity through **Monte Carlo methods**.  
- Implement **Round Robin scheduling** to avoid section overcrowding.  
- Compute **section-wise revenue** and recommend layout optimizations.  
- Identify **high-priority** (most profitable) and **low-priority** (least profitable) sections.  

---

## 🧠 Core Concepts  

| Concept | Description |
|----------|--------------|
| **Markov Chain Model** | Represents customer transitions between store sections as probabilistic states. |
| **Monte Carlo Simulation** | Uses random sampling to simulate real-world store activity and revenue outcomes. |
| **Round Robin Congestion Handling** | Distributes customer flow evenly to manage overcrowded sections efficiently. |
| **Time Series Data** | Captures customer movements across time (7 AM – 10 PM). 

---

## ⚙️ Installation & Setup  

### 🧩 Prerequisites  

Ensure you have the following installed:  
- ![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)(https://www.python.org/)
- ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
- ![Matplotlib](https://img.shields.io/badge/Matplotlib-008B8B?style=for-the-badge&logo=plotly&logoColor=white)
- ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
- ![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
- [![Jupyter Notebook](https://img.shields.io/badge/Jupyter_Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
- [![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)

### 🪄 Steps to Run  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/Customer-Behavior-Analysis-Using-Markov-Chain-and-Monte-Carlo-Simulation.git

# 2️⃣ Navigate into the project folder
cd Customer-Behavior-Analysis-Using-Markov-Chain-and-Monte-Carlo-Simulation

# 3️⃣ Install all dependencies
pip install -r requirements.txt

# 4️⃣ Run the main notebook for step-by-step analysis
jupyter notebook customerMovementPrediction.ipynb
jupyter notebook transitionMatrixGeneration.ipynb

# OR run the simulation directly from Python script
python simulation1.py


