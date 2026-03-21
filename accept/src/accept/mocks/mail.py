import httpx


class MailpitSpy:
    def __init__(self) -> None:
        self.client = httpx.Client(base_url="http://localhost:8025")

    @property
    def message_count(self):
        response = self.client.get("/api/v1/messages")
        assert response.status_code == 200
        return response.json()['count']
    
    def get_last_mail(self):
        response = self.client.get("/api/v1/messages")
        assert response.status_code == 200
        mails = response.json()
        last_mail = mails['messages'][0]
        return last_mail
    
    def reset(self):
        response = self.client.delete("/api/v1/messages")
        assert response.status_code == 200