import {Component, OnInit} from '@angular/core';
import {ConfigFileData, RTConfig, SumType} from "../../shared/models/interfaces";
import {DashboardService} from "./dashboard.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  showProgressBar: boolean = true
  activeConfigs: RTConfig[] = <RTConfig[]>[]
  sumTypes: SumType[] = <SumType[]>[]
  allMonConfigs: ConfigFileData[] = <ConfigFileData[]>[]

  constructor(public dashboardService: DashboardService) {
  }

  ngOnInit(): void {
    // get all the data from server
    this.dashboardService.getActiveRTConfigs().subscribe((activeConfigs: RTConfig[]) => {
      this.activeConfigs = activeConfigs
      this.dashboardService.getAllConfigs().subscribe((allMonConfigs: ConfigFileData[]) => {
        // map the FK to the actual configs
        for (const singleActiveConfig of this.activeConfigs) {
          for (const monConfig of allMonConfigs) {
            if (monConfig.id === singleActiveConfig.config_id) {
              singleActiveConfig.config_file_data = monConfig
            }
          }
        }
        this.allMonConfigs = allMonConfigs
        this.isFinished()
      })
    })
    this.dashboardService.getSumTypes().subscribe((sumTypes) => {
      this.sumTypes = sumTypes
      this.isFinished()
    })
  }

  /**
   * Gets the name of a SuM-Type for an ID
   * @param sumTypeId the id which is searched for
   */
  getSumTypeNameForId(sumTypeId: number | undefined) {
    for (const sumType of this.sumTypes) {
      if (sumType.id === sumTypeId) {
        return sumType.name
      }
    }
    console.error(`No SumType for ID: ${sumTypeId}`)
    return 'undefined'
  }

  /**
   * Checks if the progressbar is still needed or if all REST calls are finished. Returns true if all is finished.
   * @private
   */
  isFinished() {
    if (this.allMonConfigs.length > 0 && this.activeConfigs.length > 0 && this.sumTypes.length > 0) {
      this.showProgressBar = false
      return true
    }
    return false
  }

  /**
   * Called, when clicking on the 'Show Data' button.
   * @param clickedConfig The config on which the button is clicked on.
   */
  onShowDataBtnClicked(clickedConfig: RTConfig) {
    console.log(clickedConfig)
  }

  /**
   * Called, when clicking on the 'Stop Monitoring' button.
   * @param clickedConfig The config on which the button is clicked on.
   */
  onStopMonitoringBtnClicked(clickedConfig: RTConfig) {
    console.log(clickedConfig)
  }
}
