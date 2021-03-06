import {Component, OnInit} from '@angular/core';

import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';
import {UpdateNotificationService} from './update-notification.service';

@Component({
  moduleId: module.id,
  selector: 'top-daily',
  templateUrl: 'top-daily.component.html',
  providers: [UpdateNotificationService]
})
export class TopDailyComponent implements OnInit {
  public dailyTopCountriesData: any = [];
  public dailyTopTitlesData: any = [];

  private subject: WebSocketSubject<any>;

  constructor(
    private webSocketService: WebSocketService,
    private updateNotificationService: UpdateNotificationService
  ) {}

  ngOnInit(): void {
    this.webSocketService.connect('daily-top-charts');
    this.subject = this.webSocketService.getSubject();
    this.subject.subscribe(
      e => {
        this.dailyTopTitlesData = e.charts['daily-top-titles'];
        this.dailyTopCountriesData = e.charts['daily-top-countries'];
        this.updateNotificationService.notify(true);
      },
      function (e) { console.log('onError: ' + e.message); },
      function () { console.log('onCompleted'); }
    );
    this.subject.next('');
  }
}
