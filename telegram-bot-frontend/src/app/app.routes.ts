import { Routes } from '@angular/router';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { HomeComponent } from './home/home.component';
import { AdComponent } from './ad/ad.component';
import { VideoComponent } from './video/video.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'ad', component: AdComponent },
    { path: 'video', component: VideoComponent }
  ];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
