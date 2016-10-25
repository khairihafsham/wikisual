import {Injectable} from '@angular/core';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';

@Injectable()
export class WebSocketService {
  protected subject: WebSocketSubject<any>;

  connect(path): WebSocketSubject<any> {
    var url = `ws://${window.location.host}/${path}`;
    console.log(`connecting to ${url}`);
    this.subject = WebSocketSubject.create(url);

    return this.subject;
  }

  getSubject(): WebSocketSubject<any> {
    return this.subject;
  }
}
