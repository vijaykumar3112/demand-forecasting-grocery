# 📊 Grocery Demand Forecasting System
## AI-Powered Supply Chain Optimization

---

# 1. Project Overview

### **The Problem**
*   **Overstocking:** Leads to perishable waste and lost capital.
*   **Understocking:** Results in lost sales and dissatisfied customers.
*   **Complexity:** Demand fluctuates due to promotions, holidays, and seasonality.

### **The Solution**
An **End-to-End Machine Learning System** that predicts future sales with high accuracy, enabling data-driven inventory decisions.

---

# 2. Key Features

*   **🚀 Real-Time Forecasting:** Instant predictions for any item/store combination.
*   **📈 Interactive Dashboard:** User-friendly interface for business stakeholders.
*   **🧠 Advanced Analytics:** Insights into sales trends, promotion impact, and model performance.
*   **☁️ Cloud Native:** Fully deployed and accessible via the web (Render.com).
*   **🌗 Modern UI:** Professional Dark/Light mode design.

---

# 3. Technical Architecture

### **Tech Stack**
*   **Frontend:** Streamlit (Python) - *Responsive Web UI*
*   **Backend:** FastAPI - *High-performance REST API*
*   **Machine Learning:** LightGBM - *Gradient Boosting Framework*
*   **Deployment:** Render.com (Dockerized containers)
*   **Version Control:** Git & GitHub

### **Data Flow**
1.  **User** inputs data (Item, Store, Date) in Dashboard.
2.  **Dashboard** sends JSON request to **FastAPI**.
3.  **API** processes features & queries **LightGBM Model**.
4.  **Model** returns prediction & confidence intervals.
5.  **Dashboard** visualizes results instantly.

---

# 4. Data & Modeling Strategy

### **The Dataset**
*   Historical sales data from a large grocery chain.
*   Key variables: Date, Store ID, Item ID, Promotions, Unit Sales.

### **Feature Engineering**
We transformed raw data into predictive signals:
*   **Time-Series Features:** Day of week, Month, Year.
*   **Lag Features:** Sales from 1, 7, 14, 28 days ago.
*   **Rolling Statistics:** Moving averages (7-day, 28-day) to capture trends.

### **Model Choice: LightGBM**
*   Selected for its **speed** and **efficiency** with large datasets.
*   Handles categorical variables (Store/Item IDs) natively.
*   Outperformed Random Forest and XGBoost in initial tests.

---

# 5. Live Demo Highlights

### **1. Dashboard Overview**
*   At-a-glance system health (API status, Uptime).
*   Quick stats on the dataset and model performance.

### **2. Demand Forecaster**
*   **Input:** Select specific Item #1 at Store #1 for tomorrow.
*   **Output:** "Predicted Demand: 45 units".
*   **Confidence:** "Range: 35-55 units" (Helps in risk management).
*   **Actionable Insight:** "Recommended Stock: 50 units".

### **3. Performance Analytics**
*   Visualizes feature importance (what drives sales?).
*   Shows historical sales trends and promotion impact.

---

# 6. Deployment & CI/CD

### **Cloud Hosting**
*   Deployed on **Render.com** using a microservices architecture.
*   **Service 1:** API (Backend) - Handles logic and computation.
*   **Service 2:** Dashboard (Frontend) - Handles user interaction.

### **CI/CD Pipeline**
*   Code pushed to **GitHub**.
*   **Render** automatically detects changes.
*   Builds Docker environment -> Installs dependencies -> Deploys live.

---

# 7. Business Impact

*   **📉 Reduced Waste:** Better predictions mean less expired stock.
*   **💰 Optimized Inventory:** Capital is not tied up in excess inventory.
*   **⚡ Operational Efficiency:** Automated forecasting saves hours of manual work.
*   **🎯 Better Planning:** Promotion planning based on data, not intuition.

---

# 8. Future Improvements

*   **Multi-Model Support:** Add Prophet or ARIMA for comparison.
*   **User Authentication:** Secure login for different store managers.
*   **Batch Processing:** Upload CSV for bulk predictions.
*   **Inventory Integration:** Connect directly to ERP systems.

---

# Thank You!
## Questions?

*   **Live App:** [https://demand-forecasting-dashboard.onrender.com](https://demand-forecasting-dashboard.onrender.com)
*   **GitHub:** [https://github.com/vijaykumar3112/demand-forecasting-grocery](https://github.com/vijaykumar3112/demand-forecasting-grocery)

---
---

# 📝 Speaker Notes (Script)

### **Slide 1: Title**
"Good morning/afternoon everyone. Today I'm presenting my project: a Grocery Demand Forecasting System. This is an AI-powered solution designed to optimize supply chain operations."

### **Slide 2: Project Overview**
"The core problem in retail is balancing inventory. Overstocking leads to waste—especially with food—while understocking means lost revenue. My solution is an end-to-end machine learning system that predicts future sales with high accuracy, allowing store managers to make data-driven decisions."

### **Slide 3: Key Features**
"What makes this system special?
First, it provides **real-time forecasting**. You don't wait for overnight batch jobs.
Second, it features an **interactive dashboard** that is easy for non-technical staff to use.
Third, it's **cloud-native**, fully deployed on the web, and accessible from anywhere.
And finally, it includes a modern **Dark/Light mode UI** for a professional user experience."

### **Slide 4: Technical Architecture**
"Under the hood, I used a modern tech stack:
*   **Streamlit** for the frontend interface.
*   **FastAPI** for a high-performance backend.
*   **LightGBM** as our machine learning engine.
The system follows a microservices architecture where the frontend and backend are decoupled, communicating via REST APIs. This ensures scalability and maintainability."

### **Slide 5: Data & Modeling**
"For the modeling strategy:
I used historical sales data and engineered powerful features like **lag values** (past sales) and **rolling averages** to capture trends and seasonality.
I chose **LightGBM** because it's incredibly fast and accurate for tabular data, outperforming other models in my experiments."

### **Slide 6: Live Demo**
*(Switch to your live dashboard here if possible)*
"Let's look at the application.
The **Overview** page gives us system health metrics.
The **Forecaster** is the heart of the tool. If I select Item 1 and Store 1, it instantly predicts demand, gives me a confidence interval (so I know the risk), and even recommends a stocking level.
The **Analytics** page helps us understand *why* sales are happening, showing us feature importance and trends."

### **Slide 7: Deployment**
"This isn't just running on my laptop. It's fully deployed on the cloud using **Render.com**.
I set up a CI/CD pipeline linked to GitHub. Whenever I push code, it automatically rebuilds and deploys the new version, ensuring the production app is always up to date."

### **Slide 8: Business Impact**
"Ultimately, this technology drives business value by:
1.  Reducing waste from perishable goods.
2.  Optimizing capital allocation.
3.  Saving operational hours through automation."

### **Slide 9: Future Improvements**
"Looking ahead, I plan to add user authentication for security and batch processing capabilities to handle bulk predictions for entire stores at once."

### **Slide 10: Conclusion**
"Thank you for your time. The application is live at the link provided, and I'm happy to answer any questions."
