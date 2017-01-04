import {Component, Input} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';

import {UpdateNotificationService} from './update-notification.service';

@Component({
  moduleId: module.id,
  selector: 'live-display',
  templateUrl: 'live-display.component.html'
})
export class LiveDisplayComponent {
  @Input() lastUpdated: string;

  subscription: Subscription;

  constructor(private updateNotificationService: UpdateNotificationService) {
    this.subscription = updateNotificationService.notification$.subscribe(
      updated => {
        if (updated === true) {
          this.lastUpdated = Date().toString();
        }
      }
    );
  }
}
