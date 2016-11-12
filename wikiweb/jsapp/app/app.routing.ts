import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {TopDailyComponent} from './top-daily.component';
import {TopHourlyComponent} from './top-hourly.component';

const appRoutes: Routes = [
  {
    path: 'top-daily',
    component: TopDailyComponent
  },
  {
    path: 'top-hourly',
    component: TopHourlyComponent
  },
  {
    path: '',
    redirectTo: '/top-daily',
    pathMatch: 'full'
  }
]

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
