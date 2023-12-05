import InitFirebase from '../databaseConfig/index'
import React from 'react'
import { ref, onValue } from 'firebase/database'
import { Table } from 'react-bootstrap'
import dateFormat from 'dateformat'
import { motion } from 'framer-motion'

const db = InitFirebase()
export class PnlData extends React.Component {
  constructor() {
    super()
    this.state = {
      tableData: [],
    }
  }

  componentDidMount() {
    const dbRef = ref(db, '/' + dateFormat(new Date(), 'yyyymmdd'))

    onValue(dbRef, (snapshot) => {
      let records = []
      snapshot.forEach((childSnapshot) => {
        let key = childSnapshot.key
        let data = childSnapshot.val()
        records.push({ key: key, data: data })
      })
      this.setState({ tableData: records })
    })
  }

  render() {
    return (
      <Table striped bordered hover>
        <thead style={{ position: 'sticky', top: '0' }}>
          <tr>
            <th>N.</th>
            <th>SSID</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {this.state.tableData.map((row, index) => {
            return (
              <motion.tr
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                layout
                key={row.key}
                transition={{
                  opacity: { duration: 0.5 },
                }}
              >
                <td>{index + 1}</td>
                <td>{row.key}</td>
                <motion.td
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  layout
                  key={row.data}
                  transition={{
                    opacity: { duration: 0.5 },
                  }}
                >
                  {row.data}
                </motion.td>
              </motion.tr>
            )
          })}
        </tbody>
      </Table>
    )
  }
}
