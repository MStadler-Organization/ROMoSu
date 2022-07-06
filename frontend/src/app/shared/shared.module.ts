import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {MatSliderModule} from "@angular/material/slider";
import {CommonModule} from "@angular/common";
import {HeaderComponent} from './components/header/header.component';
import {FooterComponent} from './components/footer/footer.component';

@NgModule({
  declarations: [

    HeaderComponent,
    FooterComponent
  ],
  exports: [
    MatSliderModule,
    HeaderComponent,
    FooterComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class SharedModule {
}
