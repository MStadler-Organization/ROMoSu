import {Component, OnInit} from '@angular/core';
import {ConfigFileData, RTConfig, SumType} from "../../shared/models/interfaces";
import {DashboardService} from "./dashboard.service";
import {MatDialog} from "@angular/material/dialog";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {LoadingDialogComponent} from "../../shared/components/loading-dialog/loading-dialog.component";
import {RtDataDialogComponent} from "../../shared/components/rt-data-dialog/rt-data-dialog.component";

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

  constructor(public dashboardService: DashboardService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
    // get all the data from server
    this.dashboardService.getActiveRTConfigs().subscribe((activeConfigs: RTConfig[]) => {
      // check if there are any active monitors going on
      if (activeConfigs.length === 0) {
        this.showNothingToShowDialog()
        this.showProgressBar = false
        return
      }

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
    let qTime = ''
    let qDate = ''
    if (clickedConfig.query_time) {
      qTime = this.getTime(clickedConfig.query_time)
      qDate = this.getDate(clickedConfig.query_time)
    }

    this.dialog.open(RtDataDialogComponent, {
      data: {conf: clickedConfig, queryTime: qTime, queryDate: qDate},
      autoFocus: false // disable default focus on button
    });
  }

  /**
   * Called, when clicking on the 'Stop Monitoring' button.
   * @param clickedConfig The config on which the button is clicked on.
   */
  onStopMonitoringBtnClicked(clickedConfig: RTConfig) {
    if (clickedConfig.id) {
      const spinnerDialog = this.dialog.open(LoadingDialogComponent, {disableClose: true});

      this.dashboardService.stopMonitoring(clickedConfig.id).subscribe((deletedConfig) => {
        // delete from view as well
        let removeIdx = -1
        this.activeConfigs.forEach((singleRTConfig, idx) => {
          if (singleRTConfig.id === deletedConfig.id) {
            removeIdx = idx
          }
        })
        if (removeIdx > -1) {
          this.activeConfigs.splice(removeIdx, 1)
        }
        if (this.activeConfigs.length === 0) {
          this.showNothingToShowDialog()
        }
        spinnerDialog.close()
      })
    } else {
      console.error('Runtime config does not yield ID')
    }
  }

  /**
   * Returns the date from a given time string
   * @param start_time
   */
  getDate(start_time: string) {
    return start_time.substring(0, start_time.indexOf(' '))
  }

  /**
   * Returns the time from a given time string
   * @param timeString
   */
  getTime(timeString: string) {
    return timeString.substring(timeString.indexOf(' ') + 1, timeString.indexOf('.'))
  }

  /**
   * Displays a dialog to notify the user that nothing can be displayed.
   * @private
   */
  private showNothingToShowDialog() {
    this.dialog.open(CustomDialogComponent, {
      data: {
        type: 0, // create info
        message: 'No active runtime monitoring is currently going on to show here!'
      },
      autoFocus: false // disable default focus on button
    });
  }
}
