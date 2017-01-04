import {Injectable} from '@angular/core';
import {Subject} from 'rxjs/Subject';

@Injectable()
export class UpdateNotificationService {
  private notificationSource = new Subject<boolean>();

  notification$ = this.notificationSource.asObservable();

  notify(updated: boolean) {
    this.notificationSource.next(updated);
  }
}
