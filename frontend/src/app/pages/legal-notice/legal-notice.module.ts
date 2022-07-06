import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LegalNoticeRoutingModule } from './legal-notice-routing.module';
import { LegalNoticeComponent } from './legal-notice.component';


@NgModule({
  declarations: [
    LegalNoticeComponent
  ],
  imports: [
    CommonModule,
    LegalNoticeRoutingModule
  ]
})
export class LegalNoticeModule { }
