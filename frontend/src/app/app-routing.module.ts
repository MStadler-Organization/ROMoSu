import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

const routes: Routes = [{
  path: '',
  redirectTo: '/home',
  pathMatch: 'full'
}, {
  path: 'home',
  loadChildren: () => import('./pages/home/home.module').then(m => m.HomeModule)
},
  {
    path: 'legal-notice',
    loadChildren: () => import('./pages/legal-notice/legal-notice.module').then(m => m.LegalNoticeModule)
  },
  {path: 'impress', loadChildren: () => import('./pages/impress/impress.module').then(m => m.ImpressModule)},
  {path: 'about', loadChildren: () => import('./pages/about/about.module').then(m => m.AboutModule)},
  {
    path: 'new-config-wizard',
    loadChildren: () => import('./pages/new-config-wizard/new-config-wizard.module').then(m => m.NewConfigWizardModule)
  },
  {
    path: 'manage-sum-types',
    loadChildren: () => import('./pages/manage-sum-types/manage-sum-types.module').then(m => m.ManageSumTypesModule)
  },
  {
    path: 'runtime-monitoring-wizard',
    loadChildren: () => import('./pages/runtime-monitoring-wizard/runtime-monitoring-wizard.module').then(m => m.RuntimeMonitoringWizardModule)
  },
  {
    path: 'config-editor',
    loadChildren: () => import('./pages/config-editor/config-editor.module').then(m => m.ConfigEditorModule)
  },
  {path: 'dashboard', loadChildren: () => import('./pages/dashboard/dashboard.module').then(m => m.DashboardModule)}];

@NgModule({
  declarations: [],
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
