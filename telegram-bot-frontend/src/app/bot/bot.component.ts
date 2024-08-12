import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { AdComponent } from '../ad/ad.component';

@Component({
  selector: 'app-bot',
  standalone: true,
  imports: [CommonModule, AdComponent],
  templateUrl: './bot.component.html',
  styleUrl: './bot.component.css'
})
export class BotComponent {
  constructor() { }

  ngOnInit() { }

  adSkipped = false;

  onSkipAd() {
    this.adSkipped = true;
  }

}
