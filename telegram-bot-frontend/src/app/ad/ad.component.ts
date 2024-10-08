import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api/api.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ad',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ad.component.html',
  styleUrl: './ad.component.css'
})
export class AdComponent implements OnInit {
  adVideoUrl: SafeResourceUrl | null = null;

  constructor(private router: Router, private api: ApiService, private sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.get_video();
  }

  skipAd() {
    this.router.navigate(['/video']);
  }

  closeAd() {
    this.router.navigate(['/video']);
  }

  get_video() {
    this.api.get_video_url().subscribe({
      next: (data: any) => {
        this.adVideoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(data.ad_video_url);
      },
      error: (error) => {
        console.log(error)
      }
    })
  }

  // closeAd() {
  //   window.location.href = 'tg://resolve?domain=your_bot_username';
  // }

}