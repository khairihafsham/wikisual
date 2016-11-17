import {Component, OnInit} from '@angular/core';

import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';

@Component({
  selector: 'top-hourly',
  templateUrl: 'static/app/top-hourly.html'
})
export class TopHourlyComponent implements OnInit {
  private subject: WebSocketSubject<any>;

  public startHour = '0000';
  public endHour = '0100';

  public max = 23;
  public min = 0;

  public hourlyTopTitlesData = [];
  public topTitlesData = [];

  public loadedOnce = false;

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit() {
    this.webSocketService.connect('hourly-top-charts');
    this.subject = this.webSocketService.getSubject();
    this.subject.subscribe(
      e => {
        this.hourlyTopTitlesData = e.charts['hourly-top-titles'];
        if (this.loadedOnce === false) {
          this.reloadChartData(this.getLatestDataHour());
          this.setHours(this.getLatestDataHour());
          this.loadedOnce = true;
        }
      },
      function (e) { console.log('onError: ' + e.message); },
      function () { console.log('onCompleted'); }
    );
  }

  reloadChartData(hour: number): void {
    this.topTitlesData = this.hourlyTopTitlesData[hour];
  }

  getLatestDataHour(): number {
    var latestHour = 0;
    for (var hour in this.hourlyTopTitlesData) {
      if (this.hourlyTopTitlesData[hour].length > 0) {
        latestHour = Number(hour);
      }
    }

    return latestHour;
  }

  formatHour(hour: Number): string {
    if (hour < 10) {
      return `0${hour}00`;
    }

    return `${String(hour)}00`;
  }

  setHours(start: number): void {
    this.startHour = this.formatHour(start);
    this.endHour = this.formatHour(start + 1);
  }

  getStartHourAsNumber(): number {
    return Number(this.startHour.substring(0, 2));
  }

  goToCurrentHour(): void {
    this.reloadChartData(this.getLatestDataHour());
    this.setHours(this.getLatestDataHour());
  }

  goToNextHour(): void {
    var nextHour = this.getStartHourAsNumber();
    if (nextHour === this.max) {
      return;
    }

    ++nextHour;

    this.setHours(nextHour);
    this.reloadChartData(nextHour);
  };
  
  goToPreviousHour(): void {
    var previousHour = this.getStartHourAsNumber();
    if (previousHour === this.min) {
      return;
    }

    --previousHour;

    this.setHours(previousHour);
    this.reloadChartData(previousHour);
  };
}
