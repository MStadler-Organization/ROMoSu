import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {CommonModule} from "@angular/common";
import {FooterComponent} from './components/footer/footer.component';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatListModule} from "@angular/material/list";

@NgModule({
  declarations: [
    FooterComponent
  ],
  exports: [
    FooterComponent
  ],
  imports: [
    CommonModule,
    MatToolbarModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatSidenavModule,
    MatListModule
  ]
})
export class SharedModule {
}
