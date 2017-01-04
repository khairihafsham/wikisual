import {Component,
        OnChanges,
        OnInit,
        SimpleChanges,
        Input} from '@angular/core';
import {WebSocketService} from './websocket.service';
import {WebSocketSubject} from 'rxjs/observable/dom/WebSocketSubject';
import {WS_LIST} from './ws-list';

@Component({
  moduleId: module.id,
  selector: 'wiki-chart',
  templateUrl: 'wiki-chart.html'
})
export class WikiChartComponent implements OnChanges {
  @Input()
  subscription: string;

  @Input()
  label: string = '';

  @Input()
  public data: Array<any> = [];

  public type = 'horizontalBar';

  public chartData: any = {
    labels: [],
    datasets: [
      {
        label: '',
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(0, 0, 0, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(129, 147, 44, 0.2)',
          'rgba(163, 235, 38, 0.2)',
          'rgba(0, 0, 66, 0.2)'
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(0, 0, 0, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(129, 147, 44, 1)',
          'rgba(163, 235, 38, 1)',
          'rgba(0, 0, 66, 1)'
        ],
        borderWidth: 1,
        data: [],
      }
    ]
  }; 

  public options = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      xAxes: [{
        ticks: {
          beginAtZero:true
        }
      }]
    }
  }

  private subject: WebSocketSubject<any>;

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit() {
    this.chartData.datasets[0].label = this.label;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data']) {
      var copy = Object.assign({}, this.chartData);
      var data = changes['data'].currentValue;
      copy.labels = data.map((v: any): any => { 
          if (v.name.length > 20)  {
            return v.name.slice(0, 20) + '...';
          }

          return v.name; 
        });
        copy.datasets[0].data = data.map((v: any): any => { return v.total; });

        this.chartData = copy;
    }
  }
}
