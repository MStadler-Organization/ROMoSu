import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, Validators} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {NewConfigWizardService} from "./new-config-wizard.service";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {MatCheckboxChange} from "@angular/material/checkbox";


/////////// TS INTERFACES ///////////

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

  /////////// CLASS VARIABLES ///////////

  firstFormGroup = this._formBuilder.group({});
  secondFormGroup = this._formBuilder.group({});

  treeNodeIdx: number = -1
  selectedSum: string = ''
  possibleSums: string[] = []
  treeData: TreeNodeElement[] = []
  showProgressBar: boolean = true

  // validate input
  FQ_PATTERN: string = '\\d+([.]\\d+)?'
  FQ_REGEX = new RegExp(this.FQ_PATTERN);
  FREQUENCY_FORM_CONTROL = new FormControl('', [Validators.required, Validators.pattern(this.FQ_PATTERN)]);

  // primitive ROS datatypes
  PRIMITIVE_ROS_TYPES: string[] = ['bool', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'string'];

  frequencies: { value: number, isCorrect: boolean }[] = []
  checkBoxes: any[] = []

  /////////// CONSTRUCTOR ///////////

  constructor(private _formBuilder: FormBuilder, public newConfigWizardService: NewConfigWizardService, public dialog: MatDialog) {
  }


  /////////// FUNCTIONS ///////////

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

    // init Checkbox values
    this.setCheckBoxesAndFQs()

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
    const nodeIndex = this.treeNodeIdx

    // check if type is a primitive
    if (this.isPrimitiveDataType(dataType)) {
      let primitiveTreeNodeElement: TreeNodeElement = {
        name: typeName,
        dataType: dataType,
        isExpandable: false, // since this is a primitive one
        isChecked: false, // default
        index: nodeIndex
      }
      return primitiveTreeNodeElement
    } else {
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
          index: nodeIndex
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
   * @param currentNodeIdx treeNodeElements index
   * @param parentNodeIdx
   */
  onCheckboxChange($event: MatCheckboxChange, currentNodeIdx: number, parentNodeIdx: number) {
    // find treeNode element in data
    const searchNode = this.searchTreeNode(currentNodeIdx)
    if (searchNode) {
      const checkedAction = $event.checked
      // set data for form
      searchNode['isChecked'] = $event.checked
      this.checkBoxes[searchNode.index] = checkedAction
      // update the children with value
      this.updateChildrenCheckboxes(searchNode, checkedAction)

      // if checked and all other children of a parent are also checked, parent must be checked
      if (checkedAction) {
        this.checkParentChecking(parentNodeIdx)
      }

      // if unchecked, parent is also unchecked since at least on child is not checked
      if (!checkedAction && parentNodeIdx) {
        this.setParentOff(parentNodeIdx)
      }
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
        childNode['isChecked'] = pChecked
        this.checkBoxes[childNode.index] = pChecked
        this.updateChildrenCheckboxes(childNode, pChecked)
      }
    }
  }

  /***
   * Called when clicking on 'Next'-button on step two
   * @param stepper the stepper mat component
   */
  goToStepThreeButtonClicked(stepper: MatStepper) {
    // validate checkbox selection
    if (this.checkBoxes.filter(Boolean).length < 1) {
      // at least one topic must be selected to monitor
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create error
          message: 'At least one property must be selected for monitoring!'
        },
        autoFocus: false // disable default focus on button
      });
      return
    }

    // validate frequency
    for (const fq of this.frequencies) {
      if (!fq.isCorrect) {
        // at least on frequency input is not correct
        this.dialog.open(CustomDialogComponent, {
          data: {
            type: 2, // create error
            message: 'At least one frequency input field is not filled out properly. All frequencies must be assigned and filled only with floating point numbers!'
          },
          autoFocus: false // disable default focus on button
        });
        return;
      }
    }

    // all inputs are correct, go to step three
    stepper.next()
  }

  /***
   * <i>Workaround:</i>
   * Called when a frequency changes and stores the value in the formgroup
   * @param $event the event which is fired when the frequency changes
   * @param idx the index of the leafnode
   */
  onFrequencyChange($event: any, idx: number) {
    const val = $event.target.value
    this.frequencies[idx] = {value: val, isCorrect: this.FQ_REGEX.test(val)}
  }

  /**
   * Searches for an index in the treeData and returns the corresponding TreeNode. If no treeNode is found, null is returned
   * @param idx the index to search for in the treeData
   * @private
   */
  private searchTreeNode(idx: number) {
    for (const leafNode of this.treeData) {
      const searchedNode = this._searchForIdx(leafNode, idx)
      if (searchedNode) return searchedNode
    }
    console.error(`Invalid index for treenode search: ${idx}`)
    return null
  }

  /***
   * Searches in a given treeNode for a specific index. <i>Do not use this class for searching a node, instead use "searchTreeNode" function!!!</i>
   * @param treeNode the treeNode in which is searched
   * @param pSearchIdx the index which is searched for
   * @private
   */
  private _searchForIdx(treeNode: TreeNodeElement, pSearchIdx: number): TreeNodeElement | null {
    // check if this is the searched node
    if (treeNode.index === pSearchIdx) {
      return treeNode
    }
    // check the children
    if (treeNode.children) {
      for (const childNode of treeNode.children) {
        let searchNode = this._searchForIdx(childNode, pSearchIdx)
        if (searchNode) return searchNode
      }
    }
    // if still not found, this node has not the index
    return null
  }

  /**
   * Helper function which initiates the checkboxes class variable with the length of the treenodes and sets them all to false
   * @private
   */
  private setCheckBoxesAndFQs() {
    for (let i = 0; i < this.treeNodeIdx + 1; i++) {
      this.checkBoxes[i] = false
    }
    for (let j = 0; j < this.treeData.length; j++) {
      this.frequencies[j] = {value: -1, isCorrect: false}
    }
  }

  /**
   * Adds a 'checkbox-' as prefix to a number and returns it as a string
   * @param index the number to add as suffix
   */
  getCcheckBoxIdString(index: number): string {
    return `checkbox-${index}`;
  }

  /**
   * Returns the index contained in an id string as a number. E.g., 'checkbox-34' -> 34
   * @param idString the id string
   */
  getCheckBoxIdFromString(idString: string): number {
    return +idString.substring(idString.indexOf('-') + 1)
  }

  /***
   * Sets recursively a parent nodes to unchecked state.
   * @param parentNodeIdx the index of the parent node which will be unchecked (and its parent)
   * @private
   */
  private setParentOff(parentNodeIdx: number) {
    // get the actual node
    let parentSearchNode = this.searchTreeNode(parentNodeIdx)
    // set the checked attribute to false
    if (parentSearchNode) {
      parentSearchNode['isChecked'] = false
      this.checkBoxes[parentNodeIdx] = false
      let parentCheckbox = document.getElementById(this.getCcheckBoxIdString(parentNodeIdx))
      if (parentCheckbox) {
        // @ts-ignore
        parentCheckbox.classList.remove('mat-checkbox-checked')
        // check if this one also has a parent
        let parentParentIdString = parentCheckbox.getAttribute('ng-reflect-name')
        // if this node is unchecked, also uncheck the parents parent if a parent exists (no leaf nodes)
        if (parentParentIdString) {
          this.setParentOff(this.getCheckBoxIdFromString(parentParentIdString))
        }
      }
    }
  }

  /***
   * Checks recursively if a given node index's children are checked and then checks the parent
   * @param parentNodeIdx the index of the parent node
   * @private
   */
  private checkParentChecking(parentNodeIdx: number) {
    // get the node of the parent
    let parentSearchNode = this.searchTreeNode(parentNodeIdx)
    if (parentSearchNode && parentSearchNode.children) {
      // set initial value to true
      let allChildrenChecked = true
      for (const childNode of parentSearchNode.children) {
        if (!childNode.isChecked) {
          // found a children which is not checked -> do not check this parent
          allChildrenChecked = false
          break;
        }
      }
      // if all children are checked, check the parent
      if (allChildrenChecked) {
        parentSearchNode['isChecked'] = true
        this.checkBoxes[parentNodeIdx] = true
        let parentCheckbox = document.getElementById(this.getCcheckBoxIdString(parentNodeIdx))
        if (parentCheckbox) {
          // @ts-ignore
          parentCheckbox.classList.add('mat-checkbox-checked')
          // check if this one also has a parent
          let parentParentIdString = parentCheckbox.getAttribute('ng-reflect-name')

          // since this node is now checked, also check this nodes parent
          if (parentParentIdString) {
            this.checkParentChecking(this.getCheckBoxIdFromString(parentParentIdString))
          }
        }
      }
    }
  }
}
