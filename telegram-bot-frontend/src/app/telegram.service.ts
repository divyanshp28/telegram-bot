import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TelegramService {

  private backendUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  setWebhook(webhookUrl: string) {
    return this.http.post(`${this.backendUrl}/set_webhook`, { webhook_url: webhookUrl });
  }
}
