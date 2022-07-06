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
  { path: 'legal-notice', loadChildren: () => import('./pages/legal-notice/legal-notice.module').then(m => m.LegalNoticeModule) },
  { path: 'impress', loadChildren: () => import('./pages/impress/impress.module').then(m => m.ImpressModule) },
  { path: 'about', loadChildren: () => import('./pages/about/about.module').then(m => m.AboutModule) }];

@NgModule({
  declarations: [],
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
