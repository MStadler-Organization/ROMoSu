import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {RuntimeMonitoringWizardRoutingModule} from './runtime-monitoring-wizard-routing.module';
import {RuntimeMonitoringWizardComponent} from './runtime-monitoring-wizard.component';
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatStepperModule} from "@angular/material/stepper";
import {MatListModule} from "@angular/material/list";
import {MatButtonModule} from "@angular/material/button";
import {ReactiveFormsModule} from "@angular/forms";


@NgModule({
  declarations: [
    RuntimeMonitoringWizardComponent
  ],
  imports: [
    CommonModule,
    RuntimeMonitoringWizardRoutingModule,
    MatProgressBarModule,
    MatStepperModule,
    MatListModule,
    MatButtonModule,
    ReactiveFormsModule
  ]
})
export class RuntimeMonitoringWizardModule {
}
