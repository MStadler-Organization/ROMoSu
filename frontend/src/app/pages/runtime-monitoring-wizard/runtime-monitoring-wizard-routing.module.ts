import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {RuntimeMonitoringWizardComponent} from './runtime-monitoring-wizard.component';

const routes: Routes = [{path: '', component: RuntimeMonitoringWizardComponent}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RuntimeMonitoringWizardRoutingModule {
}
