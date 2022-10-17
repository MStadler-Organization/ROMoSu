import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {RuntimeMonitoringWizardRoutingModule} from './runtime-monitoring-wizard-routing.module';
import {RuntimeMonitoringWizardComponent} from './runtime-monitoring-wizard.component';


@NgModule({
  declarations: [
    RuntimeMonitoringWizardComponent
  ],
  imports: [
    CommonModule,
    RuntimeMonitoringWizardRoutingModule
  ]
})
export class RuntimeMonitoringWizardModule {
}
