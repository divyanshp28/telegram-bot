import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  private api_url = 'http://localhost:5000';

  get_video_url() {
    return this.http.get(this.api_url + '/video')
  }
}
