import { Routes } from '@angular/router';
import { RouterModule } from '@angular/router';
import { BotComponent } from './bot/bot.component';
import { AdComponent } from './ad/ad.component';
import { NgModule } from '@angular/core';

export const routes: Routes = [
    { path: '', redirectTo: '/bot', pathMatch: 'full' },
    { path: 'bot', component: BotComponent },
    { path: 'ad', component: AdComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
