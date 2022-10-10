import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ManageSumTypesComponent} from './manage-sum-types.component';

const routes: Routes = [{path: '', component: ManageSumTypesComponent}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManageSumTypesRoutingModule {
}
