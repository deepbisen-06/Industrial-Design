# AI Industrial Chatbot — Deep Bisen

report.pdf includes the report and digitally typeset handwritten-style notes (not a real handwritten scan). Sample manuals are authored educational examples, not real operating procedures.

Run on Python 3.10+:
  python -m venv .venv
  activate your virtual environment
  python -m pip install -r source/requirements.txt
  python source/chatbot.py

The default path downloads google/flan-t5-small from Hugging Face and performs actual generation. Cache the model for offline reuse. Model access is required on first run. It does NOT silently replace failed generation with an extractive answer.

Explicit no-LLM baseline:
  python source/chatbot.py --extractive

Validation:
  python source/test_retrieval.py

Actual local retrieval tests and baseline CLI transcript are included. Hugging Face HTTPS access was blocked by proxy HTTP 403 in the preparation environment; torch/transformers were unavailable. LLM generation was therefore NOT executed. Baseline screenshots/figures are labelled accordingly. Install and run the default model locally, test the actual answers, and add genuine LLM interaction evidence before claiming full compliance with the assignment.

Before submission fill roll number, college and semester. Add real LLM demonstration screenshots to evidence/, update validation conclusions if supported by your run, and upload the source folder, sample documents, screenshots and report to Google Drive as required.

Do not use this prototype for safety-critical decisions. Retrieved text is untrusted input; prompt instructions are a mitigation, not a security guarantee. All numeric maintenance data in these sample manuals is illustrative.
