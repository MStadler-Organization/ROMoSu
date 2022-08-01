import {Component, OnInit} from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {NewConfigWizardService} from "./new-config-wizard.service";

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

  constructor(private _formBuilder: FormBuilder, public newConfigWizardService: NewConfigWizardService) {
  }

  ngOnInit(): void {
    this.newConfigWizardService.getSuMs().subscribe((possibleSums: string[]) => {
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
      // todo: show dialog or something
    } else {
      stepper.next()
    }
  }
}
