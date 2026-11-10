import requests


def ask_question(question):
    request_data = {"question": question}
    response = requests.post("http://localhost:8000/api/v1/ask", json=request_data)
    try:
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print("An error occurred:", e)
