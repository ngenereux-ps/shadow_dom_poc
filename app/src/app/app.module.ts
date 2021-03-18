import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {ContainerComponent} from './container/container.component';
import {SelectComponent} from './select/select.component';

@NgModule({
  declarations: [
    AppComponent,
    ContainerComponent,
    SelectComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
