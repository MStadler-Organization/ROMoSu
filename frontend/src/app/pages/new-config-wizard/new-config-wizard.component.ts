import {Component, OnInit} from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {NewConfigWizardService} from "./new-config-wizard.service";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";


@Component({
  selector: 'app-new-config-wizard',
  templateUrl: './new-config-wizard.component.html',
  styleUrls: ['./new-config-wizard.component.scss']
})
export class NewConfigWizardComponent implements OnInit {
  firstFormGroup = this._formBuilder.group({
    firstCtrl: [''],
    // firstCtrl: ['', Validators.required],
  });
  secondFormGroup = this._formBuilder.group({
    secondCtrl: [''],
    // secondCtrl: ['', Validators.required],
  });

  selectedSum: string = ''
  possibleSums: string[] = []
  propertyData: any
  showProgressBar: boolean = true

  constructor(private _formBuilder: FormBuilder, public newConfigWizardService: NewConfigWizardService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.newConfigWizardService.getSuMs().subscribe((possibleSums: string[]) => {
      this.showProgressBar = false
      this.possibleSums = possibleSums.sort()
    })
  }

  /***
   * Called when step 1 next button is clicked
   * @param sums the selection of the possible sum-list
   * @param stepper the stepper mat component
   */
  validateSumSelection(sums: { selectedOptions: { selected: { value: string; }[]; }; }, stepper: MatStepper) {

    this.selectedSum = sums.selectedOptions.selected[0]?.value


    if (!this.selectedSum) {
      let dialogRef = this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create error
          message: 'No System under Monitoring selected!'
        },
        autoFocus: false // disable default focus on button
      });
    } else {
      stepper.next() // go to next step
      this.showProgressBar = true
      this.newConfigWizardService.getPropsForSum(this.selectedSum).subscribe(sumDetails => {
        this.showProgressBar = false
        console.log(sumDetails)
        this.setTreeData(sumDetails)
      })
    }
  }

  /**
   * Sets the data for the tree view in step 2
   * @param sumDetails the REST response
   */
  setTreeData(sumDetails: any) {
    let treeData: any[] = []

    for (const rootTopic of sumDetails) {
      treeData.push({name: rootTopic['in_topic'], type: rootTopic['type']})
    }

    console.log(treeData)

    this.propertyData = treeData
  }
}
