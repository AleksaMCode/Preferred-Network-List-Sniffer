import InitFirebase from "../databaseConfig/index";
import React from "react";
import { ref, onValue } from "firebase/database";
import { Table } from "react-bootstrap";
import dateFormat from "dateformat";

const db = InitFirebase();
console.log(db);
export class PnlData extends React.Component {
  constructor() {
    super();
    this.state = {
      tableData: [],
    };
  }

  componentDidMount() {
    console.log("/" + dateFormat(new Date(), "yyyymmdd"));
    const dbRef = ref(db, "/" + dateFormat(new Date(), "yyyymmdd"));

    onValue(dbRef, (snapshot) => {
      let records = [];
      snapshot.forEach((childSnapshot) => {
        let keyName = childSnapshot.key;
        let data = childSnapshot.val();
        records.push({ key: keyName, data: data });
      });
      console.log(records);
      this.setState({ tableData: records });
    });
  }

  render() {
    return (
      <Table>
        <thead>
          <tr>
            <th>N.</th>
            <th>SSID</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {this.state.tableData.map((row, index) => {
            return (
              <tr>
                <td>{index + 1}</td>
                <td>{row.key}</td>
                <td>{row.data.timestamp}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    );
  }
}
