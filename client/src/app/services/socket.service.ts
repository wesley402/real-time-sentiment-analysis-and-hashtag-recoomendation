import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs';
import * as io from 'socket.io-client';
import { Event } from '../models/event';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  private url = 'http://127.0.0.1:5000/streaming_socket';
  private socket;

  public initSocket(): void {
      this.socket = io.connect(this.url);
      console.log('init socket');
  }



  public onMessage(): Observable<JSON> {
    return new Observable<JSON>(observer => {
      this.socket.on('message', (data) => {
        observer.next(data);
        console.log("SASAS");
        console.log(data);
        console.log(typeof(data));
        });
    });
  }


  public onEvent(event: Event): Observable<any> {
      return new Observable<Event>(observer => {
          this.socket.on(event, () => observer.next());
      });
  }
}
