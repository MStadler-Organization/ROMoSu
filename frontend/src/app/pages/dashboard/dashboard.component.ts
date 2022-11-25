import {Component, OnInit} from '@angular/core';
import {RTConfig} from "../../shared/models/interfaces";
import {DashboardService} from "./dashboard.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  activeConfigs: RTConfig[] = <RTConfig[]>{}

  constructor(public dashboardService: DashboardService) {
  }

  ngOnInit(): void {
    this.dashboardService.getActiveRTConfigs().subscribe((activeConfigs) => {
      this.activeConfigs = activeConfigs
    })
  }

}
