import {Component, OnInit} from '@angular/core';
import {WebSocketService} from './websocket.service';

@Component({
  selector: 'my-app',
  templateUrl: 'static/app/app.component.html'
})
export class AppComponent implements OnInit {
  title = 'Wikisual';

  constructor(public webSocketService: WebSocketService) {}

  ngOnInit(): void {
    this.webSocketService.connect('daily-top-charts');
  }
}
