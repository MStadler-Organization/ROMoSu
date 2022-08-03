import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, Validators} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {NewConfigWizardService} from "./new-config-wizard.service";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {MatCheckboxChange} from "@angular/material/checkbox";


interface TreeNodeElement {
  name: string;
  dataType: string;
  isExpandable: boolean;
  isChecked: boolean;
  children?: TreeNodeElement[];
  index: number;
}

interface Field {
  fieldName: string;
  fieldDataType: string;
}

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

  treeNodeIdx: number = -1
  selectedSum: string = ''
  possibleSums: string[] = []
  treeData: TreeNodeElement[] = []
  showProgressBar: boolean = true

  // validate input
  FREQUENCY_FORM_CONTROL = new FormControl('', [Validators.required, Validators.pattern('\\d+([.]\\d+)?')]);

  // primitive ROS datatypes
  PRIMITIVE_ROS_TYPES: string[] = ['bool', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'string'];

  frequencies: number[] = []
  checkBoxes: number[] = []

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
  goToStepTwoButtonClicked(sums: { selectedOptions: { selected: { value: string; }[]; }; }, stepper: MatStepper) {

    this.selectedSum = sums.selectedOptions.selected[0]?.value


    if (!this.selectedSum) {
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
      this.newConfigWizardService.getPropsForSum(this.selectedSum).subscribe(sumDetails => {
        this.setTreeData(sumDetails)
        this.showProgressBar = false
      })
    }
  }

  /**
   * Sets the data for the tree view in step 2
   * @param sumDetails the REST response
   */
  private setTreeData(sumDetails: any) {

    let typeDefArray: any[] = []
    let treeDataArray: TreeNodeElement[] = []

    // iterate over root topics
    for (const rootTopic of sumDetails) {
      // get the type definition of every topic and iterate over them
      typeDefArray = rootTopic.type_info.data.typedefs

      // create tree data structure for the topic
      let childTreeForRootTopic = this.getChildNodesForType(rootTopic.in_topic, rootTopic.type, typeDefArray)


      // add tree to the list
      treeDataArray.push(<TreeNodeElement>childTreeForRootTopic)
    }

    this.treeData = treeDataArray

    console.log(this.treeData)
  }

  /**
   * Recursive function for creating TreeNodeElements based on a datatype and a typeDef array
   * @param typeName the better human readably name of the type
   * @param dataType the full datatype name, either a complex one or a primitive one as string (e.g., "sensor_msgs/JointState", or "float64")
   * @param typeDefArray the type definition array provided by the ROS-bridge containing the information of the requested datatype
   * @private
   */
  private getChildNodesForType(typeName: string, dataType: string, typeDefArray: any[]) {

    this.treeNodeIdx += 1

    // check if type is a primitive
    if (this.isPrimitiveDataType(dataType)) {
      let primitiveTreeNodeElement: TreeNodeElement = {
        name: typeName,
        dataType: dataType,
        isExpandable: false, // since this is a primitive one
        isChecked: false, // default
        index: this.treeNodeIdx
      }
      return primitiveTreeNodeElement
    } else {
      // const typeIdx = typeDefArray['type'].indexOf(typeName)
      const typeIdx = this.findIdxInTypeDef(dataType, typeDefArray)
      if (typeIdx != -1) {
        // type exists

        // get type in array
        const singleTypeDef = typeDefArray[typeIdx]


        // get fields of datatype
        let fields: Field[] = []

        // gather all the fields of the complex datatype
        for (let i = 0; i < singleTypeDef.fieldnames.length; i++) {
          let newField: Field = {
            fieldName: singleTypeDef.fieldnames[i],
            fieldDataType: singleTypeDef.fieldtypes[i]
          }
          fields.push(newField)
        }

        // get nodes of children for all fields
        let childrenTreeNodes: TreeNodeElement[] = []
        for (const singleField of fields) {
          let newChildNode = this.getChildNodesForType(singleField.fieldName, singleField.fieldDataType, typeDefArray)
          childrenTreeNodes.push(<TreeNodeElement>newChildNode)
        }

        // get childDataTypes
        let nonPrimitiveTreeNodeElement: TreeNodeElement = {
          name: typeName,
          dataType: dataType,
          isExpandable: true,
          isChecked: false,
          children: childrenTreeNodes,
          index: this.treeNodeIdx
        }
        return nonPrimitiveTreeNodeElement
      } else {
        console.error('Something went wrong in creating data tree')
        return []
      }
    }
  }

  /***
   * Returns the index of a type in an array of type definitions. If type is not contained, -1 is returned.
   * @param typeName the type to search for
   * @param typeDefArray the array in which the type is searched
   * @private
   */
  private findIdxInTypeDef(typeName: string, typeDefArray: any) {
    for (let i = 0; i < typeDefArray.length; i++) {
      if (typeName === typeDefArray[i].type) {
        return i
      }
    }
    return -1
  }


  /**
   * Checks whether a given string type is a primitive ROS datatype
   * @param type a datatype name as string
   */
  private isPrimitiveDataType(type: string) {
    return this.PRIMITIVE_ROS_TYPES.includes(type);
  }

  /***
   * Called when a checkbox in step 2 is checked or unchecked
   * @param $event the event which happened (contains the data about checked or unchecked)
   * @param idx treeNodeElements index
   */
  onCheckboxChange($event: MatCheckboxChange, idx: number) {
    // find treeNode element in data
    const searchNode = this.searchTreeNode(idx)
    if (searchNode) {
      // update the children with value
      this.updateChildrenCheckboxes(searchNode, $event.checked)
    }
  }

  /***
   * Updates the parent and children checkboxes of a tree node recursively, e.g., parent is checked -> all children are checked
   * @param treeNodeElement the parent treenode element
   * @param pChecked boolean whether to check or uncheck the nodes
   * @private
   */
  private updateChildrenCheckboxes(treeNodeElement: TreeNodeElement, pChecked: boolean) {
    if (treeNodeElement.isExpandable && treeNodeElement.children) {
      for (const childNode of treeNodeElement.children) {
        childNode.isChecked = pChecked
        this.updateChildrenCheckboxes(childNode, pChecked)
      }
    }
  }

  /***
   * Called when clicking on 'Next'-button on step two
   * @param stepper the stepper mat component
   */
  goToStepThreeButtonClicked(stepper: MatStepper) {
    console.log(this.frequencies)
  }

  /***
   * <i>Workaround:</i>
   * Called when a frequency changes and stores the value in the formgroup
   * @param $event the event which is fired when the frequency changes
   * @param idx the index of the leafnode
   */
  onFrequencyChange($event: any, idx: number) {
    this.frequencies[idx] = $event.target.value
  }

  private searchTreeNode(idx: number) {
    for (const leafNode of this.treeData) {
      const searchedNode = this.searchForIdx(leafNode, idx)
      if (searchedNode) return searchedNode
    }
    console.error(`Invalid index for treenode search: ${idx}`)
    return null
  }

  private searchForIdx(treeNode: TreeNodeElement, idx: number): TreeNodeElement | null {
    // check if this is the searched node
    if (treeNode.index === idx) {
      return treeNode
    }
    // check the children
    if (treeNode.children) {
      for (const childNode of treeNode.children) {
        let searchNode = this.searchForIdx(childNode, idx)
        if (searchNode) return searchNode
      }
    }
    // if still not found, this node has not the index
    return null
  }
}
