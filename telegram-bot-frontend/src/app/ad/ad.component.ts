import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-ad',
  standalone: true,
  imports: [],
  templateUrl: './ad.component.html',
  styleUrl: './ad.component.css'
})
export class AdComponent {
  constructor() { }

  ngOnInit() { }

  @Output() skip = new EventEmitter<void>();

  onSkip() {
    this.skip.emit();
  }
}
