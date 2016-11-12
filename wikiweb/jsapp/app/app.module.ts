import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {ChartModule} from 'angular2-chartjs';

import {AppComponent} from './app.component';
import {WikiChartComponent} from './wiki-chart.component';
import {WikiTable} from './wiki-table.component';
import {WebSocketService} from './websocket.service';
import {TopDailyComponent} from './top-daily.component';
import {TopHourlyComponent} from './top-hourly.component';
import {routing} from './app.routing';

@NgModule({
  imports: [
    BrowserModule,
    ChartModule,
    routing
  ],
  providers: [
    WebSocketService
  ],
  declarations: [
    AppComponent,
    WikiChartComponent,
    WikiTable,
    TopDailyComponent,
    TopHourlyComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
