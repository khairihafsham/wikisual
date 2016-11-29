import {Component, OnInit} from '@angular/core';

import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';

@Component({
  selector: 'top-daily',
  templateUrl: 'top-daily.html'
})
export class TopDailyComponent implements OnInit {
  public dailyTopCountriesData: any = [];
  public dailyTopTitlesData: any = [];

  private subject: WebSocketSubject<any>;

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit(): void {
    this.webSocketService.connect('daily-top-charts');
    this.subject = this.webSocketService.getSubject();
    this.subject.subscribe(
      e => {
        this.dailyTopTitlesData = e.charts['daily-top-titles'];
        this.dailyTopCountriesData = e.charts['daily-top-countries'];
      },
      function (e) { console.log('onError: ' + e.message); },
      function () { console.log('onCompleted'); }
    );
    this.subject.next('');
  }
}
