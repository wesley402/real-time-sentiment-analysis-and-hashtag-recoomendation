import { Component, OnInit, OnChanges, Input } from '@angular/core';
import Chart from 'chart.js';
import { Http, Response, Headers } from '@angular/http';
import { SocketService } from '../../services/socket.service';
import { Event } from '../../models/event';
import * as moment from "moment";


@Component({
  selector: 'app-trending-by-time',
  templateUrl: './trending-by-time.component.html',
  styleUrls: ['./trending-by-time.component.css']
})

export class TrendingByTimeComponent implements OnInit {
  msg: any;
  myChart: any;
  constructor(private http: Http, private socketService: SocketService)
  { }

  ngOnInit() {
      this.initIoConnection();
      this.msgStreaming();
      this.initChart();
  }
  //
  // ngOnChanges() {
  //   if(this.msg) {
  //     this.onRefresh(this.myChart);
  //   }
  //   console.log('change');
  // }

  private onRefresh(chart, label, value): void {
    chart.data.labels.push(label);
  	chart.data.datasets.forEach((dataset) => {
      dataset.data.push(value);
  	})
    chart.update();
  }

  private msgStreaming(): void {
    this.socketService.onMessage()
      .subscribe((message: any) => {
          this.msg = message;
          this.onRefresh(this.myChart, moment(message.created_at, 'HH:mm:ss'),
            message.sentimentValue);
      });
  }

  private initIoConnection(): void {
    console.log('init connection');
    this.socketService.initSocket();

    this.socketService.onEvent(Event.CONNECT)
      .subscribe(() => {
        console.log('connected');
      });

    this.socketService.onEvent(Event.DISCONNECT)
      .subscribe(() => {
        console.log('disconnected');
      });
  }

  private initChart(): void {
    let ctx = document.getElementById("myChart");
    this.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            xAxisID: "time",
            yAxisID: "value",
            datasets: [{
                //label: '# of Votes',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    ticks: {
                      autoSkip: true,
                      maxTicksLimit: 6
                    },
                    distribution: 'linear',
                    time: {
                      unit: 'second',
                      displayFormats: {
                        'second': 'HH:mm:ss'
                      }
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: 2,
                        min: -2,
                        stepSize: 0.5
                    }
                }]
            }
        }
    });
  }
}
