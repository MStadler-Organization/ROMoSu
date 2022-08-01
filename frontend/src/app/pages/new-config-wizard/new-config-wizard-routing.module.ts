import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NewConfigWizardComponent } from './new-config-wizard.component';

const routes: Routes = [{ path: '', component: NewConfigWizardComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NewConfigWizardRoutingModule { }
