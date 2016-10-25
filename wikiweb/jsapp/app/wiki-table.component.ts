import {Component, Input, OnInit} from '@angular/core';

import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';
import {WS_LIST} from './ws-list';

@Component({
  selector: 'wiki-table',
  templateUrl: 'static/app/wiki-table.html'
})
export class WikiTable implements OnInit{
  @Input()
  subscription: string;

  public subject: WebSocketSubject<any>;
  public headers = ['Name', 'Total'];
  public data = []; 

  constructor(private webSocketService: WebSocketService) {}

  nameToURL(name: string): string {
    return `https://en.wikipedia.org/wiki/${name.replace(/\s/g,'_')}`;
  }

  ngOnInit() {
    this.subject = this.webSocketService.getSubject();
    this.subject.subscribe(
      e => {
        this.data = e.charts[this.subscription].map(v => { 
          return {
            url: this.nameToURL(v.name),
            name: v.name,
            total: v.total
          };
        });
      },
      function (e) { console.log('onError: ' + e.message); },
      function () { console.log('onCompleted'); }
    );

  }
}
