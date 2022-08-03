import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {NewConfigWizardRoutingModule} from './new-config-wizard-routing.module';
import {NewConfigWizardComponent} from './new-config-wizard.component';
import {MatStepperModule} from "@angular/material/stepper";
import {ReactiveFormsModule} from "@angular/forms";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {MatExpansionModule} from "@angular/material/expansion";
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatTreeModule} from "@angular/material/tree";


@NgModule({
  declarations: [
    NewConfigWizardComponent
  ],
  imports: [
    CommonModule,
    NewConfigWizardRoutingModule,
    MatStepperModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    MatExpansionModule,
    MatProgressBarModule,
    MatCheckboxModule,
    MatTreeModule
  ]
})
export class NewConfigWizardModule {
}
