import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-custom-dialog',
  templateUrl: './custom-dialog.component.html',
  styleUrls: ['./custom-dialog.component.scss']
})

/**
 * `data: { type: number, message: string }`. Whereby type 0 = info, type 1 = success, type 2 = error
 */
export class CustomDialogComponent {

  type: number = -1
  message: string = ''

  /***
   * Creates a parameterized dialog
   * @param dialogRef the CustomDialogComponent
   * @param data the params in the form of
   * `data: { type: number, message: string }`. Whereby type 0 = info, type 1 = success, type 2 = error
   */
  constructor(public dialogRef: MatDialogRef<CustomDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: { type: number, message: string }) {
    this.type = data.type;
    if (this.type < 0 || this.type > 2) {
      this.type = 0
      console.warn(`Got invalid param for custom dialog: ${data.type}`)
    }
    this.message = data.message;
  }

  /**
   * OK button clicked. Closes the dialog
   */
  onClickOk() {
    this.dialogRef.close();
  }
}
