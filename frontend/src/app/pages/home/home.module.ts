import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {HomeRoutingModule} from './home-routing.module';
import {HomeComponent} from './home.component';
import {MatSliderModule} from "@angular/material/slider";


@NgModule({
  declarations: [
    HomeComponent
  ],
  imports: [
    MatSliderModule,
    CommonModule,
    HomeRoutingModule
  ]
})
export class HomeModule {
}
