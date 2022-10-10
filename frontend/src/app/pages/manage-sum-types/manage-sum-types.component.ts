import {Component, OnInit} from '@angular/core';
import {SumType} from "../../shared/models/interfaces";
import {ManageSumTypesService} from "./manage-sum-types.service";
import {FormBuilder} from "@angular/forms";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";

@Component({
  selector: 'app-manage-sum-types',
  templateUrl: './manage-sum-types.component.html',
  styleUrls: ['./manage-sum-types.component.scss']
})
export class ManageSumTypesComponent implements OnInit {


  showProgressBar: boolean = true
  sumTypes: SumType[] = []
  displayedCols: string[] = ['id', 'name', 'action']
  newSumFormGroup = this._formBuilder.group({
    newSumTypeInput: [''],
  });

  /////////// CONSTRUCTOR ///////////

  constructor(private _formBuilder: FormBuilder, public manageSumTypesService: ManageSumTypesService, public dialog: MatDialog) {
  }

  /////////// FUNCTIONS ///////////

  ngOnInit(): void {
    this.manageSumTypesService.getSumTypes().subscribe((sumTypes: SumType[]) => {
      this.showProgressBar = false
      this.sumTypes = sumTypes
    })
  }

  /**
   * Called when clicking on delete SuM-Type
   * @param sumTypeIdToDelete
   */
  deleteButtonClicked(sumTypeIdToDelete: number) {
    // delete from table
    for (let i = 0; i < this.sumTypes.length; i++) {
      if (this.sumTypes[i].id === sumTypeIdToDelete) {
        this.sumTypes.splice(i, 1)
        location.reload();
      }
    }
    this.manageSumTypesService.deleteSumType(sumTypeIdToDelete).subscribe(response => {
      console.log(response)
    })
  }

  /**
   * Called when the add button is clicked.
   */
  addButtonClicked() {
    const newSumTypeName = this.newSumFormGroup.get('newSumTypeInput')?.value
    if (newSumTypeName) {
      this.manageSumTypesService.addSumType(newSumTypeName).subscribe((response: SumType) => {
        this.sumTypes.push(response)
        location.reload();
      })
    } else {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create error
          message: 'Enter a name for the new SuM type!'
        },
        autoFocus: false // disable default focus on button
      });
    }
  }
}
