import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api/api.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-video',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video.component.html',
  styleUrl: './video.component.css'
})
export class VideoComponent implements OnInit {
  mainVideoUrl: SafeResourceUrl | null = null;

  constructor(private router: Router, private api: ApiService, private sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.get_video();
  }

  get_video() {
    this.api.get_video_url().subscribe({
      next: (data: any) => {
        this.mainVideoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(data.main_video_url);

      },
      error: (error) => {
        console.log(error)
      }
    })
  }

  closeVideo() {
    this.router.navigate(['/ad']);
  }

  // closeVideo() {
  //   window.location.href = 'tg://resolve?domain=your_bot_username';
  // }

  playVideo() { }
}