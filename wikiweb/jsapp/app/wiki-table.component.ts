import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';
        
import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';
import {WS_LIST} from './ws-list';

@Component({
  selector: 'wiki-table',
  templateUrl: 'static/app/wiki-table.html'
})
export class WikiTable implements OnChanges{
  @Input()
  subscription: string;

  @Input()
  data = []; 

  public subject: WebSocketSubject<any>;
  public headers = ['Name', 'Total'];

  constructor(private webSocketService: WebSocketService) {}

  nameToURL(name: string): string {
    return `https://en.wikipedia.org/wiki/${name.replace(/\s/g,'_')}`;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data']) {
      this.data = changes['data'].currentValue.map(v => { 
        return {
          url: this.nameToURL(v.name),
          name: v.name,
          total: v.total
        };
      });
    }
  }
}
