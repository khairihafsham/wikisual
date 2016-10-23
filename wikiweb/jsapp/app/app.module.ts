import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {ChartModule} from 'angular2-chartjs';

import {AppComponent} from './app.component';
import {WikiChartComponent} from './wiki-chart.component';
import {WikiTable} from './wiki-table.component';
import {WebSocketService} from './websocket.service';

@NgModule({
  imports: [
    BrowserModule,
    ChartModule
  ],
  providers: [
    WebSocketService
  ],
  declarations: [
    AppComponent,
    WikiChartComponent,
    WikiTable
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
