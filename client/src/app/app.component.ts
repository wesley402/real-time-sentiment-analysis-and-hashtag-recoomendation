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

  constructor(private http: Http, private socketService: SocketService) {
  }

  ngOnInit(): void {
  }





}
