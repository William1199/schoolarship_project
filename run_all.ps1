Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py runserver"
Start-Process -NoNewWindow -FilePath "streamlit" -ArgumentList "run vanna_ai/app.py"
