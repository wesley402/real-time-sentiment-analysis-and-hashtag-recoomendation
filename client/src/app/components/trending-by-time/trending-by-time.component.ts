import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';

@Component({
  selector: 'app-trending-by-time',
  templateUrl: './trending-by-time.component.html',
  styleUrls: ['./trending-by-time.component.css']
})

export class TrendingByTimeComponent implements OnInit {

  constructor(
  ) { }

  ngOnInit() {
      let ctx = document.getElementById("myChart");
      let myChart = new Chart(ctx, {
          type: 'line',
          data: {
              xAxisID: "time",
              yAxisID: "value",
              labels: ["1", "2","3","4"],
              datasets: [{
                  //label: '# of Votes',
                  data: [12, 19, 3, 5, 2, 3],
                  backgroundColor: 'rgba(255, 99, 132, 0.2)',
                  borderColor: 'rgba(255,99,132,1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero:true
                      }
                  }]
              }
          }
      });
  }
}
