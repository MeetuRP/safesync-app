# **SafeSync: Smarter Choice, Safer Outcomes**

A rapid reference web tool for medical professionals to instantly retrieve critical drug formulation and interaction safety data.

## **1\. The Big Picture: What is SafeSync?**

Imagine you have a very important question about a specific medicine, and you need a reliable answer instantly. SafeSync is a simple web tool designed to be that instant, reliable source for medical professionals like doctors and pharmacists.

Think of it like a super-fast, digital reference book for medicines. A healthcare provider can look up a drug and immediately get a clear, concise summary of the most critical information needed to ensure patient safety.

### **The Problem It Solves**

Medical professionals handle hundreds of different drugs. For every single one, they need to know:

* What are all the ingredients inside it?  
* Can this drug be safely taken with another drug?  
* What is the correct way to store it?

Finding this information quickly from different sources can be time-consuming and challenging. SafeSync solves this by putting all the essential safety information into one easy-to-use screen, helping them make smarter, safer decisions for their patients.

## **2\. Project Description & Technology**

SafeSync is a data-driven web application built entirely in Python. It serves as a proof-of-concept for a rapid-retrieval tool that leverages pre-compiled datasets on pharmaceutical formulations and drug-drug interactions. The front-end is rendered dynamically, providing a responsive and intuitive user experience for querying the data.

### **Technology Stack**

* **Backend & Frontend:** [**Python**](https://www.python.org/) with the [**Streamlit**](https://streamlit.io/) framework. Streamlit allows for the rapid development of interactive web applications using only Python.  
* **Data Manipulation:** [**Pandas**](https://pandas.pydata.org/) for loading, cleaning, and querying the drug information from the CSV datasets.  
* **Deployment:** The application is designed to be deployed on [**Streamlit Community Cloud**](https://streamlit.io/cloud).

## **3\. Project Structure**

The repository is structured to be simple and easy to navigate. All the core logic, data, and assets are organized as follows:

safesync\_project/  
│  
├── .gitignore          \# Tells Git which files to ignore  
├── data/               \# Contains the raw datasets  
│   ├── merged.csv      \# Main drug formulation dataset  
│   └── Interaction.csv \# Drug-drug interaction dataset  
│  
├── logo.jpg            \# The application logo  
├── README.md           \# This file: project documentation  
├── requirements.txt    \# Lists the Python libraries needed for the project  
└── safesync\_app.py     \# The main application file with all the Python/Streamlit code

## **4\. Setup and Installation for Contributors**

To get a local copy up and running, follow these simple steps. This is perfect for anyone who wants to contribute to the project or run it on their own machine.

### **Prerequisites**

* You must have [Python](https://www.python.org/downloads/) (version 3.8 or higher) installed.  
* You must have [Git](https://git-scm.com/downloads) installed to clone the repository.

### **Step-by-Step Installation**

1\. Clone the Repository  
Open your terminal or command prompt and run the following command to download the project files:  
git clone \<your-repository-url\>  
cd safesync\_project

2\. Create a Virtual Environment (Highly Recommended)  
It's best practice to create a separate environment for the project's dependencies. This avoids conflicts with other Python projects.  
\# Create the virtual environment  
python \-m venv venv

\# Activate it  
\# On Windows:  
venv\\Scripts\\activate  
\# On macOS/Linux:  
source venv/bin/activate

3\. Install Dependencies  
The requirements.txt file lists all the Python libraries the project needs. Install them with a single command:  
pip install \-r requirements.txt

4\. Run the Application  
You're all set\! Run the following command to start the Streamlit application:  
streamlit run safesync\_app.py

Your default web browser will automatically open a new tab with the SafeSync application running locally.
[**Streamlit**](https://safesync.streamlit.app/) link to open safesync hosted with streamlit
