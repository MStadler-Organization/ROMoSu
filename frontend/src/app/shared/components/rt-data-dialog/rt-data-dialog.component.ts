import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {RTConfig} from "../../models/interfaces";


@Component({
  selector: 'app-rt-data-dialog',
  templateUrl: './rt-data-dialog.component.html',
  styleUrls: ['./rt-data-dialog.component.scss']
})
export class RtDataDialogComponent {

  rt_data: RTConfig;

  /***
   * Creates a parameterized dialog
   * @param dialogRef the CustomDialogComponent
   * @param data the rt data params
   */
  constructor(public dialogRef: MatDialogRef<RtDataDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: RTConfig) {
    this.rt_data = data
  }

  /**
   * OK button clicked. Closes the dialog
   */
  onClickOk() {
    this.dialogRef.close();
  }

  /***
   * Adds dots to data longer than 10 chars
   * @param last_data the string to be previewed
   */
  getPreviewData(last_data: string) {
    if (last_data.length > 10) {
      return last_data.substring(0, 10) + '...'
    } else {
      return last_data
    }
  }
}
