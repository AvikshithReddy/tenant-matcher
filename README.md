Tenant Matcher

Tenant Matcher is a data-driven property matching system that helps users find rental properties based on their preferences and automatically sends matched listings via email.

The system is designed to later evolve into an AI-powered chatbot for conversational property search.

⸻

🚀 Features
	•	User input–based search (beds, baths, price range, amenities, location)
	•	Dataset-driven property matching
	•	Automated email delivery of matched properties
	•	Frontend-first design with chatbot-ready backend logic

⸻

🧠 How It Works
	1.	User selects rental preferences from the frontend
	2.	System filters a structured property dataset
	3.	Best-matched properties are identified
	4.	Results are emailed directly to the user





 Project Structure:
 tenant-matcher/
├── app.py                  # Main app
├── matcher.py              # Matching logic
├── email_utils.py          # Email utilities
├── send_test_email.py      # Email testing
├── tenant_units_demo.csv   # Property dataset
├── requirements.txt
└── README.md



Tech Stack
	•	Python
	•	Pandas
	•	Streamlit
	•	SMTP / Email services
	•	dotenv

Dependencies include streamlit, pandas, and python-dotenv  ￼

⸻

🔮 Future Enhancements
	•	Conversational AI chatbot (LLM-based)
	•	ML-based recommendation ranking
	•	Database integration (PostgreSQL / Cloud)
	•	User accounts and saved searches
