import requests
import sseclient

response = requests.get('http://149.130.186.128:8080/backend/yudexminds/mcp', stream=True)
client = sseclient.SSEClient(response)
for event in client.events():
    print(f'Event: {event.event}')
    print(f'Data: {event.data}')
    break