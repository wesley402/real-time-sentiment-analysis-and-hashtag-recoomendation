import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from "@angular/common/http";
import { AppComponent } from './app.component';
import { HttpModule } from "@angular/http";
import { TrendingByTimeComponent } from './components/trending-by-time/trending-by-time.component';

@NgModule({
  declarations: [
    AppComponent,
    TrendingByTimeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
