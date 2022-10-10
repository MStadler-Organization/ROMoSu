import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ManageSumTypesRoutingModule} from './manage-sum-types-routing.module';
import {ManageSumTypesComponent} from './manage-sum-types.component';
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatTableModule} from "@angular/material/table";
import {MatButtonModule} from "@angular/material/button";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {ReactiveFormsModule} from "@angular/forms";


@NgModule({
  declarations: [
    ManageSumTypesComponent
  ],
  imports: [
    CommonModule,
    ManageSumTypesRoutingModule,
    MatProgressBarModule,
    MatTableModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule
  ]
})
export class ManageSumTypesModule {
}
