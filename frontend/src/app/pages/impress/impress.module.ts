import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ImpressRoutingModule } from './impress-routing.module';
import { ImpressComponent } from './impress.component';


@NgModule({
  declarations: [
    ImpressComponent
  ],
  imports: [
    CommonModule,
    ImpressRoutingModule
  ]
})
export class ImpressModule { }
