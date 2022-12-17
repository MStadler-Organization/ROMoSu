import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {CommonModule} from "@angular/common";
import {FooterComponent} from './components/footer/footer.component';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatListModule} from "@angular/material/list";
import {CustomDialogComponent} from './components/custom-dialog/custom-dialog.component';
import {MatDialogModule} from "@angular/material/dialog";
import {LoadingDialogComponent} from './components/loading-dialog/loading-dialog.component';
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {RtDataDialogComponent} from './components/rt-data-dialog/rt-data-dialog.component';

@NgModule({
  declarations: [
    FooterComponent,
    CustomDialogComponent,
    LoadingDialogComponent,
    RtDataDialogComponent
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
    MatListModule,
    MatDialogModule,
    MatProgressSpinnerModule
  ]
})
export class SharedModule {
}
