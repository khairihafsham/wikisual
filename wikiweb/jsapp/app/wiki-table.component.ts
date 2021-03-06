import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';
        
import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';
import {WS_LIST} from './ws-list';

@Component({
  moduleId: module.id,
  selector: 'wiki-table',
  templateUrl: 'wiki-table.component.html'
})
export class WikiTable implements OnChanges{
  @Input()
  subscription: string;

  @Input()
  data: any = []; 

  public subject: WebSocketSubject<any>;
  public headers = ['Name', 'Total'];

  constructor(private webSocketService: WebSocketService) {}

  nameToURL(name: string): string {
    return `https://en.wikipedia.org/wiki/${name.replace(/\s/g,'_')}`;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data']) {
      this.data = changes['data'].currentValue.map((v: any): any => { 
        return {
          url: this.nameToURL(v.name),
          name: v.name,
          total: v.total
        };
      });
    }
  }
}
