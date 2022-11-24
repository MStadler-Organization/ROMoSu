import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ConfigEditorRoutingModule } from './config-editor-routing.module';
import { ConfigEditorComponent } from './config-editor.component';


@NgModule({
  declarations: [
    ConfigEditorComponent
  ],
  imports: [
    CommonModule,
    ConfigEditorRoutingModule
  ]
})
export class ConfigEditorModule { }
