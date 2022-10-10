import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ManageSumTypesRoutingModule} from './manage-sum-types-routing.module';
import {ManageSumTypesComponent} from './manage-sum-types.component';


@NgModule({
  declarations: [
    ManageSumTypesComponent
  ],
  imports: [
    CommonModule,
    ManageSumTypesRoutingModule
  ]
})
export class ManageSumTypesModule {
}
