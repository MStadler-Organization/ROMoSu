import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ConfigEditorRoutingModule} from './config-editor-routing.module';
import {ConfigEditorComponent} from './config-editor.component';
import {MatTableModule} from "@angular/material/table";
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {ReactiveFormsModule} from "@angular/forms";
import {MatButtonModule} from "@angular/material/button";


@NgModule({
  declarations: [
    ConfigEditorComponent
  ],
  imports: [
    CommonModule,
    ConfigEditorRoutingModule,
    MatTableModule,
    MatProgressBarModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    MatButtonModule
  ]
})
export class ConfigEditorModule { }
