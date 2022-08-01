import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NewConfigWizardRoutingModule } from './new-config-wizard-routing.module';
import { NewConfigWizardComponent } from './new-config-wizard.component';


@NgModule({
  declarations: [
    NewConfigWizardComponent
  ],
  imports: [
    CommonModule,
    NewConfigWizardRoutingModule
  ]
})
export class NewConfigWizardModule { }
