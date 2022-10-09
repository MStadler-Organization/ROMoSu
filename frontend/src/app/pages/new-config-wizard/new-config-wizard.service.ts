import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ConfigFileData} from "../../shared/models/interfaces";

interface SumType {
  id: number;
  name: string;
}

@Injectable({
  providedIn: "root"
})
export class NewConfigWizardService {

  private readonly baseApiURL: string;

  constructor(private readonly http: HttpClient) {
    this.baseApiURL = "http://127.0.0.1:8000/";
  }

  /**
   * REST call to server to get possible SuMs
   */
  getSuMs(): Observable<string[]> {
    return this.http.get<string[]>(this.baseApiURL + "possible-sums/");
  }

  /**
   * REST call to server to get topics associated with a selected SuM
   * @param pSum the name of the SuM as string
   */
  getPropsForSum(pSum: string): Observable<any> {
    return this.http.get<any>(this.baseApiURL + `props-for-sum/?sum=${pSum}`);
  }

  /**
   * REST call to server to get the Sum types
   */
  getSumTypes(): Observable<SumType[]> {
    return this.http.get<SumType[]>(this.baseApiURL + "sum-types/");
  }

  /**
   * REST call to server to get the Sum types
   * @param pSumType The new sum type name which should be created
   */
  addSumType(pSumType: string): Observable<SumType> {
    return this.http.post<SumType>(this.baseApiURL + "sum-types/", {name: pSumType});
  }

  /**
   * REST call to server to generate and save a new configuration
   * @param configFileData The data for the new configuration file
   */
  createNewConfigFile(configFileData: ConfigFileData): Observable<any> {
    // @ts-ignore
    configFileData.property_tree = ''
    // @ts-ignore
    configFileData.frequencies = ''
    return this.http.post<any>(this.baseApiURL + "config-file/", {configFileData});
  }
}
