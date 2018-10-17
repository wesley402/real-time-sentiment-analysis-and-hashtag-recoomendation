import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SocketService } from './services/socket.service';
import { Event } from './models/event';
import { Http, Response, Headers } from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  messages: JSON[] = [];
  ioConnection: any;
  msg: any;
  constructor(private http: Http, private socketService: SocketService) {
  }


  ngOnInit(): void {
    this.initIoConnection();
  }

  private initIoConnection(): void {
    console.log('init connection');
    this.socketService.initSocket();
    this.socketService.onMessage()
      .subscribe((message: any) => {
          this.msg = message;
      });

    this.socketService.onEvent(Event.CONNECT)
      .subscribe(() => {
        console.log('connected');
      });

    this.socketService.onEvent(Event.DISCONNECT)
      .subscribe(() => {
        console.log('disconnected');
      });
  }

  private startStream(): void {
    // const requestOptions = {
    //   headers: new Headers({ 'Content-Type': 'application/json' })
    // };
       this.http.get('/api/stream')
      .toPromise()
      .then();

  }


}
