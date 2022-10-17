import {Component, OnInit} from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {RuntimeMonitoringWizardService} from "./runtime-monitoring-wizard.service";
import {MatStepper} from "@angular/material/stepper";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {ConfigFileData, RTConfig, SumType} from "../../shared/models/interfaces";

@Component({
  selector: 'app-runtime-monitoring-wizard',
  templateUrl: './runtime-monitoring-wizard.component.html',
  styleUrls: ['./runtime-monitoring-wizard.component.scss']
})
export class RuntimeMonitoringWizardComponent implements OnInit {

  /////////// CLASS VARIABLES ///////////

  firstFormGroup = this._formBuilder.group({});
  secondFormGroup = this._formBuilder.group({});
  runtimeConfigResult: RTConfig = {sum_prefix: '', sum_type_id: -1, config_id: -1}
  possibleSums: string[] = []
  showProgressBar: boolean = true
  sumTypes: SumType[] = []
  possibleConfigs: ConfigFileData[] = []

  constructor(private _formBuilder: FormBuilder, public runtimeMonitoringWizardService: RuntimeMonitoringWizardService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.runtimeMonitoringWizardService.getSuMs().subscribe((possibleSums: string[]) => {
      this.showProgressBar = false
      this.possibleSums = possibleSums.sort()
    })
  }


  /***
   * Called when step 1 next button is clicked
   * @param sums the selection of the possible sum-list
   * @param stepper the stepper mat component
   */
  goToStepTwoButtonClicked(sums: { selectedOptions: { selected: { value: string; }[]; }; }, stepper: MatStepper) {

    this.runtimeConfigResult.sum_prefix = sums.selectedOptions.selected[0]?.value

    if (!this.runtimeConfigResult.sum_prefix && this.runtimeConfigResult.sum_prefix != '') {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create error
          message: 'No System under Monitoring selected!'
        },
        autoFocus: false // disable default focus on button
      });
    } else {
      stepper.next() // go to next step
      this.showProgressBar = true
      this.runtimeMonitoringWizardService.getSumTypes().subscribe((restSumTypes) => {
        for (const singleSumType of restSumTypes) {
          this.sumTypes.push(singleSumType)
        }
        this.showProgressBar = false
      });
    }
  }

  /***
   * Called when step 2 next button is clicked
   * @param sumsTypes the selection of the possible sum-list
   * @param stepper the stepper mat component
   */
  goToStepThreeButtonClicked(sumsTypes: { selectedOptions: { selected: { value: string; }[]; }; }, stepper: MatStepper) {

    this.runtimeConfigResult.sum_type_id = +sumsTypes.selectedOptions.selected[0]?.value

    if (!this.runtimeConfigResult.sum_type_id && this.runtimeConfigResult.sum_type_id != -1) {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create error
          message: 'No Type selected!'
        },
        autoFocus: false // disable default focus on button
      });
    } else {
      stepper.next() // go to next step
      this.showProgressBar = true
      this.runtimeMonitoringWizardService.getConfigsForSuMType(this.runtimeConfigResult.sum_type_id).subscribe((configList: ConfigFileData[]) => {
        for (const singleConfig of configList) {
          this.possibleConfigs.push(singleConfig)
        }
        this.showProgressBar = false
      });
    }
  }
}
