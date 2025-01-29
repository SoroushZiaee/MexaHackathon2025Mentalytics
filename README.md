# TheraAssist: AI-Powered Homework Generator for Clinicians

Project for MEXA (Mental Health x AI) hackathon - January 2025.

**TheraAssist** is an AI-powered assistant designed to help clinicians create personalized homework assignments for clients. Within this FastAPI-based application, clinicians provide assessment surveys, which clients complete, and the AI analyzes this data to generate customized, research-backed exercises. These exercises are delivered through a mobile app that sends reminders and notifications to support homework completion. Clinicians retain full control, selecting the most relevant exercises to ensure quality, appropriateness, and minimal burden on clients. By streamlining homework creation, TherAssist enhances therapeutic outcomes while reducing clinicians’ workload! 

In this version, we focused on clients who work from home and experience social anxiety. We used the Liebowitz Social Anxiety Scale (LSAS) for assessment. As clients complete the survey, clinicians receive their responses along with Gemini's analysis and personalized homework recommendations. This helps clinicians quickly assess social anxiety levels, track progress over time, and provide targeted interventions more efficiently.

- [Gemini_integration.ipynb](https://github.com/SoroushZiaee/MexaHackathon2025Mentalytics/blob/main/Gemini_integration.ipynb) notebook has the step by step Gemini integration, as well as example cases.
- [app.py](https://github.com/SoroushZiaee/MexaHackathon2025Mentalytics/blob/main/apis/app.py) script has the application code. The application includes features for:<br>
  - client and clinician registration.
  - LSAS survey submission and tracking
  - progress monitoring
  - exercise assignments
  - analytics dashboard
- **Demo:**<br>
![](https://github.com/SoroushZiaee/MexaHackathon2025Mentalytics/blob/main/TheraAssistant-demo.gif)

