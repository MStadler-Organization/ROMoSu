import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ConfigEditorComponent } from './config-editor.component';

const routes: Routes = [{ path: '', component: ConfigEditorComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ConfigEditorRoutingModule { }
