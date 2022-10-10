import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {SumType} from "../../shared/models/interfaces";

@Injectable({
  providedIn: "root"
})
export class ManageSumTypesService {

  private readonly baseApiURL: string;

  constructor(private readonly http: HttpClient) {
    this.baseApiURL = "http://127.0.0.1:8000/";
  }


  /**
   * REST call to server to get the Sum types
   */
  getSumTypes(): Observable<SumType[]> {
    return this.http.get<SumType[]>(this.baseApiURL + "sum-types/");
  }

  /**
   * REST call to server to add a new sum types
   * @param pSumType The new sum type name which should be created
   */
  addSumType(pSumType: string): Observable<SumType> {
    return this.http.post<SumType>(this.baseApiURL + "sum-types/", {name: pSumType});
  }

  /**
   * REST call to server to delete a sum type
   * @param pSumTypeId The sum type id to delete
   */
  deleteSumType(pSumTypeId: number): Observable<SumType> {
    return this.http.delete<SumType>(this.baseApiURL + `sum-types/?id=${pSumTypeId}`);
  }
}
