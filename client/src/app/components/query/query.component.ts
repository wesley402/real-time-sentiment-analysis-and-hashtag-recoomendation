import { Component, OnInit } from '@angular/core';
import { SocketService } from '../../services/socket.service';
import { Http, Response, Headers, RequestOptions } from '@angular/http';

@Component({
  selector: 'app-query',
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.css']
})
export class QueryComponent implements OnInit {
  keywords: string;
  messages: JSON[] = [];
  ioConnection: any;

  constructor(private http: Http, private socketService: SocketService) {}

  ngOnInit() {
  }


  private startStreaming(value: string): void { // without type info
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    this.keywords = value;
    let data = { "query": this.keywords }
    this.http.post('/api/streaming/start', data, options)
    .toPromise()
    .then();
  }

  private stopStreaming(value: string): void { // without type info
    this.http.post('/api/streaming/stop', {params: {}})
    .toPromise()
    .then();
  }

}
