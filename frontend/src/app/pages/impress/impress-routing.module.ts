import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ImpressComponent } from './impress.component';

const routes: Routes = [{ path: '', component: ImpressComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ImpressRoutingModule { }
