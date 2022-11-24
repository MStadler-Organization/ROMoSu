import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ConfigEditorRoutingModule} from './config-editor-routing.module';
import {ConfigEditorComponent} from './config-editor.component';
import {MatTableModule} from "@angular/material/table";
import {MatProgressBarModule} from "@angular/material/progress-bar";


@NgModule({
  declarations: [
    ConfigEditorComponent
  ],
  imports: [
    CommonModule,
    ConfigEditorRoutingModule,
    MatTableModule,
    MatProgressBarModule
  ]
})
export class ConfigEditorModule { }
