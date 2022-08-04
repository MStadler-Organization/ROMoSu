/////////// TS INTERFACES ///////////

export interface TreeNodeElement {
  name: string;
  dataType: string;
  isExpandable: boolean;
  isChecked: boolean;
  children?: TreeNodeElement[];
  index: number;
}

export interface Field {
  fieldName: string;
  fieldDataType: string;
}

export interface SumType {
  id: number;
  name: string;
}

export interface ConfigFileData {
  fileName: string;
  saveType: string;
  sumTypeId: number;
  propertyTree: TreeNodeElement[];
  frequencies: number[];
}
